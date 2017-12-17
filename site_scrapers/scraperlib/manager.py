from scraperlib import scraperutils
from scraperlib import config
import os


class ScraperManger:
    def __init__(self):
        self.SITE_NAME = os.path.split(os.getcwd())[1]
        cm = config.ConfigManager()
        self.db = cm.get_mongo()
        self.categories = self.db[self.SITE_NAME + '_categories']
        self.jobs = self.db[self.SITE_NAME + '_jobs']
        self.price = self.db[self.SITE_NAME + '_prices']
        self.driver = cm.get_driver()
        self.driverManager = DriverManager()

    def get_next_scrape(self, collection):
        doc = collection.find_one({'scraped': False})
        return doc

    def check_duplicate(self, job, document):

        res = job.find_one({'question': document['question']})
        return res

    def update_next_scrape(self, collection, document):
        if document is not None:
            id = collection.update_one({'_id': document['_id']}, {"$set": {"scraped": True}}, False)
            return id
        return -1


# In the future this object will manage requests on each proxy to balance them
class DriverManager:
    number_Scrapes = 0

    def __init__(self):
        self.data = []

    def check_driver(self, driver):
        if self.number_Scrapes < 10:
            self.number_Scrapes += 1
            return driver
        else:
            return scraperutils.get_driver()
