# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request


class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']


    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(absolute_url, callback=self.parse_book)

        # Process next page
        next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield Request(absolute_next_page_url)    
        

    def parse_book(self, response):
        pass

























# Scraping books using selenium

#from time import sleep
#from scrapy import Spider
#from selenium import webdriver
#from scrapy.selector import Selector
#from scrapy.http import Request
#from selenium.common.exceptions import NoSuchElementException


#class BooksSpider(Spider):
#    name = 'books'
#    allowed_domains = ['books.toscrape.com']

    # start_requests is a reserved function, it must return a response to the URL
#    def start_requests(self):
        # Load the chrome driver
#        self.driver = webdriver.Chrome('chromedriver')
#        self.driver.get('http://books.toscrape.com')
        
        # Set the selector as the source code of the page we are scraping
        #sel = Selector(text=self.driver.page_source)
        # Grab the URL of each book
        #books = sel.xpath('//h3/a/@href').extract()
        # Iterate each book URL and yield the resulting title URLs
        #for book in books:
            #url = 'http://books.toscrape.com/' + book
            #yield Request(url, callback=self.parse_book)

        # We can iterate the pages on this website using a while loop
#        while True:
#            try:
#                next_page = self.driver.find_element_by_xpath('//a[text()="next"]')
                # We want to allow the requests to wait for 3 seconds in order
                # to not try and hit the next page while we are still loading
                # This should avoid potential errors
                # Instead of sleep, we could also use selenium to determine when a specific element
                # on the page is loaded before going to the next page, but this is just an example
#                sleep(3)
#                self.logger.info('Sleeping for 3 seconds.')
                # Click to the next page
#                next_page.click()

                # Set the selector as the source code of the page we are scraping
#                sel = Selector(text=self.driver.page_source)
                # Grab the URL of each book
#                books = sel.xpath('//h3/a/@href').extract()
                # Iterate each book URL and yield the resulting title URLs
#                for book in books:
#                    url = 'http://books.toscrape.com/catalogue/' + book
#                    yield Request(url, callback=self.parse_book)
    
#            except NoSuchElementException:
                # We will let the user know when we have no more pages
#                self.logger.info('No more pages to load.')
                # Once we are done, we will quit the Chrome driver
#                self.driver.quit()
                # Once we quit the driver, we will break out of the while loop
#                break

    # Function for parsing each book URL
#    def parse_book(self, request):
#        pass


# This script will grab the URL for each book on a page.
# Then, it will pass that URL to the `parse_book` function.
# Once the entire page's URLs are done being scraped, it will
# click to the next page and repeat.
# When it is done parsing all of the pages, it will quit
# the browser and clean itself up.
