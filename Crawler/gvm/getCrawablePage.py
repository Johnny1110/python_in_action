from queue import Queue

import requests
from bs4 import BeautifulSoup

from Crawler.gvm.tools import generateTxDate, PreCrawlerProcessor, extractPostDate
outqueue = Queue()


frontPage = "https://www.gvm.com.tw/category/business"
txDate = generateTxDate("2020-04-01")

class Processor(PreCrawlerProcessor):
    def fillDataToQueue(self, url):
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        pagesBar = soup.find("ul", class_="article-list__pagination")
        main_tag = soup.find("div", id="article_list")
        url_tags = main_tag.findAll("div", class_="article-list-item__intro")
        for item in url_tags:
            postDate = extractPostDate(item.find("div", class_="time").text.strip())
            if postDate >= txDate:
                url = item.findAll("a")[0].get("href").strip()
                outqueue.put(url)
            else:
                pagesBar = None
                break

        return pagesBar


    def getNextPage(self, pagesBar):
        if pagesBar is not None:
            currentPage = pagesBar.find("li", class_="active")
            nextPageTag = currentPage.next_sibling
            if nextPageTag is not None:
                nextUrl = nextPageTag.find("a").get("href").strip()
                return nextUrl

def startCraw():
    processor = Processor()
    processor.fillUrlQueue(frontPage)


if __name__ == '__main__':
    startCraw()
    while True:
        try:
            url = outqueue.get(block=False)
            print(url)
        except Exception:
            break