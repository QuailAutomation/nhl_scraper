#!/usr/bin/python

"""
A script that scrapes projections from cbssports.com and outputs them to csv
format.  It produces the following files:
    cbssports.skaters.proj.csv   : Projections for all skaters
    cbssports.goalies.proj.csv   : Projections for all goalies
"""
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd


class ProjectionScraper:
    def __init__(self):
        pass

    def scrape(self):
        driver = webdriver.Chrome()
        file_names = []
        try:
            driver.maximize_window()
            driver.implicitly_wait(15)
            driver.get(self.url())
            file_names.append(self.scrape_pos(driver, "D", "defense"))
            file_names.append(self.scrape_pos(driver, "F", "forwards"))
            file_names.append(self.scrape_pos(driver, "G", "goalies"))
        finally:
            driver.close()
        return file_names

    def scrape_pos(self, driver, pos_abrev, pos_long):
        driver.find_element_by_id("Dropdown-selectedText").click()
        driver.find_element_by_link_text(pos_abrev).click()
        time.sleep(5)
        fn = "cbs_sports.{}.html".format(pos_long)
        with open(fn, "w") as f:
            soup = BeautifulSoup(driver.page_source, "lxml")
            f.write(soup.prettify())
        return fn

    def url(self):
        return "https://www.cbssports.com/fantasy/hockey/stats"


class Parser:
    def __init__(self, file_name):
        with open(file_name, "rb") as f:
            self.soup = BeautifulSoup(f, "lxml")

    def parse(self, index_offset):
        table = self.soup.find_all('table')[0]
        headings = ["name", "Tm"] + \
            [th.get_text().strip().split("\n")[0] for th in
             table.find("thead").find_all("th")[1:]]
        table_body = table.find('tbody')
        df = pd.DataFrame(data=[], columns=headings)
        rows = table_body.find_all('tr')
        for i, row in enumerate(rows):
            plyr_cols = self.parse_name_team(row.find('td'))
            stat_cols = [ele.text.strip() for ele in row.find_all('td')[1:]]
            df = df.append(pd.DataFrame(data=[plyr_cols + stat_cols],
                                        columns=headings,
                                        index=[i + index_offset]))
        return df

    def parse_name_team(self, td):
        attrs = td.text.strip().split('\n')
        return [attrs[13].strip(), attrs[6].strip()]


if __name__ == "__main__":
    sc = ProjectionScraper()
    file_names = sc.scrape()

    skaters = None
    goalies = None
    for fn in file_names:
        p = Parser(fn)
        if "goalies" in fn:
            goalies = p.parse(0)
        else:
            if skaters is None:
                skaters = p.parse(0)
            else:
                skaters = skaters.append(p.parse(len(skaters.index)))

    skaters.to_csv("cbssports.skaters.proj.csv")
    goalies.to_csv("cbssports.goalies.proj.csv")
