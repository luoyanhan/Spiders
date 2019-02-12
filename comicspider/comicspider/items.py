# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html



import scrapy

class ComicspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # 文件名，章节名
    dir_name = scrapy.Field()
    # 每个章节名每一页的链接
    link_url = scrapy.Field()
    # 图片链接
    img_url = scrapy.Field()
    # 图片保存路径
    image_paths = scrapy.Field()
