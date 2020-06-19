from bs4 import BeautifulSoup

from Crawler.newsMarket.refactor.tools_2 import session, Entity, toMD5, generateDate


def startParse(url):
    resp = session.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, features='lxml')
    article = Entity()
    article.url = url
    article.postId = toMD5(url)
    article.rid = article.postId
    article.title = soup.find("h1", class_="entry-title").getText()
    article.authorName = soup.find("a", class_="author url fn").getText()
    article.articleDate = generateDate(soup.find("time", class_="entry-date").get("datetime"))
    content = soup.find("div", class_="entry-content")
    for p in content.findAll("p"):
        article.content += p.getText() + "\r\n"
    print("已寫入 DB: ", article.toMap())
    return article


if __name__ == '__main__':
    url = "https://www.newsmarket.com.tw/blog/132907/"
    startParse(url)