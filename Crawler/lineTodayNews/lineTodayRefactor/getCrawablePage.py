from Crawler.lineTodayNews.lineTodayRefactor.tools_2 import generateDate, PreCrawlerProcessor, session
from bs4 import BeautifulSoup

frontPage = "https://today.line.me/TW/pc/main/100457"

def cutClassId(url):
    result = str(url)[-url.index("/"):]
    return result

def parseDigestModule(digestTagsElems):
    # 大看板
    newRecord = {}
    newRecord["classId"] = cutClassId(frontPage)
    newRecord["postId"] = digestTagsElems[0].a.get("data-articleid")
    newRecord["url"] = (digestTagsElems[0].a.get("href"))
    print(newRecord)

    # 熱區的 li
    ul = digestTagsElems[0].findAll("li")
    for li in ul:
        newRecord = {}
        newRecord["classId"] = cutClassId(frontPage)
        newRecord["postId"] = (li.a.get("data-articleid"))
        newRecord["url"] = (li.a.get("href"))
        print(newRecord)


def parseOperationModule(operationTagsElems):
    for el in operationTagsElems:
        ul = el.findAll("li")
        for li in ul:
            newRecord = {}
            newRecord["classId"] = (cutClassId(frontPage))
            newRecord["postId"] = (li.a.get("data-articleid"))
            newRecord["url"] = (li.a.get("href"))
            print(newRecord)


# 實作 fillDataToQueue() 與 getNextPage() 就可以了。
class Processor(PreCrawlerProcessor):
    def getCrawablePage(self, url) -> BeautifulSoup:
        resp = session.get(url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        digestTagsElems = soup.findAll("div", {"class": "digest-module"})
        operationTagsElems = soup.findAll("div", {"class": "operation-module"})
        try:
            parseDigestModule(digestTagsElems)  # 熱區
        except Exception:
            print("熱區爬取失敗 : ", frontPage)
        parseOperationModule(operationTagsElems)  # 話題

    def getNextPage(self, pagesBar) -> str:
        pass


if __name__ == '__main__':
    processor = Processor()
    processor.start(frontPage)