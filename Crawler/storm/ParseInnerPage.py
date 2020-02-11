from queue import Queue

import requests
from bs4 import BeautifulSoup

from Crawler.storm.GetCrawablePage import outqueue as url_queue, startCraw
from Crawler.storm.tools import Entity, extractPostDate, toMD5

site = "test_site_id"
outqueue = Queue()

def startParse(url):
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, features="lxml")
    article = parseArticle(url, soup.find("div", class_="page_wrapper"))
    return article



def parseArticle(url, contentSoup):
    article = Entity()
    article.url = url
    article.authorName = contentSoup.find("a", class_="link_author info_inner_content").text
    article.title = contentSoup.find("h1", id="article_title").text
    article.content = contentSoup.find("div", id="CMS_wrapper").text
    article.articleDate = extractPostDate(contentSoup.find("span", id="info_time").text)
    article.postId = toMD5(url)
    article.rid = article.postId
    outqueue.put(article.toList())
    return article


if __name__ == '__main__':
    startCraw()
    while True:
        try:
            urls = url_queue.get(block=False)
            for url in urls:
                startParse(url)
        except Exception as e:
            break

    while True:
        try:
            data = outqueue.get(block=False)
            print("---"*30)
            for item in data:
                print(item)
        except Exception:
            break




