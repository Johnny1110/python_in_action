from queue import Queue

import requests
from bs4 import BeautifulSoup

from Crawler.commonWealth.tools import Entity, toMD5, extractPostDate
outqueue = Queue()

def startParse(url):
    parseArticle(url)

def parseArticle(url):
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, features='lxml')
    article = Entity()
    article.url = url
    article.title = soup.find("title").text
    article.postId = toMD5(article.url)
    article.rid = article.postId
    authorName = soup.find("li", class_="authorName").a
    article.authorName = authorName.text if authorName is not None else "?"
    content = soup.find("section", class_="nevin")
    article.articleDate = extractPostDate(content.find("time").text)
    for p in content.findAll("p"):
        article.content += p.text.strip()
    outqueue.put(article.toList())


if __name__ == '__main__':
    parseArticle("https://www.cw.com.tw/article/article.action?id=5098812")