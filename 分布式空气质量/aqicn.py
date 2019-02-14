from celery import Celery
from bs4 import BeautifulSoup
import re
import time

import ohRequests as requests

app = Celery('aqicn', broker='redis://:''@66.42.116.42/2', backend='redis://:''@66.42.116.42:6379/3')


@app.task
def crawl(location, url):
    req = requests.ohRequests()
    content = req.get(url)

    pattern = re.compile('<table class=\'api\'(.*?)</table>', re.S)
    data = pattern.findall(content)

    if data:
        data = "<table class='api' {} </table>".format(data[0])
    soup = BeautifulSoup(data, 'lxml')

    aqi = soup.find(id='aqiwgtvalue').text

    if aqi == '-':
        return None

    t = soup.find(id='aqiwgtutime').get('val')

    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(t)))

    return [location, aqi, t]