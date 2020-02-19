from queue import Queue

import requests
from bs4 import BeautifulSoup

from Crawler.businessToday.tools import Entity, toMD5, extractPostDate
outqueue = Queue()

def startParse(url):
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, features='lxml')
    article = Entity()
    article.url = url
    article.postId = toMD5(url)
    article.rid = article.postId
    main_tag = soup.find("div", class_="container")
    article.title = main_tag.find("h1", class_="article__maintitle").text.strip()
    article.articleDate = extractPostDate(main_tag.find("p", class_="context__info-item context__info-item--date").text.strip(), inner=True)
    article.authorName = main_tag.find("p", class_="context__info-item context__info-item--author").text.strip()
    article.content = main_tag.find("div", {"itemprop": "articleBody"}).text.strip()
    outqueue.put(article.toList())
    return article

if __name__ == '__main__':
    url = "https://www.businesstoday.com.tw/article/category/80392/post/202002190045/武漢肺炎衝擊台灣經濟！蘇內閣「48小時拍板600億銀彈」搶救3大產業備戰實錄"
    article = startParse(url)
    for data in article.toList():
        print(data)
        print("---"*40)