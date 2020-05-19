import re

from bs4 import BeautifulSoup

from Crawler.nowNews.tools_2 import session, Entity, toMD5, generateDate


def startParse(url):
    try:
        resp = session.get(url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        main = soup.find("div", class_="newsContainer")
        article = Entity()
        article.title = main.find("h3", class_="newsTitle").getText()
        article.url = url
        article.postId = toMD5(url)
        article.rid = article.postId
        newsInfo = main.find("div", class_="newsInfo").getText()  # 記者吳雨婕/綜合報導-2020-05-17 08:00:00
        dateStr = re.search("[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}", newsInfo).group()
        try:
            authorName = re.sub("-{}".format(dateStr), "", newsInfo)
        except Exception:
            authorName = "???"
        article.authorName = authorName
        article.articleDate = generateDate(dateStr)
        article.content = main.find("div", class_="newsMsg").getText()
        print("已寫入: ", article.title)
    except Exception:
        print("文章解析失敗 url: ", url)


if __name__ == '__main__':
    url = "https://www.nownews.com//news/entertainment/5008706"
    startParse(url)