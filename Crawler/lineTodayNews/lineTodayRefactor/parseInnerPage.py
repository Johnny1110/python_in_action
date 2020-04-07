import json

from bs4 import BeautifulSoup

from Crawler.lineTodayNews.lineTodayRefactor.tools_2 import session, Entity, generateArticleCommonsAPI, extarctDate, \
    toMD5, msTransToDate, generateCommonsReplysAPI


def startParse(classId, postId, url):
    resp = session.get(url)
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
    resp = session.get(commentsAPI)
    resp.encoding = "utf-8"
    commentAndLikes = json.loads(resp.text)['result']['commentLikes'][0]
    likeViews = commentAndLikes['likeViews']
    commentViews = commentAndLikes['commentViews']

    ### 解析主文 ###
    article.likescnt = likeViews['count']
    article.dislikescnt = 0
    article.replycnt = commentViews['count']
    article.url = url
    article.title = soup.select_one("h2", {"class": "news-title"}).text.strip()
    article.authorName = "???"
    try:
        article.authorName = soup.select("dd.name")[0].text.strip()
    except Exception:
        article.authorName = soup.select("dd.publisher")[0].text.strip()
    article.articleDate = extarctDate(soup.select("dd.date")[0].text.strip())
    articleArea = soup.find("article", {"class": "article-content news-content"})  # 提出 article area
    articleArea = articleArea.select("p")  # 提出所有的段落<p>
    for p in articleArea:
        article.content += str(p.text + "\t \n")
    article.postId = postId
    article.rid = article.postId
    article.setAttr("classId", classId)

    print("已寫入文章 : ", article.toMap())

    parseComments(article)  # 解析留言 param 需傳入主文物件


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


def parseComments(article):
    commentAPI = generateArticleCommonsAPI(article.postId, article.replycnt, categoryId=article.getAttr("classId"))
    resp = session.get(commentAPI)
    resp.encoding = "utf-8"
    commentViews = json.loads(resp.text)['result']['commentLikes'][0]['commentViews']
    comments = commentViews['comments']
    for i in range(len(comments)):
        comtData = comments[i]
        comment = Entity()
        comment.parent = article
        comment.url = article.url
        comment.title = article.title
        comment.authorName = comtData['displayName']
        comment.articleDate = msTransToDate(comtData['createdDate'])
        comment.content = comtData['contents'][0]['extData']['content']
        comment.postId = article.postId + "_" + str(i+1)
        comment.rid = article.postId
        comment.likescnt = extarctLikeCnt(comtData['ext']['likeCount'])
        comment.dislikescnt = extarctDislikeCnt(comtData['ext']['likeCount'])
        comment.replycnt = comtData['ext']['replyCount']
        comment.setAttr("commentSn", comtData['commentSn'])

        print("已寫入留言: ", comment.toMap())

        parseReply(comment)# 解析留言的回覆 param 需傳入主文物件


def parseReply(comment):
    replyAPI = generateCommonsReplysAPI(comment.parent.postId, comment.replycnt, comment.getAttr("commentSn"))
    resp = session.get(replyAPI)
    resp.encoding = "utf-8"
    replyJson = json.loads(resp.text)['result']['comments']['comments']

    for i in range(len(replyJson)):
        repData = replyJson[i]
        reply = Entity()
        reply.parent = comment
        reply.url = comment.url
        reply.title = comment.title
        reply.authorName = repData['displayName']
        reply.articleDate = msTransToDate(repData['createdDate'])
        reply.content = repData['contents'][0]['extData']['content']
        reply.postId = comment.postId + "_" + str(i+1)
        reply.rid = reply.parent.postId
        reply.likescnt = 0
        reply.dislikescnt = 0
        reply.replycnt = 0

        print("已寫入回應: ", reply.toMap())


if __name__ == '__main__':
    classId = "100457"
    postId = "98286284"
    url = "https://today.line.me/tw/pc/article/%E5%A7%8B%E6%96%99%E6%9C%AA%E5%8F%8A%E7%9A%84%E7%96%AB%E6%83%85%E5%BD%B1%E9%9F%BF%EF%BC%81-DPzO6p"
    startParse(classId, postId, url)