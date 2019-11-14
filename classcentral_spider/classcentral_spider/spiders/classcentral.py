# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request


class ClasscentralSpider(Spider):
    name = 'classcentral'
    allowed_domains = ['classcentral.com']
    start_urls = ['http://classcentral.com/subjects']

    # This is an initializer so we can pass an argument to the script to choose the
    # subject we want to scrape
    def __init__(self, subject=None):
        self.subject = subject

    def parse(self, response):
        if self.subject:
            subject_url = response.xpath('//a[contains(@title, "' + self.subject + '")]/@href').extract_first()
            absolute_subject_url = response.urljoin(subject_url)  # Create an absolute URL
            yield Request(absolute_subject_url,
                          callback=self.parse_subject)

        else:
            self.log('Scraping all subjects.')
            # Grab ALL subjects
            subjects = response.xpath('//h3/a[1]/@href').extract()
            # Create absolute URL for each URL and pass to the next function
            for subject in subjects:
                absolute_subject_url = response.urljoin(subject)
                # Yield the URL callback to the parsing function
                yield Request(absolute_subject_url,
                              callback=self.parse_subject)

    
    def parse_subject(self, response):
        subject_name = response.xpath('//h1/text()').extract_first()

        courses = response.xpath('//tr[@itemtype="http://schema.org/Event"]')
        # Iterate over the courses
        for course in courses:
            course_name = course.xpath('.//span[@class="course-name-text text-1 weight-semi line-tight"]/text()').extract_first()
            course_url = course.xpath('.//a[@title="' + course_name + '"]/@href').extract_first()
            # Join the original URL with the course's direct URL
            absolute_course_url = response.urljoin(course_url)
            
            # Yield the course data
            yield {
                'subject_name': subject_name,
                'course_name': course_name,
                'absolute_course_url': absolute_course_url,
            }

        # Next page iteration
        next_page = response.xpath('.//link[@rel="next"]/@href').extract_first()
        if next_page:
            absolute_next_page = response.urljoin(next_page)
            
            # Reiterate over the next page
            yield Request(absolute_next_page,
                          callback=self.parse_subject)
