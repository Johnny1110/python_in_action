from bs4 import BeautifulSoup

from Crawler.storm.refactor.tools_2 import session, Entity, toMD5, generateDate

def startParse(url):
    resp = session.get(url)
    soup = BeautifulSoup(resp.text, features="lxml")
    main = soup.find("div", class_="page_wrapper")
    article = Entity()
    article.url = url
    article.authorName = main.find("a", class_="link_author info_inner_content").text
    article.title = main.find("h1", id="article_title").text
    article.content = main.find("div", id="CMS_wrapper").text
    article.articleDate = generateDate(main.find("span", id="info_time").text)
    article.postId = toMD5(url)
    article.rid = article.postId
    print("寫入資料庫: ", article.toMap())

if __name__ == '__main__':
    url = "https://www.storm.mg/article/2684441"
    startParse(url)