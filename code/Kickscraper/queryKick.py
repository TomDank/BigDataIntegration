#scrapes query links stored in a text file form kickstarter.com

from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import json
import urllib
from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv
import kick


# A function to scrape project urls based on a kickstarter.com  query stored in query.txt

def scrapesUrls(query,driver):
    # the random user query is formated for kickstater search interface
    url = "https://www.kickstarter.com/discover/advanced?ref=nav_search&term=" + urllib.parse.quote(query) + "&woe_id=0&sort=magic&seed=2603901&page={0}"

    # urls are stored in a csv file
    DATA_FILE = "kick_query.csv"
    csvfile = open(DATA_FILE, 'w')  # output data as csv file
    csvwriter = csv.writer(csvfile)  # delimiter
    csvwriter.writerow(['querylinks'])

    page_start =1   # set a page number increment
    url = url.format(page_start)


    while True:
        driver.get(url)
        response = urlopen(url)
        html = response.read()

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        details= soup.find_all('div', {"class":"js-react-proj-card"}) #project details in a json object on the website

        if len(details) != 0:


            for div in details:
                project = json.loads(div['data-project'])  #the project data is stored as a json document
                row = [project["urls"]["web"]["project"]] #retrieves the proejct links that is stored as a json data with key/value pair

                print(row)

                csvwriter.writerow(row)

        page_start += 1
        url = "https://www.kickstarter.com/discover/advanced?ref=nav_search&term=" + urllib.parse.quote(
                query) + "&woe_id=0&sort=magic&seed=2603901&page={0}"
        url = url.format(page_start) #the url is formated to allow the pages to iterate to the next pages

        #the code stops if there are no projects to show
        if len(details) == 0:
            break
    return csvfile

# the main function implements the selenium web driver that reads the random user queries
def main():
    driver = webdriver.Chrome(executable_path='/Users/apple/PycharmProjects/untitled3/chromedriver') #chromedriver must be in path
    with open("query.txt") as queries:
        for query in queries.readlines():
            csvfile = scrapesUrls(query, driver)
            csvfile.close()
    # kick.getPageDetails("kick_query.csv")



main()
















