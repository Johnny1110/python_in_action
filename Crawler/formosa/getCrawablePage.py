from queue import Queue

from Crawler.formosa.tools import generateDate, PreCrawlerProcessor, generateFormosaUrl

outqueue = Queue()

import requests
from bs4 import BeautifulSoup

frontPage = "http://www.my-formosa.com/KM/M_5.htm"
txDate = generateDate("2020-02-01")

# 實作 fillDataToQueue() 與 getNextPage() 就可以了。
class Processor(PreCrawlerProcessor):
    def fillDataToQueue(self, url) -> BeautifulSoup:
        resp = requests.get(url)
        resp.encoding = 'big5'
        soup = BeautifulSoup(resp.text, features='lxml')
        main_tag = soup.find("div", class_="content")
        for section in main_tag.findAll("section", id="featured-news"):
            try:
                url = section.findAll("a")[0].get("href").strip()
                url = generateFormosaUrl(url)
                outqueue.put(url)
            except Exception:
                pass

    def getNextPage(self, pagesBar) -> str:
        pass


if __name__ == '__main__':
    processor = Processor()
    processor.start(frontPage)
    while True:
        try:
            print(outqueue.get(block=False))
        except Exception as e:
            break