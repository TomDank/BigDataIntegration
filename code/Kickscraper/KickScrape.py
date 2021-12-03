#This scrape all project details from kickstarter.com based on a query text

import queryKick #imports the queryKick.py file that scrapes the links of project according to query.txt file
import kick #import kick.py file that scrapes the details of kickstarter project according to the links from queryKick.py file
import csv, time, os

#this function runs the imported Python files

def main():
    queryKick.main()
    kick.getPageDetails("kick_query.csv") #uploads scrapes the project details according to the links provided by the user query

main()