import requests
import re
import json
import execjs

URL = 'https://fanyi.baidu.com/?aldtype=16047#zh/en/'
TRANSLATE_API = 'https://fanyi.baidu.com/v2transapi'
REALTRANSLATE_API = 'https://fanyi.baidu.com/transapi'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'fanyi.baidu.com',
    'Origin': 'https://fanyi.baidu.com',
    'Referer': 'https://fanyi.baidu.com/',
    'X-Requested-With': 'XMLHttpRequest',
}

HEADERS2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0', 'Accept': '*/*', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Connection': 'keep-alive', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Host': 'fanyi.baidu.com', 'Origin': 'https://fanyi.baidu.com', 'Referer': 'https://fanyi.baidu.com/', 'X-Requested-With': 'XMLHttpRequest', 'Cookie': 'BAIDUID=BEA2658FC962DF6CA0C053E5690C1934:FG=1; locale=zh; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1540531940; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1540531984; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D'}


Cookie = 'REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1540531940; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1540531984; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D'

class fanYi:
    def __init__(self):
        self._session = requests.session()
        self._data = {
            'from': 'zh',
            'to': 'en',
            'query': '',
            'transtype': 'realtime',
            'simple_means_flag': '3',
            'sign': '',
            'token': ''
        }

    def _set_words(self, words):
        self._words = words

    def _get_token(self):
        response = self._session.get(URL, headers=HEADERS2)
        html = response.text
        li = re.search(r"<script>\s*window\[\'common\'\] = ([\s\S]*?)</script>", html)
        token = re.search(r"token: \'([a-zA-Z0-9]+)\',", li.group(1))
        self._data['token'] = token.group(1)

    def _get_sign(self):
        with open('baidufanyi.js') as f:
            js = f.read()
        sign = execjs.compile(js).call('e', self._words)
        self._data['sign'] = sign

    def _translate(self):
        self._get_token()
        self._get_sign()
        self._data['query'] = self._words
        # string = ''
        # cookie = self._session.cookies.get_dict()
        # for key in cookie:
        #     string += key + '=' + cookie[key] + '; '
        # # response = self._session.post(REALTRANSLATE_API, data=self._data, headers=HEADERS)
        # HEADERS['Cookie'] = string + Cookie
        # print(HEADERS)
        response = self._session.post(TRANSLATE_API, data=self._data, headers=HEADERS2)
        Dict = json.loads(response.content.decode('utf-8'))
        print(Dict['trans_result']['data'][0]['dst'])


if __name__ == "__main__":
    fanyi = fanYi()
    fanyi._set_words('中国')
    fanyi._translate()





