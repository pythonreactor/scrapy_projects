# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    # CrawlSpider has a reserver variable called rules. This will set rules, clearly.
    # This will also be a tuple
    # LinkExtractor will grab all of the URLs for us
    # We also need to callback to our upcoming parse function
    # `parse` is reserved for the base scrapy spider (scrapy.Spider)
    # We must also add `follow`, a bool variable to follow URLs. It will follow the next page
    # and continue collecting all subsequent URLs. Never collection the same URL twice
    # If set to false, it will only scrape the first page
    rules = (Rule(LinkExtractor(), callback='parse_page', follow=False),)

    def parse_page(self, response):
        yield {'URL': response.url}
