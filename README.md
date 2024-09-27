# webscraping-scrapy
This project showcase how to scrape data from magicbricks using scrapy(top level web scraping framework)

## To Create Scrapy Project -

"scrapy start project magicbricks" - Create scrapy project

Enter inside magicbricks folder for further building

"scrapy genspider magicbricks_crawl (url to scrape data from) " - Create spider

Enter inside the magicbricks_crawl.py file and edit the flow using python

## Features of scrapy

Callback - feature to yield the response to the function mentioned.

errback - common feature to handle all the errors.    

yield - generator.

Multiple Restful api methods.

dont_filter - used to filter out the duplicate requests.

meta - pass the data,handle proxies,retries & many more.

Additionaly, most of the features can be handled in settings.py page which helps users to create multiple spider within a scrapy project with default setting of rotating proxies,retires.
