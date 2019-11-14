# -*- coding: utf-8 -*-
import scrapy


class TableSpider(scrapy.Spider):
    name = 'table'
    allowed_domains = ['en.wikipedia.org']
    #start_urls = ['http://en.wikipedia.org/']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population']

    def parse(self, response):
        table = response.xpath('//table[contains(@class, "wikitable sortable")]')[0]
        table_rows = table.xpath('.//tr')[1:]

        for row in table_rows:
            rank = row.xpath('.//td[1]/text()').extract_first().strip()
            city = row.xpath('.//td[2]//text()').extract_first()
            state = row.xpath('.//*[@class="flagicon"]/following-sibling::a/text()').extract_first()
            state = row.xpath('.//*[@class="flagicon"]/following-sibling::a/text()|'
                           './/*[@class="flagicon"]/following-sibling::text()').extract_first().strip()

            # Now we can yield the data
            yield {
                 'rank': rank,
                 'city': city,
                 'state': state,
             }
