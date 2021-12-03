#scrapes project individual project details from urls stored in a csv file

import csv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import time
from urllib.request import urlopen
import json

def csv_url_reader(url_obj):
    project_dict = {}

    reader = csv.DictReader(url_obj, delimiter=',')
    list_reader =list(reader)
    index = 0
    while index < 2:
        data1 = []
        # project_dict = {}
        url = list_reader[index]["links"]
        print(url)
        index = index + 1

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path='/Users/apple/PycharmProjects/untitled3/chromedriver',
                                  options=chrome_options)
        driver.get(url)

        response = urlopen(url)
        html = response.read()
        # print(html)

        soup = BeautifulSoup(driver.page_source, 'html.parser')


        time.sleep(2)

        #Selenium webdriver identifies the cookie popup and clicks on it to access the page

        if driver.find_element_by_css_selector('#CybotCookiebotDialogBodyLevelButtonAccept') != None:

            try:
                driver.find_element_by_css_selector('#CybotCookiebotDialogBodyLevelButtonAccept').click()

            except NoSuchElementException: # if cookie pop up does not appear selenium proceeds to the main website
                pass

        else:
            pass

        time.sleep(2)
        # scrapes the name of the project
        if soup.find("h2", {"class": "preLaunch-headerSection-title t-align--center"}) != None:
            try:
                project_dict["Name"] = soup.find("h2", {"class": "preLaunch-headerSection-title t-align--center"}).text # identifies the text attribute and scrapes the name of the project
            except:
                project_dict["Name"] = "NaN"

        elif soup.find("div", {"class": "campaignHeaderBasics-title ng-binding"}) != None:
            project_dict["Name"] = soup.find("div", {"class": "campaignHeaderBasics-title ng-binding"}).text
        else:
           project_dict["Name"] = soup.find("div", {"class": "basicsSection-title is-hidden-tablet t-h3--sansSerif"}).text



        # scrapes the text that gives a summary of the project
        if soup.find("h5", {"class": "preLaunch-headerSection-subtitle t-align--center"}) != None:
            try:
                project_dict["project_Summary"] = soup.find("h5", {"class": "preLaunch-headerSection-subtitle t-align--center"}).text
            except:
                project_dict["project_Summary"] = "NaN"
        elif soup.find("div", {"class": "campaignHeaderBasics-tagline ng-binding"}) != None:
            project_dict["project_Summary"] = soup.find("div", {"class": "campaignHeaderBasics-tagline ng-binding"}).text
        else:
            project_dict["project_Summary"] = soup.find("div", {"class": "basicsSection-tagline is-hidden-desktop t-h5--sansSerif"}).text



        # scrapes the link to the project on indiegogo.com
        project_dict["Project_Link"] = url

        if soup.find("div",{"class":"basicsCampaignOwner-details-city"}) != None:
            project_dict["Project_Location"] = soup.find("div",{"class":"basicsCampaignOwner-details-city"}).text
        elif soup.find("div", {"class": "campaignTrust-detailsLocation ng-binding"}) != None:
            project_dict["Project_Location"] = soup.find("div", {"class": "campaignTrust-detailsLocation ng-binding"}).text
        else:
            project_dict["Project_Location"] = "NaN"


        #scrapes the project Backers
        if soup.find("span", {"class": "t-weight--medium"}) != None:
            try:
                project_dict["Project_Backers"] = soup.find("span", {"class": "t-weight--medium"}).text
            except:
                project_dict["project_Backers"] = "NaN"

        elif driver.find_elements_by_class_name("statusTab-countPill--light-grey") != None:
            try:
                project_dict["Project_Backers"] = driver.find_element_by_css_selector('body > div.ng-scope > div > div > campaign-page > div > campaign-body > div > div.campaignBody-horizontal > div > div.campaignBody-leadSection > campaign-navigation > filter-tabs > div > ul:nth-child(5) > li > filter-tab > div > span.statusTab-countPill.statusTab-countPill--light-grey').text
            except:
                project_dict["Project_Backers"] = "NaN"
        else:
            project_dict["Project_Backers"] = "NaN"


        #scrapes the target amount of the project
        if soup.find("span",{"class":"basicsGoalProgress-progressDetails-detailsGoal-goalPercentageOrInitiallyRaised"}) != None:
            project_dict["Target_Amount"] = soup.find("span",{"class":"basicsGoalProgress-progressDetails-detailsGoal-goalPercentageOrInitiallyRaised"}).text[17:24] #targets a specific section of the text attribute to retrieve the target amount
        elif soup.find("span", {"class": "indemandProgress-raisedAmount ng-binding"}) != None:
            project_dict["Target_Amount"] = soup.find("span", {"class": "indemandProgress-raisedAmount ng-binding"}).text
        else:
            project_dict["Target_Amount"] = "NaN"

        #scrapes the amount pledged for the project

        if soup.find("span",{"class":"basicsGoalProgress-amountSold t-h5--sansSerif t-weight--bold"}) != None:
            project_dict["Pledged"] = soup.find("span",{"class":"basicsGoalProgress-amountSold t-h5--sansSerif t-weight--bold"}).text
        elif soup.find("span", {"class": "indemandProgress-raisedAmount ng-binding"}) != None:
            project_dict["Pledged"] = soup.find("span", {"class": "indemandProgress-raisedAmount ng-binding"}).text
        else:
            project_dict["Pledged"] = "NaN"

        #scrapes the type of currency that defines the funding of the project

        if soup.find("span",{"class":"basicsGoalProgress-raisedCurrency"}) != None:
            project_dict["Currency"] = soup.find("span",{"class":"basicsGoalProgress-raisedCurrency"}).text
        elif soup.find("span", {"class": "indemandProgress-raisedAmount ng-binding"}) != None:
            project_dict["Currency"] = soup.find("span", {"class": "indemandProgress-raisedAmount ng-binding"}).text[0:1]
        else:
            project_dict["Currency"] ="NaN"

        #scrapes the days remaining till the project completion
        if soup.find("div",{"class":"basicsGoalProgress-progressDetails-detailsTimeLeft column t-body--sansSerif t-align--right"}) !=None:
            project_dict["Days_left"] = soup.find("div",{"class":"basicsGoalProgress-progressDetails-detailsTimeLeft column t-body--sansSerif t-align--right"}).text[0:2]
        else:
            project_dict["Days_left"] = "NaN"


        time.sleep(2)

        # Selenium automates the websites to the project story (details) section
        # Selenium retrieves the content of the text attribute as the story of the project
        try:
             if driver.find_element_by_link_text("STORY") != None:
                driver.find_element_by_link_text("STORY").click()

                time.sleep(5)

                project_dict["story"] = driver.find_element_by_xpath('//*[@id="vCampaignRouterContent"]/div[2]/div/div/div[2]').text
             else:
                 project_dict["story"] = driver.find_element_by_id("mainContent").text
        except NoSuchElementException:
            project_dict["story"] = "NaN"


        time.sleep(2)


        #Selenium automates the browser to the FAQ section of the website
        #BeautifulSoup retrieves the content of the text attributes as the FAQ of the project
        try:
            if driver.find_element_by_link_text("FAQ") != None:
                driver.find_element_by_link_text("FAQ").click()
                time.sleep(2)

                soup1 = BeautifulSoup(driver.page_source, 'html.parser')
                try:

                    project_dict["FAQ"] = soup1.find("div", {"class": "faqSection-container"}).text
                except:
                    project_dict["FAQ"] = "NaN"
        except NoSuchElementException:
            project_dict["FAQ"] = "NaN"
            time.sleep(2)

        #Selenium automates the browser to the Updates section of the website
        #BeautifulSoup is used to scrape the current number of updates of the project

        try:
            if driver.find_element_by_css_selector('a.tabHeadersWithPill-tab:nth-child(3) > div:nth-child(1) > span:nth-child(1)') != None:
                b = driver.find_element_by_css_selector(
                    'a.tabHeadersWithPill-tab:nth-child(3) > div:nth-child(1) > span:nth-child(1)')
                b.click()
                time.sleep(2)
                soup2 = BeautifulSoup(driver.page_source, 'html.parser')

                project_dict["Number_of_Updates"] = soup2.find("span", {"class": "tabHeadersWithPill-tab-pill t-label--sm"}).text

            else:
                project_dict["Number_of_Updates"] = "NaN"

        except NoSuchElementException:
            project_dict["Number_of_Updates"] = "NaN"


        time.sleep(2)

        #The the current updates to the project is scraped in this section
        try:

            if driver.find_element_by_css_selector('a.tabHeadersWithPill-tab:nth-child(3) > div:nth-child(1) > span:nth-child(1)') != None:
                b = driver.find_element_by_css_selector(
                    'a.tabHeadersWithPill-tab:nth-child(3) > div:nth-child(1) > span:nth-child(1)')
                b.click()
                time.sleep(2)
                soup2 = BeautifulSoup(driver.page_source, 'html.parser')

                if soup2.find("div", {"class": "routerContentUpdates"}) != None:
                    project_dict["Project_Updates"] = soup2.find("div", {"class": "routerContentUpdates"}).text

                else:
                    project_dict["Project_Updates"] = "NaN"


            else:
                project_dict["Project_Updates"] = "NaN"

        except NoSuchElementException:
            project_dict["Project_Updates"] = "NaN"


        time.sleep(2)


        #Scrapes the number of comments
        try:

            if driver.find_element_by_css_selector('#vCampaignRouterContent > div.tabHeadersWithPill > div > a:nth-child(4) > div > span:nth-child(1)') != None:
                try:
                    b = driver.find_element_by_css_selector(
                        '#vCampaignRouterContent > div.tabHeadersWithPill > div > a:nth-child(4) > div > span:nth-child(1)')
                    b.click()
                    time.sleep(2)

                    soup3 = BeautifulSoup(driver.page_source, 'html.parser')

                    if soup3.find("span", {"class": "tabHeadersWithPill-tab-pill t-label--sm"}) != None:
                        project_dict["Number_of_comments"] = driver.find_element_by_xpath(
                            '//*[@id="vCampaignRouterContent"]/div[1]/div/a[4]/div/span[2]').text
                    else:
                        project_dict["Number_of_comments"] = "NaN"

                except NoSuchElementException:
                        project_dict["Number_of_comments"] = "NaN"
        except NoSuchElementException:
            project_dict["Number_of_comments"] = "NaN"


        time.sleep(2)

        #This scrapes the text content of the comments on the project

        try:
            if driver.find_element_by_css_selector('#vCampaignRouterContent > div.tabHeadersWithPill > div > a:nth-child(4) > div > span:nth-child(1)') != None:

                try:
                    c = driver.find_element_by_css_selector(
                        '#vCampaignRouterContent > div.tabHeadersWithPill > div > a:nth-child(4) > div > span:nth-child(1)')
                    c.click()
                    time.sleep(2)

                    soup3 = BeautifulSoup(driver.page_source, 'html.parser')

                    if soup3.find("div", {"class": "routerContentComments"}) != None:
                        project_dict["Project_Comments"] = soup3.find("div", {"class": "routerContentComments"}).text

                    else:
                        project_dict["Project_Comments"] = "NaN"

                except NoSuchElementException:
                    project_dict["Project_Comments"] = ("NaN")

        except NoSuchElementException:
            project_dict["Project_Comments"] = ("NaN")


        time.sleep(2)

        #Selenium access the external link that leads to the profile of the project owner
        #
        try:

            if driver.find_element_by_class_name("tooltipHover-hoverable") != None:
                try:

                    element_to_hover_over = driver.find_element_by_class_name("tooltipHover-hoverable")

                    hover = ActionChains(driver).move_to_element(element_to_hover_over) #Selenium hovers over the link to the project owner's page
                    hover.perform()

                    time.sleep(2)

                    driver.find_element_by_link_text("View full profile").click() #Selenium webdriver clicks on the hoverable link that opens another browser window

                    driver.switch_to.window(driver.window_handles[1]) #moves the code to target new browesr window

                    soup4 = BeautifulSoup(driver.page_source, 'html.parser') # a BeautifulSoup collection that contains the html content of the page

                    time.sleep(2)

                    #Scrapes the name of the project owner

                    if soup4.find("h1", {"class": "i-profileHeader-accountName"}) != None:
                        project_dict["CreatorName"] = soup4.find("h1", {"class": "i-profileHeader-accountName"}).text
                    else:
                        project_dict["CreatorName"] = "NaN"


                    time.sleep(2)

                    # Scrapes the profile of the project owner by using Selenium to navigate to the profile page

                    driver.find_element_by_xpath('/html/body/div[2]/div/div/div[5]/div/span[1]/span/a').click()
                    time.sleep(2)
                    if soup4.find("div", {"class": "col-sm-7"}) != None:
                        project_dict["Creator_Profile"] = soup4.find("div", {"class": "col-sm-7"}).text
                    else:
                        project_dict["Creator_Profile"] = "NaN"

                    if soup4.find("div", {"class": "col-sm-4"}) != None:
                        project_dict["About_Creator"] = soup4.find("div", {"class": "col-sm-4"}).text
                    else:
                        project_dict["About_Creator"] = "NaN"


                    time.sleep(2)


                    #scrapes the links to the website of the project owner
                    driver.find_element_by_xpath('/html/body/div[2]/div/div/div[6]/div/div/div[3]/div[3]/div[2]')
                    soup2 = BeautifulSoup(driver.page_source, 'html.parser')
                    try:
                        for a in soup2.find_all("a", {"rel": "nofollow noopener"}):
                            project_dict["Creator_Urls"] = a['href']
                    except:

                        project_dict["Creator_Urls"] = "NaN"
                except:
                    project_dict["Creator_Urls"] = "NaN"



                # Another way of scraping the name of the project owner and links to the websites of the project owner
        except:
            if soup.find("div", {"class": "campaignTrust-detailsName ng-binding"})!= None:
                project_dict["CreatorName"] = soup.find("div", {"class": "campaignTrust-detailsName ng-binding"}).text

                driver.find_element_by_link_text('More').click()
                time.sleep(2)
                soupA = BeautifulSoup(driver.page_source, 'html.parser')

                try:

                    ULink = soupA.find("a",{"ng-if":"owner.website_url"})

                    project_dict["Creator_Urls"] = ULink['href']
                except:

                    soupb = BeautifulSoup(driver.page_source, 'html.parser')

                    project_dict["Creator_Urls"] = soupb.find("a", {"ng-if": "member.website_url"})

            else:
                project_dict["Creator_Urls"] = "NaN"


        #Data cleaning section
        #the data cleaning function removes escape characters of the scraped data

        def clean_string(var):

            var = str(var)
            var = var.rstrip()
            var = var.replace('\n', '')
            # cleantext = BeautifulSoup(var, "html.parser").text
            # print(cleantext)
            return var
        try:

            project_dict["Name"] = clean_string(project_dict["Name"])
        except:
            pass
        try:
             project_dict["project_Summary"] = clean_string(project_dict["project_Summary"])
        except:
            pass

        try:
            project_dict["Project_Location"] = clean_string(project_dict["Project_Location"])
        except:
            pass
        try:
            project_dict["Project_Backers"] = clean_string(project_dict["Project_Backers"])
        except:
            pass
        try:
            project_dict["Target_Amount"] = clean_string(project_dict["Target_Amount"])
        except:
            pass
        try:
            project_dict["Pledged"] = clean_string(project_dict["Pledged"])
        except:
            pass
        try:
            project_dict["Currency"] = clean_string(project_dict["Currency"])
        except:
            pass
        try:
            project_dict["Days_left"] = clean_string(project_dict["Days_left"])
        except:
                pass
        try:
            project_dict["story"] = clean_string(project_dict["story"])
        except:
            pass
        try:
            project_dict["FAQ"] = clean_string(project_dict["FAQ"])
        except:
            pass
        try:
            project_dict["Number_of_Updates"] = clean_string(project_dict["Number_of_Updates"])
        except:
            pass
        try:
            project_dict["Project_Updates"] = clean_string(project_dict["Project_Updates"])
        except:
            pass
        try:
            project_dict["Number_of_comments"] = clean_string(project_dict["Number_of_comments"])
        except:
            pass
        try:
            project_dict["Project_Comments"] = clean_string(project_dict["Project_Comments"])
        except:
            pass
        try:
            project_dict["CreatorName"] = clean_string(project_dict["CreatorName"])
        except:
            pass
        try:
            project_dict["Creator_Profile"] = clean_string(project_dict["Creator_Profile"])
        except:
            pass
        try:
            project_dict["About_Creator"] = clean_string(project_dict["About_Creator"])
        except:
            pass
        try:
            project_dict["Creator_Urls"] = clean_string(project_dict["Creator_Urls"])
        except:
            pass


        #the scraped data is appended to the empty array data1

        data1.append(project_dict)

        #the scraped data can be stored locally in a json file

        for project in data1:

            with open("indie_data.json", "a") as outfile:
                json.dump(project, outfile)
                outfile.write('\n')

            print(project)


        driver.quit() # Selenium webdriver stops



#This function uploads the links from the random queries of users and starts the web scraping

def getPageDetails():
    with open("indie_query.csv") as url_obj:
        csv_url_reader(url_obj)































