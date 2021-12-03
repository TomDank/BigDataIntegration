#scrapes project individual project details from urls stored in a csv file

#imports Selenium and BeautifulSoup dependencies
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time
from urllib.request import urlopen
import json
import csv

#uploads a csv file contatining a list of links to individual projects on Kickstarter.com
# Also a starting and stoping index is set so that a defined amount of links can be scraped at a time. This was required because the code breaks at some point due
# to the difference in  html code structure for some individual projects.

def csv_url_reader(url_obj):
    project_dict = {}
    reader = csv.DictReader(url_obj, delimiter =',')
    list_reader = list(reader)
    index = 0
    while index < 100: # only 100 links are scraped at a run
        data1 = []
        url = list_reader[index]["Project_url"] #the list reader concentrates on the column that holds the links to each project
        print(url)
        index = index + 1 # an increment that tells the code to go through each row


#Selenium uses the chrome browser to automates through each project website.
#chrome_options package allows chrome to run the background as a headless browser.

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path='/Users/apple/PycharmProjects/untitled3/chromedriver',
                                  options=chrome_options) #chrome webdriver needs to in path for Selenium webdriver to automates the browser
        driver.get(url) # Selenium webdriver access each link

        response = urlopen(url)
        html = response.read()

        soup = BeautifulSoup(html, 'html.parser') # BeautifulSoup parses the html content of each website using a generic parser called the html.parser

