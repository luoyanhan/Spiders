import requests
import json
import time
import os
import re

BaseUrl_keywords = 'http://www.yidianzixun.com/home/q/news_list_for_keyword'
BaseUrl_channel = 'http://www.yidianzixun.com/home/q/news_list_for_channel'
Par_channel = {'channel_id': 't1121',
           'infinite': 'true',
           'refresh': '1',
           '__from__': 'pc',
           'multi': '5',
           'appid': 'web_yidian'
           }

Headers = {
    'Host': 'www.yidianzixun.com',
    'Referer': 'http://www.yidianzixun.com/channel/w/%E8%A1%97%E6%8B%8D?searchword=%E8%A1%97%E6%8B%8D',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
    }

def get_ChapterList(page):
    print('start page:', page)
    if page == 1:
        par_keyword = {
            'display': '街拍',
            'cstart': '0',
            'cend': '10',
            'word_type': 'token',
            'multi': '5',
            'appid': 'web_yidian',
            '_': ''
        }
        nowtime = int(round(time.time() * 1000))
        par_keyword['_'] = nowtime
        response = requests.get(BaseUrl_keywords, params=par_keyword, headers=Headers)
    else:
        par_channel = Par_channel.copy()
        nowtime = int(round(time.time()*1000))
        par_channel['_'] = nowtime
        cstart = str((page-1)*10)
        cend = str(page*10)
        par_channel['cstart'] = cstart
        par_channel['cend'] = cend
        o = 'sptokent1121'+cstart+cend
        a = ''
        for c in range(len(o)):
            r = 10 ^ ord(o[c])
            a += chr(r)
        par_channel['_spt'] = a
        response = requests.get(BaseUrl_channel, params=par_channel, headers=Headers)

    result = json.loads(response.text)['result']
    for chapter in result:
        Type = chapter.get('content_type', None)
        base = 'http://i1.go2yd.com/image.php?url='
        if Type == 'slides':
            title = chapter.get('title').replace('，', ',').replace(':', '：')
            if not os.path.exists('./download/'+title):
                os.makedirs('./download/'+title)
            gallery_items = chapter.get('gallery_items')
            for image in gallery_items:
                id = image['img']
                img_url = base+id
                response = requests.get(img_url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'})
                with open('./download/'+title+'/'+id+'.jpeg', 'wb') as f:
                    f.write(response.content)
        elif Type == 'news':
            title = chapter.get('title').replace('，', ',').replace(':', '：')
            if not os.path.exists('./download/' + title):
                os.makedirs('./download/' + title)
            itemid = chapter.get('itemid')
            dsource = chapter.get('dsource', None)
            if dsource == '一点资讯':
                news_url = 'http://www.yidianzixun.com/article/{0}?searchword=%E8%A1%97%E6%8B%8D'.format(itemid)
                text = requests.get(news_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'}).text
                docinfo = re.search(r'"image_urls":\[([\s\S]*?)\],"source"', text).group(1)
                img_ids = docinfo.split(',')
                for id in img_ids:
                    id = id.replace('"', '')
                    img_url = base + id
                    response = requests.get(img_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'})
                    with open('./download/'+title+'/'+id+'.jpeg', 'wb') as f:
                        f.write(response.content)
            else:
                print('page:', page)
                print(chapter)
    print('finished page:', page)



if __name__ == "__main__":
    for i in range(1, 11):
        get_ChapterList(i)