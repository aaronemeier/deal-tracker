import json

from bs4 import BeautifulSoup

from deal_tracker.scrapers.exceptions import ItemParseError
from deal_tracker.scrapers.shops.base import BaseScraper


class JyskScraper(BaseScraper):
    shop_domain = "jysk.ch"

    def _parse_response(self, response_text, url):
        item = self._init_item(url)
        soup = BeautifulSoup(response_text, "html.parser")
        try:
            script = soup.find("script", {"data-drupal-selector": "drupal-settings-json"}).text
            parsed = json.loads(script.encode("utf-8"), strict=False)
            item.stock = int(parsed["jysk_react"]["checkout"]["online_sales"])
            data_layer = parsed["dataLayer"]
            parsed = json.loads(data_layer, strict=False)
            print(parsed)
            product = parsed["productDetailPage"]["data"]["ecommerce"]["detail"]["products"][0]
            item.name = product["name"]
            item.price = float(product["price"])
            item.brand = product["brand"]

            meta_image = soup.find("meta", property="og:image")
            if not meta_image:
                raise ItemParseError("Could not find required meta tags")

            item.image_url = meta_image["content"]
            item.description = soup.select_one(".product-details-description").find("p").get_text()

            return item

        except AttributeError as e:
            raise ItemParseError from e
