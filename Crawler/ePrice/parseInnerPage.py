from bs4 import BeautifulSoup

from Crawler.ePrice.tools_2 import session, Entity, toMD5, generateDate


def parseArticle(resp):
    soup = BeautifulSoup(resp.text, features='lxml')
    article = Entity()
    article.url = resp.url
    article.postId = toMD5(resp.url)
    article.rid = article.postId
    article.title = soup.select('h1.title')[0].text
    article.authorName = soup.select('a.nickname')[0].text
    date_str = soup.select('span.date')[0].text[4:].strip()
    article.articleDate = generateDate(date_str)
    article.content = soup.select('div.user-comment-block')[0].text.strip()
    print("已寫入文章: ", article.title)
    article.setAttr("soup", soup)
    return article


def parseComments(article, id_index=1):
    soup = article.getAttr("soup")
    for resp in soup.findAll("dd", {"class": "enabled"}):
        id_index += 1
        entity = Entity()
        entity.parent = article
        entity.authorName = resp.select("a.nickname")[0].text
        entity.title = soup.select('h1.title')[0].text
        entity.postId = toMD5(article.url + '_' + str(id_index))
        entity.rid = article.postId
        entity.content = resp.select('div.comment')[0].text.strip()
        date_str = resp.select('span.date')[0].text[4:].strip()
        entity.articleDate = generateDate(date_str)
        print("已寫入留言: ", entity.content)


def startParse(url):
    resp = session.get(url)
    resp.encoding = 'utf-8'
    article = parseArticle(resp)
    parseComments(article)


if __name__ == '__main__':
    url = "https://www.eprice.com.tw/mobile/talk/4544/5517994/1/"
    startParse(url)