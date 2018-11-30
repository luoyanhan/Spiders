import requests
import configure
import random
import ast
import re
import os
import progressbar
import time

def get_playlist_m3u8(vid):
    url = "https://vmobile.douyu.com/video/getInfo?vid={0:s}".format(vid)
    header = {}
    header['user-agent'] = random.choice(configure.FakeUserAgents_mobile)

    try:
        response = requests.get(url, headers=header)
        content = None
        if response.status_code == requests.codes.ok:
            content = response.text

    except Exception as e:
        print(e)

    djson = ast.literal_eval(content)

    if int(djson.get('error')) != 0:
        return None, None

    video_url = ast.literal_eval(content).get('data').get('video_url').replace('\\', '')
    n = len('playlist.m3u8') * (-1)
    domain = video_url.split('?')[0][:n]
    print("playlist.m3u8 file retrieved.")

    try:
        response = requests.get(video_url, headers=header)
        content = None
        if response.status_code == requests.codes.ok:
            content = response.text

    except Exception as e:
        print(e)

    return domain, content

def parser_m3u8(domain, fm3u8):
    fm3u8_list = fm3u8.split('\n')
    res = []

    for url in fm3u8_list:
        url = url.strip()
        if url and not url.startswith('#'):
            res.append(domain+url)

    return res


def download_ts(vid, tss):
    if not os.path.exists("Download"):
        os.makedirs("Download")

    header = {}
    header['user-agent'] = random.choice(configure.FakeUserAgents)

    name_list = []
    print("Parser {0:d} ts files in download list.".format(len(tss)))
    bar = progressbar.ProgressBar(maxval=len(tss)).start()

    for i, ts in enumerate(tss):
        name = "{0:s}_{1:s}".format(vid, re.split('[_?]', ts)[2])
        name_list.append(name)
        content = ''
        try:
            response = requests.get(ts, headers=header)
            content = None
            if response.status_code == requests.codes.ok:
                content = response.content

        except Exception as e:
            print(e)

        with open("Download/" + name, 'wb') as file:
            file.write(content)

        print("Downloaded {0:s}".format(name))
        bar.update(i + 1)
    bar.finish()

    return name_list

cnt = 0


def combine_ts(vid, name1, name2):
    global cnt
    os.system("cd Download & copy /b {0:s}+{1:s} temp{2:d}.ts".format(name1, name2, cnt))
    os.system("cd Download & del {0:s}".format(name1))
    os.system("cd Download & del {0:s}".format(name2))
    cnt += 1
    return ["temp{0:d}.ts".format(cnt - 1)]


def combine(vid, ret):
    if len(ret) == 1:
        return ret

    if len(ret) == 2:
        return combine_ts(vid, ret[0], ret[1])

    return combine(vid, combine(vid, ret[:len(ret) // 2]) + combine(vid, ret[len(ret) // 2:]))

if __name__ == "__main__":
    vid = 'Aox276Nd3no7Vz8Z'
    domain, fm3u8 = get_playlist_m3u8(vid)
    tss = parser_m3u8(domain, fm3u8)
    ret = download_ts(vid, tss)
    lastname = combine(vid, ret)
    os.system("cd Download & rename {0:s} {1:s}.ts".format(lastname[0], vid))