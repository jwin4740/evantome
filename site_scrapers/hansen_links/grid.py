import sys

import json
import ast

sys.path.append('../')
from scraperlib import base_scraper


class TriviaGridScraper(base_scraper.BaseScraper):

    def __init__(self):
        base_scraper.BaseScraper.__init__(self)

    def grab_data(self):
        res = self.sm.driver.execute_script("""
           var q = document.getElementsByClassName('title')[0].children[0].innerText;
           var answer = document.getElementsByClassName('spoiler-content')[0].innerText;
           var title = document.getElementsByClassName('page-title')[0].innerText;
           let t = {
                category : title,
                question : q,
                answer : answer}
            return t;
        """)

        return ast.literal_eval(json.dumps(res))

    def insert_links(self, question, answer, category):
        job = self.su.create_job_object(question, answer, category)
        return job

    def next_page_disabled(self):
        return self.sm.driver.execute_script("""
                var t = document.getElementsByClassName('pager-next')[0]
                if (t){
                return false;
                } else {
                return true;}
             
            """)

    def click_next(self):
        self.su.short_timeout()
        self.sm.driver.execute_script("""
            document.getElementsByClassName('pager-next')[0].children[0].click();
            """)
        # self.su.short_timeout()

    def run_scraper(self):
        global running
        global repeat_counter
        doc = self.sm.get_next_scrape(self.sm.categories)
        running = True
        repeat_counter = 0
        counter = 0
        # while doc is not None:
        url = doc["category_url"]
        while running:
            n = url + "?page=" + str(counter)

            self.sm.driver.get(n)
            current = self.grab_data()
            print current["question"]

            res = self.sm.check_duplicate(self.sm.jobs, current)
            if res is not None:
                if current["question"] == res["question"]:
                    # means that there is already an entry in the mongo database
                    repeat_counter += 1
                    if repeat_counter > 2:
                        running = False
                        print "set to false"
                else:
                    repeat_counter = 0
                    print "not false"
                counter += 1
            else:
                print("inserting...")
                self.sm.jobs.insert_one(self.insert_links(current["question"], current["answer"], current["category"]))
            # if res is not None:
            #     self.sm.jobs.insert_one(job)
            # return t["question"]

            # doc = self.sm.get_next_scrape(self.sm.categories)
            # self.sm.update_next_scrape(self.sm.categories, doc)

        self.sm.driver.quit()


TriviaGridScraper().run_scraper()
