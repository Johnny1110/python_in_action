from queue import Queue

import requests
from bs4 import BeautifulSoup

from Crawler.gvm.tools import Entity, extractPostDate, toMD5
outqueue = Queue()

def startParse(url):
    resp = requests.get(url)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, features='lxml')
    article = Entity()
    article.url = url
    main_tag = soup.find("article", class_="pc-bigArticle")
    article.title = main_tag.find("h1").text.strip()
    article.authorName = main_tag.find("div", class_="pc-bigArticle").text.strip()
    article.articleDate = extractPostDate(main_tag.find("div", class_="article-time").text.strip())
    article.content = main_tag.find("section", class_="article-content").text.strip()
    article.postId = toMD5(url)
    article.rid = article.postId
    outqueue.put(article.toList())
    return article


if __name__ == '__main__':
    url = "https://www.gvm.com.tw/article/71976"
    article = startParse(url)
    print(article.toList())
