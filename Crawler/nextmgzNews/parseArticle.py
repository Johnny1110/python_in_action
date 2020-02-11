import requests
from bs4 import BeautifulSoup

from Crawler.nextmgzNews import getCrawablePage
from Crawler.nextmgzNews.tools import Entity, extractArticleDate, extractAuthor, toMD5


def parseArticle(url):
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, features='lxml')
    content = soup.find("div", class_="article-content")
    article = Entity()
    article.url = url
    article.title = soup.find("title").text
    article.articleDate = extractArticleDate(soup.find("time", class_="time").text)
    for p in content.findAll("p"):
        article.content += p.text
    article.authorName = extractAuthor(article.content)
    article.postId = toMD5(url)
    article.rid = article.postId

    print(article.toList())


if __name__ == '__main__':
    urlQueue = getCrawablePage.outqueue
    getCrawablePage.startParse("https://tw.nextmgz.com/breakingnews/life")
    while True:
        try:
            url = urlQueue.get(block=False)
            print(url)
        except Exception as e:
            break


