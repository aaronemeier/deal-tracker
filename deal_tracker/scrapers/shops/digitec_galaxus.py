from json import JSONDecodeError
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from deal_tracker.scrapers.exceptions import ItemParseError
from deal_tracker.scrapers.shops.base import BaseScraper


class DigitecGalaxusScraper(BaseScraper):
    user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9"
        " (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"
    )

    def _parse_response(self, response_text, url):
        item = self._init_item(url)
        soup = BeautifulSoup(response_text, "html.parser")
        try:
            meta_name = soup.find("meta", property="og:title")
            meta_description = soup.find("meta", property="og:description")
            meta_brand = soup.find("meta", property="og:brand")
            meta_amount = soup.find("meta", property="product:price:amount")
            meta_availability = soup.find("meta", property="og:availability")
            meta_image = soup.find("meta", property="og:image")

            if not (meta_name or meta_description or meta_brand or meta_amount):
                raise ItemParseError("Could not find required meta tags")

            item.name = meta_name["content"]
            item.description = meta_description["content"]
            item.brand = meta_brand["content"]
            item.price = float(meta_amount["content"])
            item.stock = 0
            item.image_url = ""

            if meta_availability and meta_availability["content"] == "in stock":
                item.stock = 10

            if meta_image:
                image_url_data = meta_image["content"]
                item.image_url = self.clean_image_url(image_url_data)

            return item

        except (KeyError, JSONDecodeError) as e:
            raise ItemParseError from e

    def clean_image_url(self, image_url) -> str:
        return urljoin(f"https://www.{self.shop_domain}/im/Files/", image_url)


class DigitecScraper(DigitecGalaxusScraper):
    shop_domain = "digitec.ch"


class GalaxusScraper(DigitecGalaxusScraper):
    shop_domain = "galaxus.ch"
