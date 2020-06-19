import re

from bs4 import BeautifulSoup

from Crawler.ltn.tools_2 import session, Entity, generateDate, toMD5


def extractAuthorName(content):
    matcher = re.search("〔.*?／.*?報導〕", content)
    if matcher:
        return matcher.group()
    return "自由時報"

def startParse(url):
    try:
        resp = session.get(url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        body = soup.find("div", {"itemprop": "articleBody"})
        article = Entity()
        article.url = url
        article.postId = toMD5(url)
        article.rid = article.postId
        article.title = body.find("h1").getText()
        article.articleDate = generateDate(body.find("span", class_="time").getText())
        for p in body.findAll("p"):
            article.content += p.getText().strip()
            article.authorName = extractAuthorName(article.content)
        print("寫入資料: ", article.toMap())
    except Exception:
        print("文章解析失敗: ", url)


if __name__ == '__main__':
    url = "https://news.ltn.com.tw/news/politics/breakingnews/3173094"
    startParse(url)