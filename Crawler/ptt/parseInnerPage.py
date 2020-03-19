import requests
from bs4 import BeautifulSoup

from Crawler.ptt.tools import Entity, toMD5, generateDate, headers, cookies, generateIpDate

def parseArticle(url, html):
    soup = BeautifulSoup(html, features='lxml')
    article = Entity()
    article.url = url
    article.postId = toMD5(url)
    article.rid = article.postId
    article.title = soup.find("title").getText()
    article.authorName = soup.find("span", text="作者").next_sibling.getText()
    article.articleDate = generateDate(soup.find("span", text="時間").next_sibling.getText())
    content = soup.find("div", id="main-content")
    for child in content.findAll():
        child.decompose()
    article.content = content.getText().strip()
    article.setAttr("html", html)
    return article


def processCommentMapList(temp_comment_map_list):
    print(temp_comment_map_list)


def parseComments(article):
    html = article.getAttr("html")
    soup = BeautifulSoup(html, features='lxml')
    comment_tags = soup.findAll("div", class_="push")
    temp_comment_list = []
    for index, tag in enumerate(comment_tags):
        comment = Entity()
        comment.parent = article
        comment.postId = toMD5("{}_{}".format(article.url, index))
        comment.rid = article.postId
        comment.authorName = tag.find("span", class_="f3 hl push-userid").getText()
        comment.articleDate = generateIpDate(article.articleDate, tag.find("span", class_="push-ipdatetime").getText())
        comment.content = tag.find("span", class_="f3 push-content").getText()
        cmtType = tag.find("span", class_="f1 hl push-tag")
        if cmtType is None:
            cmtType = tag.find("span", class_="hl push-tag")
        if cmtType is not None:
            cmtType = cmtType.getText().strip()
            comment.setAttr("type", cmtType)
        else:
            print("comment type parse error : ", comment.content)
        temp_comment_list.append(comment)

    comment_list = processCommentMapList(temp_comment_list)




def startParse(url, html):
    article = parseArticle(url, html)
    parseComments(article)
    # mySender(article.toArticleMap())
    print(article.toArticleMap())


if __name__ == '__main__':
    url = "https://www.ptt.cc/bbs/Gossiping/M.1584080011.A.713.html"
    html = requests.get(url, headers=headers, cookies=cookies)
    html.encoding = 'utf-8'
    html = html.text
    startParse(url, html)