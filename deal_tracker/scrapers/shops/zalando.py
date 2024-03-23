import json
from bs4 import BeautifulSoup

from deal_tracker.scrapers.exceptions import ItemParseError
from deal_tracker.scrapers.shops.base import BaseScraper


class ZalandoScraper(BaseScraper):
    shop_domain = "zalando.ch"

    def _parse_response(self, response_text, url):
        item = self._init_item(url)
        soup = BeautifulSoup(response_text, "html.parser")
        script = soup.find("script", type="application/ld+json")
        json_data = json.loads(script.get_text())

        try:
            item.name = json_data["name"]
            item.description = json_data["description"]
            item.brand = json_data["brand"]["name"]
            item.image_url = json_data["image"][0]
            offers = json_data["offers"]
            available_offers = list(filter(lambda offer: offer["availability"] == "http://schema.org/InStock", offers))
            if len(available_offers) > 0:
                item.price = float(sorted(available_offers, key=lambda offer: offer["price"])[0]["price"])
                item.stock = 1
            else:
                item.price = offers[0]["price"]
                item.stock = 0
            return item

        except AttributeError as e:
            raise ItemParseError from e
