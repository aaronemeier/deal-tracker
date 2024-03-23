import re
from json import JSONDecodeError
from typing import Optional

import requests
import undetected_chromedriver as uc
from requests import Session
from requests.exceptions import ProxyError, ConnectTimeout, ReadTimeout
from selenium.webdriver.chrome.options import Options

from deal_tracker.scrapers.exceptions import ItemUrlInvalid, ItemParseError, ScraperTimeout, ScraperResponseError
from deal_tracker.scrapers.models import Item
from deal_tracker.scrapers.settings import USER_AGENT, LANGUAGE, TIMEOUT


class BaseScraper:
    shop_domain: Optional[str] = None
    language = LANGUAGE
    user_agent = USER_AGENT
    timeout = TIMEOUT
    use_selenium = False

    def __init__(self):
        if self.shop_domain is None:
            raise NotImplementedError("shop_domain is not implemented")
        self.proxies = {}
        self.session = None

    def _get_session(self, use_proxy=False) -> Session:
        if self.session is not None:
            return self.session
        session = requests.session()
        session.headers.update(
            {
                "User-agent": self.user_agent,
                "accept-language": self.language,
                "encoding": "utf-8",
            }
        )
        if use_proxy:
            session.proxies = self.proxies
        return session

    def set_proxy(self, http_proxy, https_proxy):
        self.proxies = {"http": http_proxy, "https": https_proxy}

    def scrape_item(self, url) -> Item:
        self.__check_valid_url(url)
        response_text = self._get_response_text(url)
        item = self._parse_response(response_text, url)
        self._check_item(item)
        return item

    def _get_response_text(self, url):
        if self.use_selenium:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            driver = uc.Chrome(
                options=chrome_options,
                # Workaround to prevents issue with Celery, which doesn't use the multiprocessing library
                # Alternative solution https://stackoverflow.com/a/54917626
                use_subprocess=True,
            )

            try:
                driver.get(url)
                response_text = driver.find_element("xpath", "//*").get_attribute("outerHTML")

                for text in ("captcha", "Captcha", "Cloudflare"):
                    if text in response_text:
                        raise ScraperResponseError("Bot Protection detected")
                return response_text

            except ResourceWarning as e:
                raise ScraperResponseError(f"Error while getting response from {url}: {e}") from e

            finally:
                driver.close()

        else:
            session = self._get_session()
            try:
                response = session.get(url, timeout=self.timeout)

            except (ReadTimeout, JSONDecodeError, ProxyError, ConnectTimeout) as e:
                raise ScraperTimeout from e

            finally:
                session.close()

            if response.status_code != 200:
                raise ScraperResponseError(f"status_code={response.status_code}, response={response.text}")
            return response.text

    def __check_valid_url(self, url):
        regex_pre = "^https?://(?:www.)?"
        regex_post = "/[a-z0-9-./]+$"
        pattern = re.compile(f"{regex_pre}{self.shop_domain}{regex_post}", re.IGNORECASE)
        if pattern.search(url) is None:
            raise ItemUrlInvalid(f"The URL {url} is invalid.")

    def _init_item(self, url):
        return Item(url=url, shop=self.shop_domain)

    @staticmethod
    def _check_item(item):
        if item is None or item.is_empty():
            raise ItemParseError(f"Item was not parsed correctly. item={item.__dict__}")

    def _parse_response(self, response_text, url):
        raise NotImplementedError()