## Most project links on Kickstarter.com stores the summary of each project details in a json file that is kept in a div tag and class: bg-grey-100

        details = soup.find_all('div', {"class": "bg-grey-100"})  # BeautifulSoup finds the content of the div tag with class: bg-grey-100

        time.sleep(5)

        if len(details) != 0: # checks if details has contents
            for div in details:
                data=json.loads(div['data-initial']) #retrieves the proejct details that is stored as a json data with key/value pair


                # BeautifulSoup scrapes the data from the json data representation for an example, data["project"]["name"] will scrape the name of the project
                # The data is stored in the project_dict array eg project_dict["Name"]=data["project"]["name"] stores the project name
                #Also if the data is not present in the json file as in some projects, "NaN" is stored in the project_dict array

                try:
                    project_dict["Name"] = data["project"]["name"] # stores the project name as "Name" in the project_dict array
                except:
                    project_dict["Name"] = "NaN"

                try:
                    project_dict["Description"] = data["project"]["description"]
                except:
                    project_dict["Description"] = "NaN"

                try:
                    project_dict["Project_link"] = data["project"]["url"]
                except:
                    project_dict["Project_link"] = "NaN"


                try:
                    project_dict["Project_Category"] = data["project"]["category"]["name"]
                except:
                    project_dict["Project_Category"] = "NaN"


                try:
                    project_dict["Location"]=data["project"]["location"]["displayableName"]

                except:
                    project_dict["Location"] = "NaN"


                try:
                    project_dict["Backers"] = data["project"]["backersCount"]
                except:
                    project_dict["Backers"] = "NaN"

                try:
                    project_dict["Target_Amount"] = data["project"]["goal"]["amount"]
                except:
                    project_dict["Target_Amount"] = "NaN"

                try:
                    project_dict["Pledged"] = data["project"]["pledged"]["amount"]
                except:
                    project_dict["Pledged"] = "NaN"

                try:
                    project_dict["Currency"] = data["project"]["goal"]["currency"]
                except:
                    project_dict["Currency"] = "NaN"

                try:
                    project_dict["Name_of_Creator"] = data["project"]["creator"]["name"]
                except:
                    project_dict["Name_of_Creator"] = "NaN"

                try:
                    project_dict["Profile_Link"] = data["project"]["creator"]["url"]
                except:
                    project_dict["Profile_Link"] = "NaN"

                try:
                    project_dict["Number_of_Comments"] = data["project"]["commentsCount"]
                except:
                    project_dict["Number_of_Comments"] = "NaN"

                try:
                    project_dict["Creator_websites"] = data["project"]["creator"]["websites"]
                except:
                    project_dict["Creator_websites"] = "NaN"

        # if BeautifulSoup does not find the content of the div tag with class: bg-grey-100
        # then the proect details are scraped using other html tags and class example the project name can also be scraped by accessing the "a" tag and class:"hero_link"
        else:
            time.sleep(5)
            try:
                project_dict["Name"] = soup.find('a', {"class":"hero__link"}).text
            except:
                project_dict["Name"] = "NaN"

            try:
                project_dict["Description"] = soup.find('span', {"class":"content"}).text
            except: project_dict["Description"] = "NaN"

            try:
                project_url1 = soup.find("a", class_="hero__link")
                project_dict["Project_link"] = "kickstarter.com" + project_url1['href']  #captures the project link by appending it to the base url "kickstarter.com"

            except:
                project_dict["Project_link"] = "NaN"

            # This section provides two option that captures the project category
            #First it looks for the parent div tag with class: "NS_projects__category_location ratio-16-9 flex items-center"
            #If the class exists then the text content of the sibling tag "a" with the composite class: "grey-dark mr3 nowrap type-12" is scraped. the text content is the project category

            if soup.find("div", {"class": "NS_projects__category_location ratio-16-9 flex items-center"}) != None:
                b = soup.find("div", {"class": "NS_projects__category_location ratio-16-9 flex items-center"})

                try:
                    for a in b:
                        project_dict["Project_Category"] = soup.find("a", {
                            "class": "grey-dark mr3 nowrap type-12"}).find_next("a").text

                except:

                    project_dict["Project_Category"] = soup.find("span", {"class": "ml1"}).text # Another option to capture project category is to target the span tag with class: "ml1"

            else:
                project_dict["Project_Category"] = "NaN"

            if soup.find("a", {"class": "grey-dark mr3 nowrap type-12"}) !=None:

                try:
                    project_dict["Location"] = soup.find("a", {"class": "grey-dark mr3 nowrap type-12"}).text
                except:

                    project_dict["Location"] = "NaN"


                #BeautifulSoup finds if the div tag with class:"NS_spotlight_stats" exists
                #the first part of the the text attribute of div tag with class:"NS_spotlight_stats"
            if soup.find("div", {"class": 'NS_campaigns__spotlight_stats'}) != None:
                try:
                    project_dict["Backers"] = \
                    soup.find("div", {"class": 'NS_campaigns__spotlight_stats'}).text.replace(',', '').split(' ')[0] # the first part of the text content is split to give the number of backers
                except:
                    project_dict["Backers"] = "NaN"

            if soup.find("div", {"class": "type-12 medium navy-500"}) != None:
                try:
                    project_dict["Target_Amount"] = soup.find("div", {"class": "type-12 medium navy-500"}).text # scrapes the Target amount for a project
                except:
                    project_dict["Target_Amount"] = "NaN"

            if soup.find("div", {"class": 'NS_campaigns__spotlight_stats'}) != None:
                try:
                    project_dict["Pledged"] = \
                soup.find("div", {"class": 'NS_campaigns__spotlight_stats'}).text.replace(',', '').split(' ')[3] # splits the first 3 characters of the text attribute to retrieve the amount pledged for a project
                except:
                    project_dict["Pledged"] = "NaN"

            if soup.find("span", {"class": "money"}) != None:
                try:
                    project_dict["Currency"] = soup.find("span", {"class": "money"}).text[0] # scrapes only the first character of the text attribute content to retrieve the currency used for the project
                except:
                    project_dict["Currency"] = "NaN"

            # scrapes the name of the project owner
            if soup.find('div', {"class": "creator-name"}) != None:
                try:
                    project_dict["Name_of_Creator"] = soup.find('div', {"class": "creator-name"}).text #retrieves the content of the text attribute for the name of the project creator
                except:
                    project_dict["Name_of_Creator"] = "NaN"

            #This part retreives the the link to the creators profile on kickstarter.com

            if soup.find("a", class_="js-update-text-color")['href'] != None:
                try:
                    project_dict["Profile_Link"] = "kickstarter.com" + soup.find("a", class_="js-update-text-color")['href'] # appends the content of the href attribute to the base url "kickstarte.com"
                except:
                    project_dict["Profile_Link"] = "NaN"

            # This part retrieves the total number of comments on the project
            if soup.find("a", {"class": 'js-load-project-comments'}) != None:
                try:
                    project_dict["Number_of_Comments"] = soup.find("a", {"class": 'js-load-project-comments'}).text #the text file content of the "a" tag with class:"js-load-project-comments" contains the number of comments
                except:
                    project_dict["Number_of_Comments"] = "NaN"




            #to target the the websites of the project owner, BeautifulSoup is used with Selenium to navigate to the section that has the websites of the project owner


            soup = BeautifulSoup(driver.page_source, 'html.parser')

            test = soup.find('div', {"class": "NS_projects__creator_spotlight"})
            soup1 = BeautifulSoup(driver.page_source, 'html.parser')
            time.sleep(5)

            #Selenium webdriver locates and clicks the link that leads to page where the the project owner is stored.

            python_button1 = driver.find_element_by_css_selector(
                '#content-wrap > section > div.project-profile__content > div.grid-container.pb3.pb10-sm > div > div.grid-col-12.grid-col-4-lg > div.NS_projects__creator_spotlight.mobile-center > div.flag > div.flag-body > div > div.creator-name > div.mobile-hide > a').click()

            soup0 = BeautifulSoup(driver.page_source, 'html.parser') # a new BeautifulSoup collection of the html content of the new page is created
            user_url = soup0.find("ul", {"class": "links"})
            soup2 = BeautifulSoup(driver.page_source, 'html.parser')

            time.sleep(5)

            # at the new page, BeautifulSoup finds the "a" tag and attribute "rel" with value:"nofollow noopener" that contains the href attribute

            if soup2.find("a", {"rel": "nofollow noopener"}, href=True) !=None:
                creator_url1 = soup2.find("a", {"rel": "nofollow noopener"}, href=True)

                try:
                    project_dict["Creator_websites"] = creator_url1.text #the text content of the href attribute is scraped and this is the links to the creator owner websites
                except:

                    project_dict["Creator_websites"] = creator_url1

            else:
                project_dict["Creator_websites"] = "NaN"



        driver.refresh() # Selenium webdriver refreshes the page


        time.sleep(5) # the code waits for 5 seconds to get all contents on the page fully loaded



        python_button3 = driver.find_element_by_id('campaign-emoji') # selenium webdriver finds the clickable button to the campaign section
        python_button3.click()  # click link

        time.sleep(5)

        # scraping the detailed description of a project

        driver.refresh() # the page is referesed where it automatically shows the campaign description of the project

        driver.find_element_by_class_name('description-container') # Selenium finds the class that contains the campaign details

        project_dict["Campaign"] = '\n'.join([a.text for a in driver.find_elements_by_tag_name('p')[5:-3]]) # the whole text content in the tag "p" is scraped this is the detailed description for the project



        driver.refresh() # the page is refreshed to get it back in the original state
        time.sleep(5)

        #scraping the updates section of the project

        python_button4 = driver.find_element_by_id('updates-emoji') #Selenium webdriver finds the link that leads to the updates section of the project
        python_button4.click() # python clicks the updates button


        if  soup.find("div", {"class": "NS_projects__updates_section"}) != None:
            try:
                soup1 = BeautifulSoup(driver.page_source, 'html.parser')
                time.sleep(5)
                project_dict["Updates"]= soup1.find("div", {"class": "timeline"}).text # the text content is scraped as the updates to thr project
            except:
                soup2 = BeautifulSoup(html, 'html.parser')
                project_dict["Updates"]= soup2.find("div", {"class": "timeline"}).text # another option to scrape the updates section
        else:

            try:
                soup3 = BeautifulSoup(html, 'html.parser')
                soup3.find("div", {"class": "container-flex px3"})
                project_dict["Updates"] = ("None")

            except:
                soup3 = BeautifulSoup(driver.page_source, 'html.parser')
                soup3.find("div", {"class": "container-flex px3"})
                project_dict["Updates"] = ("None")



        driver.refresh() # page refreshes

        python_button5 = driver.find_element_by_id('comments-emoji') # Selenium finds the comments section on the web page
        python_button5.click() #clicks the link to the comments section
        time.sleep(5)
        soup3 = BeautifulSoup(driver.page_source, 'html.parser')

        if soup3.find("ul", {"class": "bg-grey-100 border border-grey-400 p2 mb3"}) != None:

            project_dict["Comments"] = soup3.find("ul", {"class": "bg-grey-100 border border-grey-400 p2 mb3"}).text #the text contents is the "ul" tag is retrived as the comments


        else:

            project_dict["Comments"] = soup3.find("ul", {"class": "bg-grey-100 border border-grey-400 p2 mb3"}) # another option to scrape the comments section


        # Data cleaning stage
        # the scraped data are again defined to be called in the data cleaning function "clean_string"

        Name = project_dict["Name"]
        Description =  project_dict["Description"]
        Project_Category = project_dict["Project_Category"]
        Location = project_dict["Location"]
        Backers = project_dict["Backers"]
        Target_Amount = project_dict["Target_Amount"]
        Pledged = project_dict["Pledged"]
        Currency = project_dict["Currency"]
        Name_of_Creator = project_dict["Name_of_Creator"]
        Profile_Link = project_dict["Profile_Link"]
        Number_of_Comments = project_dict["Number_of_Comments"]
        Comments = project_dict["Comments"]
        Updates = project_dict["Updates"]
        Campaign_Description = project_dict["Campaign"]


        # a data cleaning function "clean_string" is defined

        def clean_string(var):

            var = str(var)
            var = var.rstrip()
            var = var.replace('\n', '.') #replaces escape charaters with "."
            return var

        # The scraped data are fed into the data cleaning function

        project_dict["Name"] = clean_string(Name)
        project_dict["Description"] = clean_string(Description)
        project_dict["Project_Category"] = clean_string(Project_Category)
        project_dict["Location"] = clean_string(Location)
        project_dict["Backers"] = clean_string(Backers)
        project_dict["Target_Amount"] = clean_string(Target_Amount)
        project_dict["Pledged"] = clean_string(Pledged)
        project_dict["Currency"] = clean_string(Currency)
        project_dict["Name_of_Creator"] = clean_string(Name_of_Creator)
        project_dict["Profile_Link"] = clean_string(Profile_Link)
        project_dict["Number_of_Comments"] = clean_string(Number_of_Comments)
        project_dict["Campaign"] = clean_string(Campaign_Description)
        project_dict["Comments"] = clean_string(Comments)
        project_dict["Updates"] = clean_string(Updates)


        #print(project_dict)

        data1.append(project_dict.copy()) # the copy() targets an error where retreiving the text attributes causes the code when scraping some of the projects. hence the html content is retrieved with the tags




        ## should uncommented to enable the code to scrape directly to a MongoDB databse

        # db_client = MongoClient()

        ##db = client.my_db




        # the data scraped is either stored to a csv file locally or can enabled to store to MongoDB

        for project in data1:
            # db_client.my_db.kickstarter.insert(project)

            with open("kick_data.json", "a") as outfile: #the csv filed stored locally
                json.dump(project, outfile)
                outfile.write('')

            print(project)


        driver.quit() # Selenium web driver closes


# This function uploads a text file that contains the links to user queries from the queryKick.py

def getPageDetails(query_result):
    with open(query_result) as url_obj:
        csv_url_reader(url_obj)





