from queue import Queue

import requests
from bs4 import BeautifulSoup

from Crawler.formosa.tools import Entity, toMD5, generateDate
outqueue = Queue()


def startParse(url, html):
    soup = BeautifulSoup(html, features='lxml')
    main_content = soup.find("div", class_="content")
    article = Entity()
    article.url = url
    article.postId = toMD5(url)
    article.rid = article.postId
    article.title = main_content.find("h1").getText()
    article.articleDate = generateDate(main_content.find("small", class_="date").getText().strip())
    article.content = main_content.find("div", class_="body").getText().strip()
    article.authorName = main_content.find("article").h4.getText()
    if len(article.authorName) > 100:
        article.authorName = "?"     
    outqueue.put(article.toList())
    return article


if __name__ == '__main__':
    url = "http://www.my-formosa.com/DOC_154350.htm"
    article = startParse(url)
    for data in article.toList():
        print(data)
        print("---"*40)