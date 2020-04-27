import re

from bs4 import BeautifulSoup

from Crawler.lineTodayNews.lineTodaySecEdition.tools_2 import session

frontPage = "https://today.line.me/tw/v2/tab/NBA"

def getPageUidSet():
    resp = session.get(frontPage)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, features='lxml')
    targetScript = soup.find("script", text=re.compile("^window.__NUXT__=.*"))
    ans = re.findall("[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}", str(targetScript))
    id_set = set()
    for url in ans:
        id_set.add(url)
    return id_set

def getAllPageUrl():
    id_set = getPageUidSet()
    for id in id_set:
        print("爬取目標 id: ", id)
        url = buildListingURL(id)
        resp = session.get(url)
        resp.encoding = 'utf-8'
        items = resp.json()
        for item in items['items']:
            print(item)
            urlMap = {
                "title": item['title'],
                "url": buildInnerPageURL(item['url']['hash'])
            }
            print(urlMap)

def buildListingURL(id):
    return "https://today.line.me/api/v6/listings/{}?offset=0&length=1000&country=tw".format(id)

def buildInnerPageURL(url_hash):
    return "https://today.line.me/tw/article/{}".format(url_hash)

if __name__ == '__main__':
    getAllPageUrl()