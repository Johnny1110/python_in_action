from bs4 import BeautifulSoup

import urllib

from Crawler.formosa.refactor.tools_2 import Entity, toMD5, generateDate


def startParse(url, html):
    try:
        soup = BeautifulSoup(html, features='lxml')
        main_content = soup.find("div", class_="content")
        article = Entity()
        article.url = url
        article.postId = toMD5(url)
        article.rid = article.postId
        article.title = main_content.find("h1").getText()
        article.articleDate = generateDate(main_content.find("small", class_="date").getText().strip())
        article.content = main_content.find("div", class_="body").getText().strip()
        article.authorName = main_content.find("article").getText()
        if len(article.authorName) > 100:
            article.authorName = "?"

        print('已成功寫入DB : ', article.toMap())
        return article
    except Exception:
        print('網頁解析失敗 url : ', url)



if __name__ == '__main__':
    url = "http://www.my-formosa.com/DOC_157504.htm"
    startParse(url)