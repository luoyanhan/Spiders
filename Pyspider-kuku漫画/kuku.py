from pyspider.libs.base_handler import *
import re
from faker import Faker


class Handler(BaseHandler):
    faker = Faker()
    crawl_config = {
        'itag': 'v1',
        'headers': {
            'User-Agent': faker.user_agent(),
            "Host": "comic.kukudm.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7,es;q=0.6",
            "Accept-Encoding": "gzip, deflate",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        },
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://comic.kukudm.com/index.htm', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        # only crawl the index table(A-Z)
        for each in response.doc('table:nth-of-type(4) a[href^="http://comic.kukudm.com/comictype"]').items():
            self.crawl(each.attr.href, callback=self.comictype_page)

    @config(age=10 * 24 * 60 * 60)
    def comictype_page(self, response):
        for each in response.doc('dd > a').items():
            self.crawl(each.attr.href, callback=self.book_page)

        # next page
        next = response.doc('table:nth-of-type(5) > tr > td:nth-of-type(2) > table').eq(0).find('a').items()
        for n in next:
            if n.text() == '下一页':
                self.crawl(n.attr.href, callback=self.comictype_page)

    @config(age=10 * 24 * 60 * 60)
    def book_page(self, response):
        bname = response.doc('title').text().split('|')[0]
        for each in response.doc('dd > a[href^="http://comic.kukudm.com"]').items():
            self.crawl(each.attr.href, callback=self.detail_page, save={'cname': each.text(), 'bname': bname})

    @config(age=10 * 24 * 60 * 60)
    def detail_page(self, response):
        pattern = re.compile(u'共(\d+)页')
        img_cnt = pattern.search(response.doc('table:nth-of-type(2) tr td[valign="top"]').text()).group()[1:-1]
        pre_url = response.url[:-5]

        for i in range(int(img_cnt)):
            url = pre_url + str(i + 1) + '.htm'
            self.crawl(url, callback=self.image_page, save=response.save)

    @config(priority=2)
    def image_page(self, response):
        pattern_img1 = re.compile('src=\\\'"\+.*?\+"(.*?)\\\'>')
        pattern_img2 = re.compile('src="\+server\+"(.*?)>')

        script = response.text
        url = re.findall(pattern_img1, script)
        if not url:
            url = re.findall(pattern_img2, script)

        img = 'http://n5.1whour.com/' + url[0]

        return {
            "bname": response.save['bname'],
            "cname": response.save['cname'],
            "image_url": img,
        }