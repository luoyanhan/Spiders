import execjs
import requests
import json

key = 'EFBFCB31D5BACE6BB5793A529254424E'
url = 'http://api.bbbbbb.me/yunjx/api.php'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
DATA = {
    'type': 'auto',
    'siteuser': '',
    'hd': '',
    'lg': ''
}

def _get_url(URL):
    ID = URL.split('?')[0]
    with open('./youkuVip.js') as f:
        js = f.read()
    md5_str = execjs.compile(js).call('sign', key)
    DATA['md5'] = md5_str
    DATA['id'] = ID
    print(DATA)
    response = requests.post(url, data=DATA, headers=HEADERS)
    Dict = json.loads(response.text)
    print(Dict['url'])

if __name__ == "__main__":
    # URL = 'https://www.iqiyi.com/v_19rrjr2whg.html'
    # _get_url(URL)
    response = requests.get('https://yun.zxziyuan-yun.com/20180114/15E3eMU9/800kb/hls/jzaUu78376000.ts', headers=HEADERS)
    with open('./video.ts', 'wb') as f:
        for chunk in response.iter_content(chunk_size=10240):
            f.write(chunk)
            f.flush()
    print('finished')

