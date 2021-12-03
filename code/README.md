# Linking Heterogenous Big Data Sources

The methodology employed in this project is to implement the similaity metrics in Information Retrieval field to identify potential text/string matches that exist across heterogenous data sources. By Implementing Apache Solr, with the data sources, the similarity metric can be characteriszed as a join between the relations on textual attributes. Search interface capability is enabled by integrating Apache Solr with ReactJS that retrieves query results and presents them to the user based on documents ranking as specified in Apache Solr.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites and Installations

What things you need to install the software and how to install them

```
1. Webscraping Tools for Kickstarter and Indiegogo
Pycharm : A popular Python IDE for developers developed by JetBrains
Follow the link to download Pycharm; https://www.jetbrains.com/pycharm/

Selenium: Basically developed to automate web browser, Selenium can be implemented with other Python packages for effective webscraping project.
Selenium can be installed with a simple pip command on Terminal; pip install selenium

Selenium Webdriver: Required as an add on that interfaces the browser. 
The webdriver supports the popular web browsers. To download the Selenium webdriver;
Note: The Selenium webdriver must be in path for Selenium to run ed if your path is usr/local/bin

- Chrome: https://sites.google.com/a/chromium.org/chromedriver/downloads

- Firefox: https://github.com/mozilla/geckodriver/releases

- Safari: https://webkit.org/blog/6900/webdriver-support-in-safari-10/

- Edge: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

BeautifulSoup: A Python package for pulling data out of HTML and XML files.
It can be install by a pip command on Terminal: pip install beautifulsoup4

Note: The Python codes for each website must be kept in the same file

2. Recommended Database technology:

MongoDB Community Edition 4.2: A general purpose, document-based, distributed database built for modern application developers.
Download and install MongoDB version 4 using Homebrew on Mac: brew install mongodb-community@4.2

3.Mongo-connector
A generic connection system to integrate MongoDB with Apache Solr in this project.
Mongo-connector can be installed using pip command on Terminal; pip install mongo-connector


4. Apache Solr 8.1.1
Solr is an open-souce enterprise-search platform, written in Java with features such full-text search, faceted serach, database integration.

Follow the link to download and install Apache Sorl on your system;
https://lucene.apache.org/solr/guide/8_1/installing-solr.html

Note: Extract the Solr distribution archive into your home directory on your system


5.ReactJS

React is a JavaScript library for buiding interactive user interfaces. 
To setup a React developement for this project, NodeJS is required for ReactJS.
Follow the link to download and run the package to install it on your system;
https://nodejs.org/en/download/

To install ReactJS, run the following on Terminal; npm install -g create-react-app
This install React globally on your system


```


## Running the application

How to run this application with all the software dependcies installed

1. Integrating MongoDB data with Apache Solr to be Indexed

- Start Apache Solr
Start the Solr sever from Solr directory on your System by typing;
bin/solr start

- Create a Solr Core by a login to Solr Admin Console with this http request;
http://localhost:8983/solr/

The Solr Core Dashboard provides information about the Apache Solr software package installed

-Create a Core by specifying the details of the core you are creating in the dialogue box that appears when you click on the Core Admin in the Admin Daashboard.

Note: The instanceDir and the dataDir of the dialogue box must be filled before a core is created.
        - specify the config section as solrconfig.sml and schema section as schema.xml
        
- Click Add Core to get the specific core created

- The core can be slected and viewed in the Core Selector

- The fields of the MongoDB documents to be indexed must be specified in the schema.xml or managed-schema file. This is done by opening the configuration files and adding the fields to it.
-Note: It is important to add fields ns and _ts together with the fields to be indexed in the schema.xml or managed-schema file as shown below;


<field name="Name" type="string" indexed="true" stored="true"/>
<field name="Name_of_Creator" type="string" indexed="true" stored="true"/>
<field name="Number_of_Comments" type="string" indexed="true" stored="true"/>
<field name="Profile_Link" type="string" indexed="true" stored="true"/>
<field name="Project_Comments" type="string" indexed="true" stored="true"/>
<field name="project_Summary" type="string" indexed="true" stored="true"/>
<field name="Project_link" type="string" indexed="true" stored="true"/>
<field name="_ts" type="long" indexed="true" stored="true" />
<field name="ns" type="string" indexed="true" stored="true"/>

Note: Fields not specified in the schema.xml or managed-schema are not indexed

-Also the request handler for mongo-connector must be specified by adding the line below to the solrconfig.xml file;

<requestHandler name="/admin/luke" class="org.apache.solr.handler.admin.LukeRequestHandler" />

- Also the auto commit must be set to true in the solrconfig.xml file;

<autoCommit>
<maxTime>15000</maxTime>
<openSearcher>true</openSearcher>
</autoCommit>

-restart solr for the configuration to be applied;

bin/solr restart


a. Starting MongoDB Server with replica set. 
Type the followin command at Terminal;

mongod --port 27017 --dbpath /data/db --replSet rs0

b. Start MongoDB Shell and initiate the replica set by typing
mongo
rs.initiate()

c. Starting mongo-connector to connect MongoDB and Apache Solr and index the MongoDB data
Note: MongoDB replica and Solr should be running.

- To start mongo-connector type;
mongo-connector -m <mongodb server hostname>:<replica set port> -t <replication endpoint URL, e.g. http://localhost:8983/solr> -d <name of doc manager, e.g., solr_doc_manager>

d. Querying Apache Solr
Now the the MongoDB data is indexed in Solr, navigate to the; http://localhost:8983/solr/#/<your core name>/query

- A basic text to retrieve the indexed document is to;

set the request handler as  /select and the q as *:*
executing this query will retreieve all the MongoDB data now indexed in Apache Solr.



2. A frontend search interface with ReatJS
  An App.js code integrates the MongoDB data indexed in Apache Solr in a frontend search application that accepts random user queries and formats it to produce results based on keyword matching and document ranking.
  The frontend can accessed by starting npm from the serach-app home directory by typing on Terminal;
  
  npm start 
  
  The frontend search interface can be accessed through the http request; 


## Author

**Boakye Dankwa** 



## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

