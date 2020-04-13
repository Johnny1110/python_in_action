import re

from bs4 import BeautifulSoup

from Crawler.EYNY.tools_2 import session, Entity, toMD5, generateDate


def parseArticle(url, firstPageContent):
    soup = BeautifulSoup(firstPageContent, features='lxml')
    article = Entity()
    article.title = soup.find("title")
    article.url = url
    article.postId = toMD5(url)
    article.rid = article.postId
    main_post = soup.find("div", {"id": re.compile("post_.*")})
    postDateStr = main_post.find("em", {"id": re.compile("authorposton.*")}).getText()[4:].strip()
    article.articleDate = generateDate(postDateStr)


def parseComments(article):
    pass

def startParse(url):
    resp = session.get(url)
    resp.encoding = 'utf-8'
    firstPageContent = resp.text
    article = parseArticle(url, firstPageContent)
    parseComments(article)



if __name__ == '__main__':
    url = "http://www36.eyny.com/thread-7409718-1-3GDAAPTM.html"
    startParse(url)