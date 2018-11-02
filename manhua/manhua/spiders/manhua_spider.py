import scrapy
import re
import os
import requests
from manhua.items import ManhuaItem

class ManhuaSpider(scrapy.Spider):
    name = 'manhua'
    start_urls = ['http://comic.kukudm.com/comiclist/2504/index.htm']
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    baseurl = 'http://comic.kukudm.com'
    basepath = '../manhuaDownload/'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        li = response.xpath('//dl[@id="comiclistn"]/dd/a[1]').extract()
        for i in li:
            result = re.search(r'<a href="([\s\S]*?)" target="_blank">([\s\S]*?)</a>', i)
            href = result.group(1)
            name = result.group(2)
            new_url = self.baseurl+href
            floder_name = self.basepath+name
            yield scrapy.Request(new_url, headers=self.headers, callback=self.get_chapterurls, meta={'new_url': new_url, 'floder_name': floder_name})

    def get_chapterurls(self, response):
        result = response.xpath('//td[@align="center"]/text()').extract()
        text = result[2]
        result = re.search(r'共(\d+)页', text)
        name = result.group(0)
        maxnum = result.group(1)
        floder_name = response.meta['floder_name'] + ' ' + name

        item = ManhuaItem()
        result2 = response.xpath('//script/text()').extract()
        href = re.search(r'<IMG SRC=[\s\S]*?(newkuku[\s\S]*?.jpg)\'>', result2[0])
        jpg_url = 'http://n5.1whour.com/' + href.group(1)
        filename = floder_name + '/' + '1.jpg'
        item['url'] = jpg_url
        item['floder_name'] = floder_name
        item['filename'] = filename
        yield item


        for i in range(1, int(maxnum)+1):
            photo_url = response.meta['new_url'].replace(r'1.htm', str(i)+'.htm')
            yield scrapy.Request(photo_url, headers=self.headers, callback=self.get_link, meta={'floder_name': floder_name, 'url': photo_url}, dont_filter=True)

    def get_link(self, response):
        item = ManhuaItem()
        result = response.xpath('//script/text()').extract()
        href = re.search(r'<IMG SRC=[\s\S]*?(newkuku[\s\S]*?.jpg)\'>', result[0])
        jpg_url = 'http://n5.1whour.com/'+href.group(1)
        floder_name = response.meta['floder_name']
        page = re.search(r'/(\d+).htm', response.meta['url']).group(1)
        filename = floder_name + '/' + page + '.jpg'

        item['url'] = jpg_url
        item['floder_name'] = floder_name
        item['filename'] = filename
        yield item

        # response = requests.get(jpg_url, headers=self.headers)
        # with open(filename, 'wb') as f:
        #     for chunk in response.iter_content(chunk_size=2048):
        #         if not chunk:
        #             break
        #         f.write(chunk)

