from queue import Queue

import requests
from bs4 import BeautifulSoup

from Crawler.storm.tools import *

frontPage = "https://www.storm.mg/category/118"
txDate = generateTxDate("2020-02-04")

outqueue = Queue()


def startCraw():
    fillCrawableUrl(frontPage)

def fillCrawableUrl(page):
    keepGo = True
    resp = requests.get(page)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, features="lxml")
    items = soup.findAll("div", {"class": "category_card card_thumbs_left"})
    for it in items:
        date_str = it.find("span", class_="info_time")
        postDate = extractPostDate(date_str.text)
        if postDate > txDate:
            url = it.find("a", class_="card_link link_img").get("href")
            outqueue.put(url)
        else:
            keepGo = False  # 停止往下一頁遞回
            break  # 離開此頁 items

    pageBar = soup.find("div", class_="pages_wrapper pagination_content")
    nextPageUrl = getNextPage(pageBar)

    if (keepGo) and (nextPageUrl is not None):
        fillCrawableUrl(nextPageUrl)


def getNextPage(pageBar):
    currentPageTag = pageBar.find("a", class_="pages active")
    if not str(currentPageTag.text).__eq__("100"):  # 超過 100 頁會 404
        nextPageTag = currentPageTag.find_next_sibling('a')
        nextPageUrl = generateStormUrl(nextPageTag.get("href"))
        return nextPageUrl



if __name__ == '__main__':
    startCraw()
    while True:
        try:
            url = outqueue.get(block=False)
            print(url)
        except Exception as ex:
            break


