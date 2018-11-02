# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import requests
import time
import random


class ManhuaPipeline(object):
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

    def process_item(self, item, spider):
        url = item['url']
        floder_name = item['floder_name']
        filename = item['filename']
        if not os.path.exists(floder_name):
            os.makedirs(floder_name)
        response2 = requests.get(url, headers=self.headers)
        with open(filename, 'wb') as f:
            for chunk in response2.iter_content(chunk_size=2048):
                if not chunk:
                    break
                f.write(chunk)
        print(filename)
        # time.sleep(random.randint(1, 3))
        return item
