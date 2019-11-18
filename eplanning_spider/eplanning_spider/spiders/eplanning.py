# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest


class EplanningSpider(scrapy.Spider):
    name = 'eplanning'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://eplanning.ie/']

    def parse(self, response):
        urls = response.xpath('//a/@href').extract()
        # Iterate over URLs
        for url in urls:
            # Filter out bad URLs
            if url == '#':
               pass
            else:
                yield Request(url, callback=self.parse_application)

    def parse_application(self, response):
        app_url = response.xpath('//*[@class="glyphicon glyphicon-inbox btn-lg"]/following-sibling::a/@href').extract_first()
        
        yield Request(response.urljoin(app_url), callback=self.parse_form)
        
    def parse_form(self, response):
        yield FormRequest.from_response(response,
                                        formdata={'RdoTimeLimit': '42'},
                                        dont_filter=True,
                                        formxpath='(//form)[2]',
                                        callback=self.parse_pages)

    def parse_pages(self, response):
        application_urls = response.xpath('//td/a/@href').extract()
        for url in application_urls:
            # Not an absolute URL so we must join
            url = response.urljoin(url)
            yield Request(url, callback=self.parse_items)
           
        # Once you are done parsing a page, go to the next one and continue parsing
        next_page_url = response.xpath('//*[@rel="next"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield Request(absolute_next_page_url, callback=self.parse_pages)
 
    def parse_items(self, response):
        agent_btn = response.xpath('//*[@value="Agents"]/@style').extract_first()
        # Check if the agent button's style contains the line we are looking for
        if 'display: inline;  visibility: visible;' in agent_btn:
            name = response.xpath('//tr[th="Name :"]/td/text()').extract_first()
            address_first = response.xpath('//tr[th="Name :"]/td/text()').extract()
            address_second = response.xpath('//tr[th="Address :"]/following-sibling::tr/td/text()').extract()[0:3]

            address = address_first + address_second
            phone = response.xpath('//tr[th="Phone :"]/td/text()').extract_first()
            fax = response.xpath('//tr[th="Fax :"]/td/text()').extract_first()
            email = response.xpath('//tr[th="e-mail :"]/td//a/text()').extract_first()
            url = response.url

            yield {
                'address': address,
                'phone': phone,
                'fax': fax,
                'email': email,
                'url': url
            }

        else:
            # If not, pass a log message
            self.logger.info("Agent button not found on page, passing invalid url.")
