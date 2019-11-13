# -*- coding: utf-8 -*-
import os
import csv
import glob
import pymysql
from scrapy import Spider
from scrapy.http import Request


def product_info(response, value):
    return response.xpath('//th[text()="' + value + '"]/following-sibling::td/text()').extract_first()

class BooksSpider(Spider):
    name = 'mysql'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']

    #def __init__(self, category):
        #self.start_urls = [category]

    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(absolute_url, callback=self.parse_book)

        # Process next page
        #next_page_url = response.xpath('//a[text()="next"]/@href').extract_first()
        #absolute_next_page_url = response.urljoin(next_page_url)
        #yield Request(absolute_next_page_url)    
        

    def parse_book(self, response):
        title = response.css('h1::text').extract_first()
        price = response.xpath('//*[@class="price_color"]/text()').extract_first()

        image_url = response.xpath('//img/@src').extract_first()
        image_url = image_url.replace('../..', 'http://books.toscrape.com')

        rating = response.xpath('//*[contains(@class, "star-rating")]/@class').extract_first()
        rating = rating.replace('star-rating ', '')

        description = response.xpath('//*[@id="product_description"]/following-sibling::p/text()').extract_first()

        # Product information data points
        upc = product_info(response, 'UPC')
        product_type = product_info(response, 'Product Type')
        price_without_tax = product_info(response, 'Price (excl. tax)')
        price_with_tax = product_info(response, 'Price (incl. tax)')
        tax = product_info(response, 'Tax')
        availability = product_info(response, 'Availability')
        number_of_reviews = product_info(response, 'Number of reviews')

        yield {
                'title': title,
                #'price': price,
                #'image_url': image_url,
                'rating': rating,
                #'description': description,
                'upc': upc,
                'product_type': product_type,
                #'price_without_tax': price_without_tax,
                #'price_with_tax': price_with_tax,
                #'tax': tax,
                #'availability': availability,
                #'number_of_reviews': number_of_reviews,
        }


    def close(self, reason):
        # This will find the latest .csv file and rename the file
        # to be the same, with a number attached
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
        #os.rename(csv_file, 'foobar.csv') 
        
        mydb = pymysql.connect(host='localhost',
                           user='root',
                           passwd='',
                           db='books_db')
                           
        cursor = mydb.cursor()  # Adding a cursor to the DB variable
        # Iterate over the CSV data
        with open(csv_file, newline='') as csvfile:
            csv_data = csv.reader(csvfile)

            # We need to create the tables and then insert the data to our DB
            row_count = 0
            for row in csv_data:
                if row_count != 0:
                    # This line will be what writes the data to the DB
                    cursor.execute(
                        'INSERT IGNORE INTO books_table(rating, product_type, upc, title)\
                        VALUES(%s, %s, %s, %s)', row,
                    )

                row_count += 1   
 
        mydb.commit()
        cursor.close()

