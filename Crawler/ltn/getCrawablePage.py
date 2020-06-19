import requests
from bs4 import BeautifulSoup

from Crawler.ltn.tools_2 import generateDate, PreCrawlerProcessor, session

frontPage = "https://news.ltn.com.tw/list/breakingnews/politics"
txDate = generateDate("2020-05-20")
page = 1
# 實作 fillDataToQueue() 與 getNextPage() 就可以了。
class Processor(PreCrawlerProcessor):
    def getCrawablePage(self, url) -> BeautifulSoup:
        print("queryPage = ", url)
        resp = session.get(url)
        resp.encoding = 'utf-8'
        jsonData = resp.json()
        dataArray = jsonData['data']
        if len(dataArray)  is 0:
            return None
        nextAjaxQuery = buildAjaxQuery(page)
        for data in dataArray:
            if page > 1:
                data = dataArray[data]
            postDate = generateDate(data['time'])
            if postDate >= txDate:
                url = {
                    "postDate": postDate,
                    "url": data['url']
                }
                print("捕獲URL: ", url)
            else:
                nextAjaxQuery = None
                break

        return nextAjaxQuery


    def getNextPage(self, pagesBar) -> str:
        global page
        page += 1
        query = buildAjaxQuery(page)
        return query

def buildAjaxQuery(page=1):
    class_ = frontPage.split("/")[-1]
    ajax = "https://news.ltn.com.tw/ajax/breakingnews/{}/{}".format(class_, page)
    return ajax


if __name__ == '__main__':
    ajaxQuery = buildAjaxQuery()
    processor = Processor()
    processor.start(ajaxQuery)