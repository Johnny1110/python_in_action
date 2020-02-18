from queue import Queue

import requests
from bs4 import BeautifulSoup

from Crawler.esFocus.tools import generateTxDate, PreCrawlerProcessor, extractPostDate, generateEsUrl

txDate = generateTxDate("2019-12-30")
frontPage = "https://www.eventsinfocus.org/news?page=0"

outqueue = Queue()

class Processor(PreCrawlerProcessor):
    def fillDataToQueue(self, url) -> BeautifulSoup:
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        urlTags = soup.findAll("div", class_="mb-3 views-row")
        pageBar = soup.find("ul", class_="pagination js-pager__items")

        for tag in urlTags:
            postDate = extractPostDate(tag.find("time").text.strip())
            if postDate >= txDate:
                outqueue.put(generateEsUrl(tag.find("a").get("href").strip()))
            else:
                pageBar = None
                break
        return pageBar

    def getNextPage(self, pageBar) -> str:
        if pageBar is not None:
            li = pageBar.find("li", class_="pager__item--next")
            pageNum = li.a.get("href").strip()
            if pageNum is not None:
                nextUrl = "https://www.eventsinfocus.org/news" + pageNum
                return nextUrl



def startCraw():
    processor = Processor()
    processor.fillUrlQueue(frontPage)


if __name__ == '__main__':
    startCraw()
    while True:
        try:
            url = outqueue.get(block=False)
        except Exception:
            break
