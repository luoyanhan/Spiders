import scrapy
import re
from scrapy import Selector
from scrapy_redis.spiders import RedisSpider
from comicspider.items import ComicspiderItem


class comicCrawler(RedisSpider):
#class comicCrawler(scrapy.Spider):
    name = "comicCrawler"

    redis_key='comicCrawler:start_urls'

    server_img = 'http://n5.1whour.com/'
    server_link = 'http://comic.kukudm.com'

    start_urls = ['http://comic.kukudm.com/index.htm']
    num = 1


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.index_page)

    def index_page(self, response):
        # only crawl the index table(A-Z)
        hxs = Selector(response)
        urls = hxs.xpath('//table[4]//a/@href').extract()
        for url in urls:
            yield scrapy.Request(url=self.server_link + url, callback=self.comictype_page)

    def comictype_page(self, response):
        hxs = Selector(response)
        urls = hxs.xpath('//dd/a//@href').extract()
        #print (urls)
        for url in urls:
            yield scrapy.Request(url=self.server_link + url, callback=self.book_page)

        nexts = hxs.xpath('//table[5]//tr//td[2]//table[1]//a[text()="下一页"]/@href').extract()
        for n in nexts:
            yield scrapy.Request(url=self.server_link + url, callback=self.comictype_page)


    def book_page(self, response):
        hxs = Selector(response)
        items = []

        urls = hxs.xpath('//dd/a[1]/@href').extract()
        dir_names = hxs.xpath('//dd/a[1]/text()').extract()

        for index in range(len(urls)):
            item = ComicspiderItem()
            item['link_url'] = self.server_link + urls[index]
            item['dir_name'] = dir_names[index]
            items.append(item)

        for item in items:
            yield scrapy.Request(url=item['link_url'], meta={'item': item}, callback=self.detail_page)

    def detail_page(self, response):
        item = response.meta['item']
        item['link_url'] = response.url
        hxs = Selector(response)

        page_num = hxs.xpath('//td[@valign="top"]/text()').re(u'共(\d+)页')[0]
        pre_link = item['link_url'][:-5]
        for i in range(int(page_num)):
            new_link = pre_link + str(i+1) + '.htm'
            yield scrapy.Request(url=new_link, meta={'item': item}, callback=self.image_page)

    def image_page(self, response):
        item = response.meta['item']
        item['link_url'] = response.url
        hxs = Selector(response)

        pattern_img1 = re.compile('src=\\\'"\+.*?\+"(.*?)\\\'>')
        pattern_img2 = re.compile('src="\+server\+"(.*?)>')
        script = response.text

        url = re.findall(pattern_img1, script)
        if not url:
            url = re.findall(pattern_img2, script)

        pre_img_url = hxs.xpath('//script/text()').extract()
        img_url = self.server_img + url[0]
        item['img_url'] = img_url
        print(self.num)
        self.num += 1
        yield item