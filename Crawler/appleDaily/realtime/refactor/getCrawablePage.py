from queue import Queue

from Crawler.appleDaily.realtime.refactor.tools import generateDate, PreCrawlerProcessor, urlToByteList, \
    generateAppleUrl, session

outqueue = Queue()

import requests
from bs4 import BeautifulSoup

frontPage = "https://tw.appledaily.com/life/realtime/"
txDate = generateDate("2020-02-01")

def collectUrlByDate(list_tag):
    keepGo = True
    date_list = list_tag.findAll("h1", class_="dddd")
    menu_list = list_tag.findAll("ul", class_="rtddd slvl")
    combined_list = zip(date_list, menu_list)
    for date, menus in combined_list:
        postDate = generateDate(date.getText(), Chinese=True)
        if(postDate > txDate):
            for a in menus.findAll("a"):
                outqueue.put(urlToByteList(a.get("href")))
                print("日期:{}，已蒐集 url :{}".format(postDate, a.get("href")))
        else:
            keepGo = False
            break
    return keepGo



class Processor(PreCrawlerProcessor):
    def fillDataToQueue(self, url) -> BeautifulSoup:
        resp = session.get(url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        list_tag = soup.find("div", class_="abdominis rlby clearmen")
        keepGo = collectUrlByDate(list_tag)
        navBar = soup.find("nav", class_="page_switch lisw fillup")
        if keepGo:
            return navBar
        else:
            return None

    def getNextPage(self, pagesBar) -> str:
        currentPage = pagesBar.find("a", class_="enable")
        nextPage = currentPage.next_sibling
        if nextPage is not None:
            try:
                nextUrl = nextPage.get("href")
                nextUrl = generateAppleUrl(frontPage, nextUrl)
                print("開始下一頁 : ", nextUrl)
                return nextUrl
            except Exception:
                pass


if __name__ == '__main__':
    processor = Processor()
    processor.start(frontPage)