import urllib
from queue import Queue, Empty

import getCrawlablePage
import requests
import json
import urllib.parse as parse

from bs4 import BeautifulSoup
import datetime

site = "3b9c6ee9f098367f9d7be49c5bdc007b"

outqueue = Queue()

def startParse(classId, postId, url):
    resp = requests.get(url)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, features="html.parser")
    try:
        parseArticle(classId, postId, url, soup)  # 解析主文
    except Exception as e:
        print(url, "非正常文章，無法爬取")



# 爬主文
def parseArticle(classId, postId, url, soup):
    article = Entity()  # 資料封裝

    ### 取得留言json ###
    commentsAPI = generateArticleCommonsAPI(postId, categoryId=classId)
    resp = requests.get(commentsAPI)
    resp.encoding = "utf-8"
    commentAndLikes = json.loads(resp.text)['result']['commentLikes'][0]
    likeViews = commentAndLikes['likeViews']
    commentViews = commentAndLikes['commentViews']
    ### 取得留言json ###
    article.likescnt = likeViews['count']
    article.dislikescnt = 0
    article.replycnt = commentViews['count']
    article.pageUrl = url
    article.postTitle = soup.select_one("h2", {"class": "news-title"}).text.strip()
    try:
        article.authorName = soup.select("dd.name")[0].text.strip()
    except Exception:
        article.authorName = soup.select("dd.publisher")[0].text.strip()
    article.authorName = " "
    article.articleDate = extarctDate(soup.select("dd.date")[0].text.strip())
    article.content = str()
    articleArea = soup.find("article", {"class": "article-content news-content"})  # 提出 article area
    articleArea = articleArea.select("p")  # 提出所有的段落<p>
    for p in articleArea:
        article.content = article.content + str(p.text + "\t \n")
    article.postId = postId
    article.site = site
    article.rid = article.postId
    article.pid = ""
    article.classId = classId
    outqueue.put(article.toList())

    parseComments(article)  # 解析留言 param 需傳入主文物件



def parseReply(comment):
    replyAPI = generateCommonsReplysAPI(comment.parent.postId, comment.replycnt, comment.commentSn)
    resp = requests.get(replyAPI)
    resp.encoding = "utf-8"
    replyJson = json.loads(resp.text)['result']['comments']['comments']
    for i in range(len(replyJson)):
        repData = replyJson[i]
        reply = Entity()
        reply.parent = comment
        reply.pageUrl = comment.pageUrl
        reply.postTitle = comment.postTitle
        reply.authorName = repData['displayName']
        reply.articleDate = msTransToDate(repData['createdDate'])
        reply.content = repData['contents'][0]['extData']['content']
        reply.postId = comment.postId + "_" + str(i+1)
        reply.site = site

        reply.rid = reply.parent.postId
        reply.pid = reply.parent.parent.postId

        reply.likescnt = 0
        reply.dislikescnt = 0
        reply.replycnt = 0

        outqueue.put(reply.toList())



def parseComments(article):
    commentAPI = generateArticleCommonsAPI(article.postId, article.replycnt, categoryId=article.classId)
    resp = requests.get(commentAPI)
    resp.encoding = "utf-8"
    commentViews = json.loads(resp.text)['result']['commentLikes'][0]['commentViews']
    comments = commentViews['comments']
    for i in range(len(comments)):
        comtData = comments[i]
        comment = Entity()
        comment.parent = article
        comment.pageUrl = article.pageUrl
        comment.postTitle = article.postTitle
        comment.authorName = comtData['displayName']
        comment.articleDate = msTransToDate(comtData['createdDate'])
        comment.content = comtData['contents'][0]['extData']['content']
        comment.site = site
        comment.postId = article.postId + "_" + str(i+1)

        comment.rid = comment.parent.postId
        comment.pid = comment.parent.postId

        comment.likescnt = extarctLikeCnt(comtData['ext']['likeCount'])
        comment.dislikescnt = extarctDislikeCnt(comtData['ext']['likeCount'])

        comment.replycnt = comtData['ext']['replyCount']
        comment.commentSn = comtData['commentSn']

        outqueue.put(comment.toList())

        parseReply(comment)# 解析留言的回覆 param 需傳入主文物件

############### tools ################
#   取得 Line Today 留言的 API
def generateArticleCommonsAPI(postId, commentsAmount="0", categoryId=None):
    if commentsAmount.__eq__("0"):
        commentsAmount = "50"
    api = "https://api.today.line.me/webapi/article/dinfo?articleIds=" + postId +"&categoryId=" + categoryId + "&country=TW&sort=POPULAR&commentSize=" + commentsAmount
    return api

def msTransToDate(param):
    ms = param
    return datetime.datetime.fromtimestamp(ms/1000.0).__str__()


def extarctDate(date_str):
    return datetime.datetime.strptime(date_str[5:], "%Y年%m月%d日%H:%M").__str__()

class Entity(object):
    def __init__(self):
        pass

    def toList(self):
        newRecord = []
        newRecord.append(parse.unquote(self.pageUrl))
        newRecord.append(self.postTitle)
        newRecord.append(self.authorName)
        newRecord.append(self.articleDate)
        newRecord.append(self.content)
        newRecord.append(self.postId)
        newRecord.append(self.site)
        newRecord.append(self.rid)
        newRecord.append(self.pid)
        newRecord.append(self.likescnt)
        newRecord.append(self.dislikescnt)
        newRecord.append(self.replycnt)
        return newRecord


def generateCommonsReplysAPI(postId, replycnt, commentSn):
    api = "https://api.today.line.me/webapi/comment/list?articleId=" + postId + "&limit=" + str(replycnt) + "&country=TW&parentCommentSn=" + str(commentSn)
    return api

def extarctLikeCnt(likeData):
    try:
        return likeData['up']
    except Exception:
        return 0


def extarctDislikeCnt(likeData):
    try:
        return likeData['down']
    except Exception:
        return 0
########## tools ############



if __name__ == "__main__":
    getCrawlablePage.startCraw()
    inqueue = getCrawlablePage.outqueue
    while 1:
        try:
            record = inqueue.get(block=False)
            startParse(record[0], record[1], record[2])
        except Empty as es:
            break

