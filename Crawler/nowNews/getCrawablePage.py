import requests
from bs4 import BeautifulSoup

from Crawler.nowNews.tools_2 import generateDate, PreCrawlerProcessor, session, generateNowNewsUrl

frontPage = "https://www.nownews.com/cat/health-life/"
txDate = generateDate("2020-05-01")

def buildFrontJsonUrl(frontPage):
    par = frontPage.split("/")[-2]
    jsonUrl = "https://gcs-static-json-lb.nownews.com/api/v1/cat/{}.json".format(par)
    return jsonUrl

def generateNextJsonUrl(postId):
    class_ = frontPage.split("/")[-2]
    jsonUrl = "https://www.nownews.com/nn-client/api/v1/cat/{}/?pid={}".format(class_, postId)
    return jsonUrl

# 實作 fillDataToQueue() 與 getNextPage() 就可以了。
class Processor(PreCrawlerProcessor):
    def getCrawablePage(self, url) -> str:
        resp = session.get(url)
        resp.encoding = 'utf-8'
        respJson = resp.json()
        newsList = respJson['data']['newsList']
        for new in newsList:
            newsDate = generateDate(new['newsDate'])
            if newsDate >= txDate:
                postUrl = generateNowNewsUrl(new['postUrl'])
                url = {
                    "url": postUrl
                }
                print(url)
            else:
                continue

        if generateDate(newsList[-1]['newsDate']) >= txDate:
            postId = newsList[-1]["id"]
            return generateNextJsonUrl(postId)

    def getNextPage(self, jsonUrl) -> str:
        print("next: ", jsonUrl)
        return jsonUrl


if __name__ == '__main__':
    url = buildFrontJsonUrl(frontPage)
    processor = Processor()
    processor.start(url)
