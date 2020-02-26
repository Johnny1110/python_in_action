from queue import Queue

import requests
from bs4 import BeautifulSoup

from Crawler.appleDaily.realtime.refactor.tools import getNeededJsonData, Entity, excludeIframeCode, extractAuthor, \
    toMD5, generateDate, session

outqueue = Queue()


def parseArticleAsOldVersion(url, text):
    soup = BeautifulSoup(text, features='lxml')
    article = Entity()
    article.url = url
    article.title = soup.find("hgroup").h1.text
    content = soup.find("div", {"class": "ndArticle_margin"})
    for p in content.findAll("p"):
        article.content += p.getText() + "\r\n"
    article.authorName = extractAuthor(article.content)
    article.articleDate = generateDate(soup.find("hgroup").div.text.split("出版時間：")[1])
    article.postId = toMD5(url)
    article.rid = article.postId
    outqueue.put(article.toList())
    return article


def startParse(url):
    try:
        resp = session.get(url)
        resp.encoding = "utf-8"
        contentJson = getNeededJsonData(resp.text)

        if contentJson is None:
            article = parseArticleAsOldVersion(url, resp.text)
            print("寫入文章 : <{}>".format(article.title))
            return article

        article = Entity()
        article.title = contentJson["headlines"]["basic"]
        article.url = url
        for data in contentJson["content_elements"]:
            try:
                article.content += excludeIframeCode(data['content'])
            except Exception:
                continue
        article.authorName = extractAuthor(article.content)
        article.articleDate = generateDate(contentJson["last_updated_date"])
        article.postId = toMD5(url)
        article.rid = article.postId
        print("寫入文章 : <{}>".format(article.title))
        outqueue.put(article.toList())
        return article
    except Exception as ex:
        print("解析失敗 url : ", url)
        raise ex


if __name__ == '__main__':
    url = " https://tw.appledaily.com/finance/realtime/20200226/1709784/"
    article = startParse(url)
    for data in article.toList():
        print(data)
        print('---'*40)
