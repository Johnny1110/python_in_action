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
    # mySender(article.toMap())
    article.setAttr("html", html)
    return article



def parseComments(article):
    html = article.getAttr("html")
    soup = BeautifulSoup(html, features='lxml')
    comment_tags = soup.findAll("div", class_="push")
    for index, tag in enumerate(comment_tags):
        comment = Entity()
        comment.parent = article
        comment.postId = toMD5("{}_{}".format(article.url, index))
        comment.rid = article.postId
        comment.authorName = tag.find("span", class_="f3 hl push-userid").getText()
        comment.articleDate = generateIpDate(article.articleDate, tag.find("span", class_="push-ipdatetime").getText())
        comment.content = tag.find("span", class_="f3 push-content").getText()
        # mySender(comment.toMap())




def startParse(url, html):
    article = parseArticle(url, html)
    print(article.toMap())
    parseComments(article)


if __name__ == '__main__':
    url = "https://www.ptt.cc/bbs/Gossiping/M.1584080011.A.713.html"
    html = requests.get(url, headers=headers, cookies=cookies)
    html.encoding = 'utf-8'
    html = html.text
    startParse(url, html)