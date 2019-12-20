from queue import Queue, Empty

import requests
from bs4 import BeautifulSoup

frontPage = "https://today.line.me/TW/pc/main/100457"
outqueue = Queue()

def parseDigestModule(digestTagsElems):
    # 大看板
    newRecord = []
    newRecord.append(cutClassId(frontPage))
    newRecord.append(digestTagsElems[0].a.get("data-articleid"))
    newRecord.append(digestTagsElems[0].a.get("href"))
    outqueue.put(newRecord)

    # 熱區的 li
    ul = digestTagsElems[0].findAll("li")
    for li in ul:
        newRecord = []
        newRecord.append(cutClassId(frontPage))
        newRecord.append(li.a.get("data-articleid"))
        newRecord.append(li.a.get("href"))
        outqueue.put(newRecord)


def parseOperationModule(operationTagsElems):
    for el in operationTagsElems:
        ul = el.findAll("li")
        for li in ul:
            newRecord = []
            newRecord.append(cutClassId(frontPage))
            newRecord.append(li.a.get("data-articleid"))
            newRecord.append(li.a.get("href"))
            outqueue.put(newRecord)


def startCraw():
    resp = requests.get(frontPage)
    soup = BeautifulSoup(resp.text, features="html.parser")
    digestTagsElems = soup.findAll("div", {"class": "digest-module"})
    operationTagsElems = soup.findAll("div", {"class": "operation-module"})
    try:
        parseDigestModule(digestTagsElems)  # 熱區
    except Exception:
        print("熱區爬取失敗 : ", frontPage)
    parseOperationModule(operationTagsElems)  # 話題

###### tools #######

def cutClassId(url):
    print("要解析的url -> ", url)
    result = str(url)[-url.index("/"):]
    return result

###### tools #######

if __name__ == "__main__":
    startCraw()
    while 1:
        try:
            print(outqueue.get(block=False))
        except Empty as es:
            break
