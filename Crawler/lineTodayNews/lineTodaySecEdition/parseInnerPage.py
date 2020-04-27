import json
import re

from bs4 import BeautifulSoup

from Crawler.lineTodayNews.lineTodaySecEdition.tools_2 import session, Entity, toMD5, generateDate


def startParse(url):
    article = parseArticle(url)
    parseComments(article)


def parseArticle(url):
    resp = session.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, features='lxml')
    jsonScript = soup.find("script", type="application/ld+json")
    jsonData = json.loads(jsonScript.text)
    article = Entity()
    article.url = url
    article.postId = toMD5(url)
    article.rid = article.postId
    article.title = jsonData['headline']
    article.articleDate = generateDate(jsonData['datePublished'])
    article.authorName = jsonData['author']['name']
    article.content = jsonData['articleBody']
    print(article.toMap())
    window_articleId = re.search("window.articleId = .*?;", str(soup)).group()
    query_id = re.search("[0-9]+", window_articleId).group()
    article.setAttr("query_id", query_id)
    return article


def collectComments(query_id, limit=100, pivot=0):
    while True:
        url = "https://api.today.line.me/webapi/comment/list?articleId={}&limit={}&country=TW&replyCount=true&direction=DESC&postType=&sort=POPULAR&pivot={}".format(
            query_id, limit, pivot)
        resp = session.get(url)
        resp.encoding = 'utf-8'
        jsonData = resp.json()
        comments = jsonData['result']['comments']['comments']
        if len(comments) == 0:
            break
        for comment in comments:
            yield comment
        pivot = pivot + 100


def parseComments(article):
    query_id = article.getAttr("query_id")
    print("query_id:", query_id)
    for comment in collectComments(query_id):
        print(comment)

if __name__ == '__main__':
    url = "https://today.line.me/tw/article/wyKELr"
    startParse(url)