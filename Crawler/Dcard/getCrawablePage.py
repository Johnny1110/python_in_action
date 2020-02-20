import json
from queue import Queue

from Crawler.Dcard.tools import generateDate, PreCrawlerProcessor, session

outqueue = Queue()

import requests

siteClass = "vehicle"
txDate = generateDate("2020-02-17")

class Processor(PreCrawlerProcessor):
    def fillDataToQueue(self, url) -> str:
        lastId = None
        resp = session.get(url)
        resp = resp.json()
        if len(resp) == 0:
            return
        for data in resp:
            postDate = generateDate(data['createdAt'])
            if postDate >= txDate:
                outqueue.put(siteClass)  # 第一欄輸入 siteClass
                outqueue.put(data['id'])  # 第二欄輸入 id
                outqueue.put(postDate)  # 第三欄輸入 postDate
                lastId = data['id']
            else:
                lastId = None
                break
        return lastId


    def getNextPage(self, lastId) -> str:
        if lastId is not None:
            return generateFetchDataUrl(siteClass, lastId)


def generateFetchDataUrl(siteClass, id=None):
    baseUrl = "https://www.dcard.tw/service/api/v2/forums/{}/posts?limit=30{}"
    if id is not None:
        return baseUrl.format(siteClass, "&before=" + str(id))
    else:
        return baseUrl.format(siteClass, "")

if __name__ == '__main__':
    processor = Processor()
    processor.start(generateFetchDataUrl(siteClass))
    while True:
        try:
            print(outqueue.get(block=False))
        except Exception:
            break
