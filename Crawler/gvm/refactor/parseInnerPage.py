from bs4 import BeautifulSoup

from Crawler.gvm.refactor.tools_2 import session, Entity, generateDate, toMD5

def startParse(url):
    resp = session.get(url)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, features='lxml')
    article = Entity()
    article.url = url
    main_tag = soup.find("article", class_="pc-bigArticle")
    article.title = main_tag.find("h1").text.strip()
    article.authorName = main_tag.find("div", class_="pc-bigArticle").text.strip()
    article.articleDate = generateDate(main_tag.find("div", class_="article-time").text.strip())
    article.content = main_tag.find("section", class_="article-content").text.strip()
    article.postId = toMD5(url)
    article.rid = article.postId
    print(article.toMap())
    return article


if __name__ == '__main__':
    url = "https://www.gvm.com.tw/article/71976"
    article = startParse(url)