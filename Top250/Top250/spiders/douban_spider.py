import scrapy
from bs4 import BeautifulSoup
from Top250.items import Top250Item

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    start_urls = ['https://movie.douban.com/top250']
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    baseurl = 'https://movie.douban.com/top250'

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        infos = soup.find_all('div', attrs={'class': 'info'})
        for info in infos:
            item = Top250Item()
            spans = info.find('div', attrs={'class': 'hd'}).find('a').find_all('span')
            name = ''
            for span in spans:
                name += span.text
            item['name'] = name
            bd = info.find('div', attrs={'class': 'bd'})
            detail = bd.find('p', attrs={'class': ''}).text
            item['detail'] = detail
            inq = bd.find('p', attrs={'class': 'quote'}).find('span').text
            item['inq'] = inq
            print(item['name'], item['detail'], item['inq'])
        li = soup.find('div', attrs={'class': 'paginator'}).find_all('a')
        for a in li[:-1]:
            url = self.baseurl + a.get('href')
            yield scrapy.Request(url, headers=self.headers, callback=self.eachpage)

        # return item

    def eachpage(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        infos = soup.find_all('div', attrs={'class': 'info'})
        for info in infos:
            item = Top250Item()
            spans = info.find('div', attrs={'class': 'hd'}).find('a').find_all('span')
            name = ''
            for span in spans:
                name += span.text
            item['name'] = name
            bd = info.find('div', attrs={'class': 'bd'})
            detail = bd.find('p', attrs={'class': ''}).text
            item['detail'] = detail
            inq = bd.find('p', attrs={'class': 'quote'}).find('span').text
            item['inq'] = inq
            print(item['name'], item['detail'], item['inq'])
        # return item