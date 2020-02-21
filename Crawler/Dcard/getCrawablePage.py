from json import JSONDecodeError
from queue import Queue
from time import sleep

from Crawler.Dcard.tools import generateDate, PreCrawlerProcessor, session

outqueue = Queue()

siteClass = "nptu"
txDate = generateDate("2020-02-01")
retryCnt = 0  # 嘗試 5 次，失敗就離開。

class Processor(PreCrawlerProcessor):
    def fillDataToQueue(self, url) -> str:
        try:
            lastId = None
            resp = session.get(url)
            resp = resp.json()
            if len(resp) == 0:
                return
            for data in resp:
                postDate = generateDate(data['createdAt'])
                if postDate >= txDate:
                    newRecord = []
                    newRecord.append(siteClass)# 第一欄輸入 siteClass
                    newRecord.append(data['id'])# 第二欄輸入 id
                    newRecord.append(postDate)# 第三欄輸入 postDate
                    outqueue.put(newRecord)
                    lastId = data['id']
                else:
                    lastId = None
                    break
            return lastId
        except JSONDecodeError as e:
            global retryCnt
            retryCnt += 1
            if retryCnt > 5:
                print(" url 解析失敗(JSONDecodeError) : ", url, " 已嘗試過 ", retryCnt, " 次。")
            else:
                sleep(5)
                self.start(url)



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
