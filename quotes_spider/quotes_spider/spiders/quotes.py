# -*- coding: utf-8 -*-
import scrapy

# Test
class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    # Default callback method in spiders
    def parse(self, response):
        quotes = response.xpath('//*[@class="quote"]')
        for quote in quotes:
            text = quote.xpath('.//*[@class="text"]/text()').extract_first()
            author = quote.xpath('.//*[@class="author"]/text()').extract_first()
            tags = quote.xpath('.//*[@class="keywords"]/@content').extract_first()
            
            yield{'Text': text,
                  'Author': author,
                  'Tags': tags}

        # Crawling pages
        next_page_url = response.xpath('//*[@class="next"]/a/@href').extract_first()
        # This line joins together the url we are crawling, and the next page url reference
        absolute_next_page_url = response.urljoin(next_page_url)
        yield scrapy.Request(absolute_next_page_url)  # If this wasn't in the parse function, we would need a callback function
