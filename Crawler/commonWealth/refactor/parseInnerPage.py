from bs4 import BeautifulSoup

from Crawler.commonWealth.refactor.tools_2 import session, Entity, toMD5, generateDate


def startParse(url):
    resp = session.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, features='lxml')
    article = Entity()
    article.url = url
    article.title = soup.find("title").text
    article.postId = toMD5(article.url)
    article.rid = article.postId
    try:
        article.authorName = soup.find("div", class_="author--item").a.getText().strip()
    except Exception:
        article.authorName = "???"
    content = soup.find("div", class_="article__content py20")
    article.articleDate = generateDate(soup.find("time").text)
    for p in content.findAll("p"):
        article.content += p.text.strip()
    print("寫入 DB: ", article.toMap())


if __name__ == '__main__':
    url = "https://www.cw.com.tw/article/article.action?id=5100506"
    startParse(url)