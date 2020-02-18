from queue import Queue

import requests
from bs4 import BeautifulSoup

from Crawler.esFocus.tools import Entity, extractPostDate, extractAuthorName, toMD5

outqueue = Queue()

def startParse(url):
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, features='lxml')
    mainTag = soup.find("section", class_="section")

    article = Entity()
    article.url = url
    article.title = mainTag.find("h1", class_="title").text
    article.articleDate = extractPostDate(mainTag.find("time", class_="datetime").text)
    content = mainTag.findAll("p")
    for p in content:
        article.content += p.text.strip()
    article.authorName = extractAuthorName(article.content)
    article.postId = toMD5(url)
    article.rid = article.postId
    outqueue.put(article.toList())
    return article

if __name__ == '__main__':
    article = startParse("https://www.eventsinfocus.org/news/3555")
    for data in article.toList():
        print(data)
        print("---" * 40)