from bs4 import BeautifulSoup

from Crawler.businessToday.refactor.tools_2 import session, Entity, toMD5, generateDate

def startParse(url):
    resp = session.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, features='lxml')
    article = Entity()
    article.url = url
    article.postId = toMD5(url)
    article.rid = article.postId
    main_tag = soup.find("div", class_="container")
    article.title = main_tag.find("h1", class_="article__maintitle").text.strip()
    article.articleDate = generateDate(
        main_tag.find("p", class_="context__info-item context__info-item--date").text.strip())
    article.authorName = main_tag.find("p", class_="context__info-item context__info-item--author").text.strip()
    article.content = main_tag.find("div", {"itemprop": "articleBody"}).text.strip()
    print("寫入 DB: ", article.toMap())
    return article


if __name__ == '__main__':
    url = "https://www.businesstoday.com.tw/article/category/80398/post/202006110018/Fed決策讓市場感到擔憂？「這兩個變數」恐使美股面臨下跌10％的風險"
    startParse(url)