from queue import Queue

import requests
from bs4 import BeautifulSoup

from Crawler.newsMarket.tools import Entity, toMD5, generateDate

outqueue = Queue()

def startParse(url):
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, features='lxml')
    article = Entity()
    article.url = url
    article.postId = toMD5(url)
    article.rid = article.postId
    article.title = soup.find("h1", class_="entry-title").getText()
    article.authorName = soup.find("a", class_="author url fn").getText()
    article.articleDate = generateDate(soup.find("time", class_="entry-date").get("datetime"))
    content = soup.find("div", class_="entry-content")
    for p in content.findAll("p"):
        article.content += p.getText() + "\r\n"
    outqueue.put(article.toList())
    return article



if __name__ == '__main__':
    url = "https://www.newsmarket.com.tw/blog/130223/"
    article = startParse(url)
    for data in article.toList():
        print(data)
        print('---'*40)