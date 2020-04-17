import re

import requests
from bs4 import BeautifulSoup

from Crawler.EYNY.tools_2 import session, Entity, toMD5, generateDate, generateEYNYUrl, headers

cookies = {
    "612e55XbD_e8d7_agree": "1",
    "612e55XbD_e8d7_videoadult": "1",
}

def parseArticle(url, firstPageContent):
    soup = BeautifulSoup(firstPageContent, features='lxml')
    article = Entity()
    article.title = soup.find("title").getText()
    article.url = url
    main_post = soup.find("div", id=re.compile("^post_[0-9].*$"))
    article.postId = toMD5(main_post.get("id"))
    article.rid = article.postId
    postDateStr = ""
    try:
        postDateStr = main_post.find("em", {"id": re.compile("authorposton.*")}).getText()[4:].strip()
        article.articleDate = generateDate(postDateStr)
    except Exception:
        postDateStr = main_post.find("em", {"id": re.compile("authorposton.*")}).span.get("title")
        article.articleDate = generateDate(postDateStr)
    article.articleDate = generateDate(postDateStr)
    article.authorName = "???"
    try:
        article.authorName = main_post.find("div", id=re.compile("^userinfo.*$")).strong.getText()
    except Exception:
        article.authorName = "用戶已被刪除(無名)"
    article.content = main_post.find("td", id=re.compile("^postmessage_.*$")).getText()
    article.setAttr("pageSrc", firstPageContent)
    print(article.toMap())
    return article


def collectSingleComment(comment):
    c_tag = comment.getAttr("c_tag")
    comment.postId = toMD5(c_tag.get("id"))
    comment.rid = comment.parent.postId
    postDateStr = ""
    try:
        postDateStr = c_tag.find("em", {"id": re.compile("authorposton.*")}).getText()[4:].strip()
        comment.articleDate = generateDate(postDateStr)
    except Exception:
        postDateStr = c_tag.find("em", {"id": re.compile("authorposton.*")}).span.get("title")
        comment.articleDate = generateDate(postDateStr)

    comment.authorName = "???"
    try:
        comment.authorName = c_tag.find("div", id=re.compile("^userinfo.*$")).strong.getText()
    except Exception:
        comment.authorName = "用戶已被刪除(無名)"
    comment.content = c_tag.find("td", id=re.compile("^postmessage_.*$")).getText()


def parseComments(article, isFirst=False):
    pageSrc = article.getAttr("pageSrc")
    soup = BeautifulSoup(pageSrc, features='lxml')
    if isFirst:
        all_comments = soup.findAll("div", id=re.compile("^post_[0-9].*$"))[1:]  # 排除樓主
    else:
        all_comments = soup.findAll("div", id=re.compile("^post_[0-9].*$"))
    for c_tag in all_comments:
        comment = Entity()
        comment.parent = article
        comment.setAttr("c_tag", c_tag)
        collectSingleComment(comment)
        print(comment.toMap())

    nextPageBar = soup.find("div", class_="pg")
    if nextPageBar is None:
        return
    nextPageTag = nextPageBar.find("a", text="下一頁")
    if nextPageTag is not None:
        next_url = generateEYNYUrl(nextPageTag.get("href"))
        print("爬取留言下ㄧ頁: ", next_url)
        resp = requests.get(next_url, headers=headers, cookies=cookies)
        resp.encoding = 'utf-8'
        article.setAttr("pageSrc", resp.text)
        parseComments(article)


def startParse(url):
    data = {
        "agree": "yes"
    }
    resp = session.post(url, data=data)
    resp.encoding = 'utf-8'
    firstPageContent = resp.text
    article = parseArticle(url, firstPageContent)
    parseComments(article, isFirst=True)


if __name__ == '__main__':
    # processor = Processor()
    # processor.start(frontPage)
    # for urlMap in urlList:
    #     startParse(urlMap['url'])

    url = "https://www.eyny.com/thread-12624356-1-GU7Y04C7.html"
    startParse(url)
