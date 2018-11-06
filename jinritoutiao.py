import requests
import re
import os
import time
import json
import traceback
from bs4 import BeautifulSoup


class Toutiao:
    def __init__(self, keyword, page_num=None):
        self.headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
        }
        self.baseurl = 'https://www.toutiao.com/search_content/?'
        self.data = {
            'offset': 0,
            'format': 'json',
            'keyword': keyword,
            'autoload': 'true',
            'count': '20',
            'cur_tab': '1',
            'from':'search_tab',
        }
        self.page_num = page_num

    def get_chapters(self, page):
        chapters = []
        self.data['offset'] = 20*(page-1)
        response = requests.get(self.baseurl, headers=self.headers, params=self.data).json()
        if len(response['data']) > 0:
            for i in response['data']:
                if 'open_url' in i:
                    title = i['title']
                    has_image = i['has_image']
                    has_gallery = i['has_gallery']
                    has_video = i['has_video']
                    id = i['id']
                    url = 'https://www.toutiao.com/a'+id+'/'
                    chapters.append((url, title, has_image, has_gallery, has_video))
            return chapters
        else:
            print('finished')
            return None

    def no_gallery(self, url, title):
        try:
            response = requests.get(url, headers=self.headers)
            text = re.search(r'articleInfo: {[\s\S]*?(content: [\s\S]*?)groupId:', response.text).group(1)
            img_li = re.findall(r'img src&#x3D;&quot;([\s\S]*?)&quot;', text)
            if not os.path.exists('./toutiao_imgs/' + title):
                os.makedirs('./toutiao_imgs/' + title)
            for img in img_li:
                name = img.split('/')[-1]
                response = requests.get(img, headers=self.headers)
                with open('./toutiao_imgs/' + title + '/' + str(name) + '.jpg', 'wb') as f:
                    for chunk in response.iter_content(chunk_size=2048):
                        f.write(chunk)
            print(title + ' finished')
        except Exception:
            print(url, title)
            print(traceback.format_exc())

    def has_gallery(self, url, title):
        try:
            response = requests.get(url, headers=self.headers)
            text = re.search(r'gallery: JSON.parse\(([\s\S]*?)\)', response.text).group(1)
            # img_li = re.findall(r'"uri\\":\\"([\s\S]*?)",\\"height', text)
            # print(len(img_li))
            text = json.loads(json.loads(text))
            if not os.path.exists('./toutiao_imgs/' + title):
                os.makedirs('./toutiao_imgs/' + title)
            for i in text['sub_images']:
                img = i['url']
                name = img.split('/')[-1]
                response = requests.get(img, headers=self.headers)
                with open('./toutiao_imgs/' + title + '/' + str(name) + '.jpg', 'wb') as f:
                    for chunk in response.iter_content(chunk_size=2048):
                        f.write(chunk)
            print(title + ' finished')
        except Exception:
            print(url, title)
            print(traceback.format_exc())

    def download(self):
        if not self.page_num:
            pass
        else:
            for i in range(1, self.page_num+1):
                chapters = self.get_chapters(i)
                for chapter in chapters:
                    if chapter[2] == True and chapter[3] == False and chapter[4] == False:
                        self.no_gallery(chapter[0], chapter[1])
                        time.sleep(1)
                    elif chapter[2] == True and chapter[3] == True and chapter[4] == False:
                        self.has_gallery(chapter[0], chapter[1])
                        time.sleep(1)


if __name__ == "__main__":
    toutiao = Toutiao('chinajoy', 2)
    toutiao.download()
