from bs4 import BeautifulSoup

from Crawler.upMedia.refactor.tools_2 import randomSleep, session, headers, Entity, toMD5, generateDate


def startParse(url):
    try:
        randomSleep()
        resp = session.get(url, headers=headers)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        main_tag = soup.find("div", id="news-info")
        article = Entity()
        article.url = url
        article.postId = toMD5(url)
        article.rid = article.postId
        article.title = main_tag.find("h2", id="ArticleTitle").getText()
        author_tag = main_tag.find("div", class_="author")
        article.authorName = author_tag.a.getText()
        author_tag.a.decompose()
        article.articleDate = generateDate(author_tag.getText().strip(), Chinese=True)
        content = main_tag.find("div", class_="editor")
        for p in content.findAll("p"):
            article.content += p.getText().strip() + '\r\n'
        print("寫入db: ", article.title)
    except Exception as e:
        print("內文解析失敗 url: ", url)


if __name__ == '__main__':
    url = "https://www.upmedia.mg/news_info.php?SerialNo=88169"
    startParse(url)