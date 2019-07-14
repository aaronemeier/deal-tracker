"""
 Worker

 TODO: Load scrapers in Shops
 TODO: Scrape items for each shop in Shops
"""


class Worker:
    def __init__(self):
        self.scrapers = []

    def register_scraper(self, scraper):
        self.scrapers.append(scraper)

    def run(self):
        for scraper in self.scrapers:
            scraper.resolve_items()
            scraper.update()
