import random
import time
import datetime
from scraperlib import config
from selenium.common.exceptions import WebDriverException


class ScraperUtils:

    def __init__(self):
        cm = config.ConfigManager()
        self.SHORT_MIN = cm.config_section_map("timeout")['short_min']
        self.SHORT_MAX = cm.config_section_map("timeout")['short_max']
        self.LONG_MIN = cm.config_section_map("timeout")['long_min']
        self.LONG_MAX = cm.config_section_map("timeout")['long_max']

    def long_timeout(self):
        self.sleep(self.LONG_MIN, self.LONG_MAX)

    def short_timeout(self):
        self.sleep(self.SHORT_MIN, self.SHORT_MAX)

    def sleep(self, _min, _max):
        time.sleep(random.randint(int(_min), int(_max)) + random.random())

    def get_current_url(self, driver):
        return driver.execute_script("""
            return window.location.href
        """)

    def create_category_object(self, category_url, category_name):
        post = {
            "category_url": category_url,
            "category_name": category_name,
            "scraped": False,
            "date_added": datetime.datetime.utcnow()

        }

        return post

    def create_job_object(self, question, answer, category):
        post = {
            "category": category,
            "question": question,
            "answer": answer,
            "date_added": datetime.datetime.utcnow(),
            "used": False
        }

        return post

    def click_element(self, web_element):
        if web_element is not None:
            try:
                web_element.click()
            except WebDriverException:
                print "Element is not clickable: " + str(web_element.text)
        else:
            print "element is None"
