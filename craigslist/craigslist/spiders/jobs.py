# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['newyork.craigslist.org']
    # We modified this variable and added the job search page we want to start from
    start_urls = ['https://newyork.craigslist.org/search/egr']

    def parse(self, response):
        #listings = response.xpath('//a[@class="result-title hdrlnk"]/text()').extract()
        #for listing in listings:
            #print(listing)
            #yield {'Listing': listing}

        listings = response.xpath('//li[@class="result-row"]')
        for listing in listings:
            date = listing.xpath('.//*[@class="result-date"]/@datetime').extract_first()
            link = listing.xpath('.//a[@class="result-title hdrlnk"]/@href').extract_first()
            title = listing.xpath('.//a[@class="result-title hdrlnk"]/text()').extract_first()

            yield {
                    'date': date,
                    'link': link,
                    'title': title,
            }

        next_page_url = response.xpath('//*[@class="button next"]/@href').extract_first()

        if next_page_url:
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)
