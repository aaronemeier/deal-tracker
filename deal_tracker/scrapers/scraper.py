import inspect
from collections import OrderedDict

from . import shops
from .exceptions import ScraperNotFound


class ScraperFactory:
    def __init__(self) -> None:
        self._shops: OrderedDict = OrderedDict()
        self._register_shops()

    def _register_shops(self):
        for _, obj in inspect.getmembers(shops):
            if inspect.isclass(obj):
                domain = getattr(obj, "shop_domain", False)
                if domain:
                    self._shops.update({domain: obj()})

    def get_scraper(self, domain):
        if (scraper := self._shops.get(domain)) is not None:
            return scraper
        raise ScraperNotFound(f"Scraper for {domain} not found")

    def get_scrapers(self):
        return self._shops
