import ConfigParser
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class ConfigManager:
    def __init__(self, file_path="../scraperlib/scraper.ini"):
        self.file_path = file_path
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.file_path)

    def config_section_map(self, section):
        dict1 = {}
        options = self.config.options(section)
        for option in options:
            try:
                dict1[option] = self.config.get(section, option)
                if dict1[option] == -1:
                    print "skip: " + str(option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    def get_mongo(self):
        local = self.config_section_map("mongo")['local']
        db = self.config_section_map("mongo")['db']

        if local == 'true':
            client = MongoClient()
            db = client[db]
            return db
        else:
            user = self.config_section_map("mongo")['user']
            password = self.config_section_map("mongo")['password']
            ip = self.config_section_map("mongo")['ip']
            port = self.config_section_map("mongo")['port']
            client = MongoClient('mongodb://' + user + ':' + password + '@' + ip + '', int(port))
            db = client[db]
            return db

    def get_driver(self):
        if self.config_section_map("selenium")['local'] == 'true':
            if self.config_section_map("selenium")['browser'] == 'firefox':
                driver = webdriver.Firefox()
            else:
                driver = webdriver.Chrome()
        else:
            ip = self.config_section_map("selenium")['ip']
            port = self.config_section_map("selenium")['port']
            browser = self.config_section_map("selenium")['browser']
            caps = DesiredCapabilities.CHROME
            if browser == 'firefox':
                caps = DesiredCapabilities.FIREFOX
            driver = webdriver.Remote(
                command_executor='http://' + ip + ':' + port + '/wd/hub',
                desired_capabilities=caps)
        return driver
