from queue import Queue

import requests
from bs4 import BeautifulSoup

from Crawler.pts.tools import Entity, toMD5, generateDate
outqueue = Queue()

def startParse(url):
    try:
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        article = Entity()
        article.url = url
        article.postId = toMD5(url)
        article.rid = article.postId
        main_tag = soup.find("section", class_="wrapper wrapper2")
        article.title = main_tag.find("h2", class_="article-title").getText()
        article.authorName = main_tag.find("div", class_="maintype-wapper hidden-sm hidden-xs").div.getText()
        date_str = main_tag.find("div", class_="maintype-wapper hidden-sm hidden-xs").h2.getText()
        article.articleDate = generateDate(date_str, Chinese=True)
        article.content = main_tag.find("div", class_="article_content").getText()
        outqueue.put(article.toList())
        print("資料採集成功 title = ", article.title)
        return article
    except Exception:
        print("Article 解析失敗, url = ", url)


if __name__ == '__main__':
    url = "https://news.pts.org.tw/article/466193"
    article = startParse(url)
    for data in article.toList():
        print("---"*30)
        print(data)