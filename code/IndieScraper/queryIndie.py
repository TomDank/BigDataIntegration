#scrapes query links stored in a text file form indiegogo.com

import csv
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from urllib.request import urlopen
from urllib.parse import urlencode
import urllib



DATA_FILE = "indie_query.csv"
csvfile = open(DATA_FILE, 'w')  # output data as csv file
csvwriter = csv.writer(csvfile)  # delimiter
csvwriter.writerow(['links'])

def initialStep(query, driver):
    url = "https://www.indiegogo.com/explore/all?project_type=campaign&project_timing=all&sort=trending&q=" + urllib.parse.quote(query) # formats user query
    driver.get(url)
    showMore(url, driver)

#this function scrapes the links of projects
def extractLink(url, driver):


    soup = BeautifulSoup(driver.page_source, 'html.parser')
    response = urlopen(url)
    html = response.read()

    time.sleep(2)
    for a in soup.find_all("a", {"gogo-test": "card"}): #scrapes the links to the projects that the query returns
        row = "https://www.indiegogo.com" + a['href']
        print(row)
        csvwriter.writerow([row])
    csvfile.close()

# Selenium webdriver gets past the cookie pop up if it appears
def showMore(url, driver):
    time.sleep(2)
    try:
        driver.find_element_by_css_selector('#CybotCookiebotDialogBodyLevelButtonAccept').click()

    except:
        pass
    while True:
        time.sleep(2)
        try:
            driver.find_element_by_css_selector(
                'body > div.ng-scope > div > div > div.ng-scope > explore-detail > div > div > div.exploreBody.row > section.exploreResults > div.ng-scope > div.exploreMore > div:nth-child(1) > div > a').click()
        except:

            extractLink(url, driver)
            break


def main():

    driver= webdriver.Chrome(executable_path='/Users/apple/PycharmProjects/untitled3/chromedriver') #the chromedriver should be in path
    with open("query.txt") as queries:          #uploads query.txt file which contains the random queries of the user
        for query in queries.readlines():
            initialStep(query,driver)


