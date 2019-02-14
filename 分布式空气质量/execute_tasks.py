from aqicn import crawl

URLS = []


def readurls():
    with open("urls.txt", 'r') as file:
        while True:
            item = file.readline()

            if not item:
                break

            data = item.split(',')
            location, url = data[0], data[1]
            URLS.append((location, url.replace('\n', '')))


def task_manager():
    for url in URLS:
        crawl.delay(url[0], url[1])
        # app.send_task('aqicn.crawl', args=(url[0],url[1],))


if __name__ == '__main__':
    readurls()
    task_manager()