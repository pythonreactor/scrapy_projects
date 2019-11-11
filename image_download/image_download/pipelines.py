# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os

class ImageDownloadPipeline(object):
    def process_item(self, item, spider):
        os.chdir('/Users/Michael/projects/scrapy_projects/image_download/foobar')
        
        # We need to verify the image path exists and then we can change the name
        # To do this, we will do this:
        if item['images'][0]['path']:  # item is a dict., image key holds a list of dicts.
            new_image_name = item['title'][0] + '.jpg'  # Change image name to title
            new_image_path = 'full/' + new_image_name
            
            os.rename(item['images'][0]['path'], new_image_path)
