import requests
from bs4 import BeautifulSoup

from Crawler.pts.ptsRefactor.tools_2 import Entity, toMD5, generateDate

def startParse(url):
    try:
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        article = Entity()
        article.url = url
        article.postId = toMD5(url)
        article.rid = article.postId
        main_tag = soup.find("section", class_="wrapper wrapper2")
        article.title = main_tag.find("h1", class_="article-title").getText()
        article.authorName = main_tag.find("div", class_="maintype-wapper hidden-sm hidden-xs").div.getText()
        date_str = main_tag.find("div", class_="maintype-wapper hidden-sm hidden-xs").h2.getText()
        article.articleDate = generateDate(date_str, Chinese=True)
        article.content = main_tag.find("div", class_="article_content").getText()
        print(article.toMap())
        print("資料採集成功 title = ", article.title)
        return article
    except Exception as e:
        print("Article 解析失敗, url = ", url)


if __name__ == '__main__':
    url = 'https://news.pts.org.tw/article/472822'
    article = startParse(url)
