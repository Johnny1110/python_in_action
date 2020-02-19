from queue import Queue

from Crawler.businessToday.tools import generateTxDate, PreCrawlerProcessor, extractPostDate

outqueue = Queue()

import requests
from bs4 import BeautifulSoup

frontPage = "https://www.businesstoday.com.tw/catalog/80391"
txDate = generateTxDate("2020-02-16")
pageNum = 1
overFlow = 0  # 當截止日期條件滿足 3 個再離開

# 實作 fillDataToQueue() 與 getNextPage() 就可以了。
class Processor(PreCrawlerProcessor):
    def fillDataToQueue(self, url) -> BeautifulSoup:
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        li_tags = soup.findAll("a")
        if li_tags is not None:
            for a in li_tags:
                postDate = extractPostDate(a.find("p", class_="article__item-date").text)
                if postDate >= txDate:
                    outqueue.put(a.get("href").strip())
                else:
                    global overFlow
                    overFlow += 1
                    if overFlow >= 3:
                        soup = None
                        break
        global pageNum
        pageNum += 1
        return soup


    def getNextPage(self, pagesBar) -> str:
        if pagesBar is not None:
            return generateAjaxQuery(frontPage, pageNum)

def generateAjaxQuery(url, page):
    if page < 1000:
        return "{}/list/page/{}/ajax".format(url, page)
    else:
        return None

if __name__ == '__main__':
    processor = Processor()
    processor.start(generateAjaxQuery(frontPage, pageNum))
    while True:
        try:
            url = outqueue.get(block=False)
            print(url)
        except Exception:
            break