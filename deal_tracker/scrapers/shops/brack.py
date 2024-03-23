from bs4 import BeautifulSoup

from deal_tracker.scrapers.exceptions import ItemParseError
from deal_tracker.scrapers.shops.base import BaseScraper


class BrackScraper(BaseScraper):
    shop_domain = "brack.ch"

    def _parse_response(self, response_text, url):
        item = self._init_item(url)
        soup = BeautifulSoup(response_text, "html.parser")
        try:
            item.description = (
                soup.select_one(".productStage__infoColumn").select_one(".productStage__infoText").ul.get_text()
            )
            item.brand = (
                soup.select_one(".productStage__infoColumn").select_one(".productStage__itemManufacturer").get_text()
            )
            branded_name = soup.select_one(".productStage__infoColumn").h1.get_text()
            item.name = branded_name.replace(item.brand, "")
            item.price = float(soup.select_one(".productStage__offeredPrice").select_one(".price").em.get_text())

            item.stock = int(soup.select_one(".stock__amount").get_text())
            image_url_data = soup.select_one("a.swiper-slide.js-lightbox-picture-top").get("href").strip("//")
            item.image_url = f"https://{image_url_data}"
            return item

        except AttributeError as e:
            raise ItemParseError from e
