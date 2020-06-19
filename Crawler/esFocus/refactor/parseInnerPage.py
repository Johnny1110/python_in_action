from bs4 import BeautifulSoup

from Crawler.esFocus.refactor.tools_2 import session, Entity, generateDate, toMD5, extractAuthorName

def startParse(url):
    resp = session.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, features='lxml')
    mainTag = soup.find("section", class_="section")
    article = Entity()
    article.url = url
    article.title = mainTag.find("h1", class_="title").text.strip()
    article.articleDate = generateDate(mainTag.find("time", class_="datetime").text)
    content = mainTag.findAll("p")
    for p in content:
        article.content += p.text.strip()
    article.authorName = extractAuthorName(article.content)
    article.postId = toMD5(url)
    article.rid = article.postId
    print("寫入 DB: ", article.toMap())
    return article

if __name__ == '__main__':
    url = "https://www.eventsinfocus.org/news/7145729"
    startParse(url)