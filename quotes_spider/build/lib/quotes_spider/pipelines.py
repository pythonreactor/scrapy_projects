# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class QuotesSpiderPipeline(object):
    def process_item(self, item, spider):
        if item['h1_tag']:
            item['h1_tag'] = item['h1_tag'][0].upper()  # We must slice here because we are using upper for a list
        return item
