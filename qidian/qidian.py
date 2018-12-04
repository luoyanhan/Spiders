import requests
import json
from bs4 import BeautifulSoup

HEADERS = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
'Host':'www.qidian.com'
}

books = []

def getList(page):
    url = 'https://www.qidian.com/all?chanId=9&subCateId=251&orderId=&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0&page='+str(page)
    response = requests.get(url, headers=HEADERS)
    token = response.headers['set-cookie'].split(';')[0].split('=')[1]
    soup = BeautifulSoup(response.text, 'lxml')
    string = str(soup.prettify())
    soup2 = BeautifulSoup(string, 'lxml')
    ul = soup2.find('ul', attrs={'class': 'all-img-list'}).find_all('li')

    for li in ul:
        a = li.find('h4').find('a')
        link = 'https:'+a['href']
        name = a.string.strip()
        author = li.find('a', attrs={'class': 'name'}).string.strip()
        ID = link.split('/')[-1]
        score_url = 'https://book.qidian.com/ajax/comment/index'
        Json = json.loads(requests.get(score_url, headers=HEADERS, params={'_csrfToken': token, 'bookId': ID, 'pageSize': '15'}).text)
        score = Json['data']['rate']
        result = (name, author, link, score)
        books.append(result)

if __name__ == "__main__":
    for i in range(1, 3):
        getList(i)
    books = list(set(books))
    result = sorted(books, key=lambda book: float(book[3]), reverse=True)
    for i in result:
        print(i)
    link = ''
    headers = HEADERS.copy()
    headers['Host'] = 'book.qidian.com'
    while 1:
        link = input('用link找简介：')
        link = link.replace("'", '')
        if link != 'z' and link != 'Z':
            detail = str(BeautifulSoup(requests.get(link, headers=headers).text, 'lxml').prettify())
            intro = BeautifulSoup(detail, 'lxml').find('div', attrs={'class': 'book-intro'}).find('p').get_text()
            print(intro)
        else:
            break


