from queue import Queue

import requests
from bs4 import BeautifulSoup

from Crawler.commonWealth.tools import generateTxDate, extractPostDate

outqueue = Queue()

frontPage = "https://www.cw.com.tw/masterChannel.action?idMasterChannel=9"
txDate = generateTxDate("2020-02-1")

def startCraw(url):
    fillUrlQueue(url)

def fillUrlQueue(url):
    keepGo = True
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, features='lxml')
    li_tags = soup.findAll("div", class_="caption")
    for li in li_tags:
        postDate = extractPostDate(li.time.text.strip())
        if postDate >= txDate:
            url = li.h3.a.get("href").strip()
            outqueue.put(url)
        else:
            keepGo = False
            break

    nextPageUrl = getNextPageUrl(soup)
    if(nextPageUrl is not None) and keepGo:
        fillUrlQueue(nextPageUrl)

def getNextPageUrl(soup):
    pagination = soup.find("ul", class_="pagination")
    nextTag = pagination.find("li", class_="next")
    if nextTag is not None:
        return nextTag.a.get("href")
    else:
        print("到最後一頁拉..")
        return None


if __name__ == '__main__':
    startCraw(frontPage)
    while True:
        try:
            url = outqueue.get(block=False)
            print(url)
        except Exception:
            break
