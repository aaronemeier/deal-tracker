

class BaseScraper:

    def __init__(self):
        pass

    def resolve_items(self):
        return self.catalog.items

    def fetch_data(self, items):
        pass

    def update(self):
        items = self.resolve_items()
        self.fetch_data(items)


class DigitecScraper(BaseScraper):

    def __init__(self):
        self.catalog
        #self.shop = self.catalog.shop.get_by_name("Digitec")

