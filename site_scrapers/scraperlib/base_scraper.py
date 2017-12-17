from scraperlib import scraperutils
import manager


class BaseScraper:
    def __init__(self):
        self.sm = manager.ScraperManger()
        self.su = scraperutils.ScraperUtils()


class BaseGridScraper(BaseScraper):
    def __init__(self):
        BaseScraper.__init__(self)