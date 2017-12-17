import sys
import json
import ast

sys.path.append('../')
from scraperlib import base_scraper


class HansenCatScraper(base_scraper.BaseScraper):

    def __init__(self):
        base_scraper.BaseScraper.__init__(self)

    def get_craigs_list(self):
        cats = self.sm.driver.execute_script("""
        
   var linkArray = []
        var obj = $(".result-title");
        jQuery.each(obj, function (index, value) {
           var link = value.href;
           linkArray.push(link);
         });
        return linkArray;
   
        
        
        """)

        return cats

    def run_scraper(self):
        self.sm.driver.get('https://newyork.craigslist.org/search/sss?sort=date&query=dear%20evan%20hansen')
        self.su.short_timeout()
        lin = self.get_craigs_list()

        for n in range(0, len(lin)):
            # t = ast.literal_eval(json.dumps(n))
            # # print type(t)
            post = self.su.create_category_object(lin[n])
            self.sm.categories.insert_one(post).inserted_id

        self.sm.driver.quit()


HansenCatScraper().run_scraper()
