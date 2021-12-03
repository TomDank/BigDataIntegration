#This scrape all project details from Indiegogo.com based on a query text

import queryIndie #imports the queryIndie.py file that scrapes the project links according to a query file
import Indiegogo #imports Indiegogo.py file that scrapes the details of the projects according to the links from the queryIndie.py
import csv, time, os

#this function scrapes the Indiegogo website
def main():
    queryIndie.main()

    Indiegogo.getPageDetails()

main()