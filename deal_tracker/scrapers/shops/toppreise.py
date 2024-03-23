from bs4 import BeautifulSoup

from deal_tracker.scrapers.exceptions import ItemParseError
from deal_tracker.scrapers.shops.base import BaseScraper


class ToppreiseScraper(BaseScraper):
    shop_domain = "toppreise.ch"
    use_selenium = True

    def _parse_response(self, response_text, url):
        item = self._init_item(url)
        soup = BeautifulSoup(response_text, "html.parser")

        try:
            header = soup.find("h1")
            brand = header.find("b").get_text().strip()
            name_with_brand = header.get_text().strip()
            item.name = name_with_brand.replace(brand, "").strip()
            item.brand = brand[0] + brand[1:].lower()
            item.image_url = soup.find("meta", property="og:image:secure_url").get("content").strip()
            item.description = soup.select_one(".product-features").get_text().strip()
            item.price = float(soup.select_one(".priceContainer, .shippingPrice").find("div").get_text().strip())
            item.stock = 1 if soup.select_one(".TPIcons-avail_1") is not None else 0
            return item

        except AttributeError as e:
            raise ItemParseError from e
