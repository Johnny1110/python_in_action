import datetime

import requests
from bs4 import BeautifulSoup

from Crawler.esFocus.refactor.tools_2 import generateDate, PreCrawlerProcessor, session, generateEsUrl

frontPage = "https://www.eventsinfocus.org/news?page=0"
txDate = generateDate("2020-02-01") - datetime.timedelta(days=60)

print(txDate)

# 實作 fillDataToQueue() 與 getNextPage() 就可以了。
class Processor(PreCrawlerProcessor):
    def getCrawablePage(self, url) -> BeautifulSoup:
        resp = session.get(url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        urlTags = soup.findAll("div", class_="mb-3 views-row")
        pageBar = soup.find("ul", class_="pagination js-pager__items")

        for tag in urlTags:
            postDate = generateDate(tag.find("time").text.strip())
            if postDate >= txDate:
                url = {
                    "url": generateEsUrl(tag.find("a").get("href").strip())
                }
                print(url)
            else:
                pageBar = None
                break
        return pageBar

    def getNextPage(self, pagesBar) -> str:
        li = pagesBar.find("li", class_="pager__item--next")
        pageNum = li.a.get("href").strip()
        if pageNum is not None:
            nextUrl = "https://www.eventsinfocus.org/news" + pageNum
            return nextUrl


if __name__ == '__main__':
    processor = Processor()
    processor.start(frontPage)