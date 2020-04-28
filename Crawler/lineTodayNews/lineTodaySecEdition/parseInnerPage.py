import json
import re

from bs4 import BeautifulSoup

from Crawler.lineTodayNews.lineTodaySecEdition.tools_2 import session, Entity, toMD5, generateDate, extractTsecDate


def startParse(url):
    article = parseArticle(url)
    print(article.toMap())
    for comment in parseComments(article):
        print(comment.toMap())


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
    window_categoryId = re.search("window.categoryId = .*?;", str(soup)).group()
    window_articleId = re.search("window.articleId = .*?;", str(soup)).group()
    categoryId = re.search("[0-9]+", window_categoryId).group()
    query_id = re.search("[0-9]+", window_articleId).group()
    article.setAttr("query_id", query_id)

    likeCnt_url = "https://api.today.line.me/webapi/article/dinfo_v2?articleIds={}&categoryId={}&country=TW&likeSize=1&sort=POPULAR&tabIds=1&tabContentSize=20&_=1588040353162".format(
        query_id, categoryId
    )
    likesResp = session.get(likeCnt_url)
    likesResp.encoding = 'utf-8'
    jsonData = likesResp.json()['result']
    article.likescnt = jsonData['likeViews']['count']
    article.replycnt = jsonData['commentCounts']
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
    for cmtData in collectComments(query_id):
        comment = Entity()
        comment.parent = article
        comment.articleDate = extractTsecDate(cmtData['createdDate'])
        comment.authorName = cmtData['displayName']
        comment.postId = toMD5("{}_{}".format(article.postId, cmtData['commentSn']))
        comment.rid = article.postId
        comment.content = cmtData['contents'][0]['extData']['content']
        try:
            comment.likescnt = cmtData['ext']['likeCount']['up']
        except Exception:
            comment.likescnt = "0"
        comment.replycnt = cmtData['ext']['replyCount']
        yield comment


if __name__ == '__main__':
    url = "https://today.line.me/tw/article/qjRoew"
    startParse(url)