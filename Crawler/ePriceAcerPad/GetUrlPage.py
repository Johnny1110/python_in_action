# coding=UTF-8

import requests
import datetime

from bs4 import BeautifulSoup

# 截止日期 2012-01-01 00:00:00
cutoffDate = datetime.datetime(2019, 10, 16)
# 目標首頁
frontpage = 'https://www.eprice.com.tw/mobile/talk/4544/0/1/'
# 所有可供爬網的 url list
crawlableInnerUrls = []


def startCraw():
    fillCrawlableInnerUrls(frontpage)

def fillCrawlableInnerUrls(url):
    try:
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        keepGo = crawlableUrlfilter(resp.text)
        # 繼續往下爬
        nextPage = getNextPage(url)
        if(nextPage != None) and (keepGo):
            fillCrawlableInnerUrls(generateEpriceUrl(nextPage))
    except Exception as ex:
        print(ex)

def crawlableUrlfilter(html_str):
    keepGo = True
    soup = BeautifulSoup(html_str, features="html.parser")
    date_selector = '.last-respond'
    for d in soup.findAll("ul", {"class": "field-list normal"}):

        if d.find(class_="title text-wrap highlight"):
            continue  # 跳過公告

        dateTag = str(d.select(date_selector))
        dateStr = dateTag[dateTag.index('/\">') + 3 : dateTag.index('</a>')]
        date = ""
        try:
            date = datetime.datetime.strptime(dateStr, "%Y-%m-%d %H:%M")
        except Exception:
            pass
        if (not str(date).__eq__("")) and (date >= cutoffDate):  # 最後回復大於截止日期
            halfUrl = str(d.a.get('href'))
            url = generateEpriceUrl(halfUrl)
            crawlableInnerUrls.append(url)
        else:
            keepGo = False
            break
    return keepGo


def generateEpriceUrl(halfUrl):
    return "https://www.eprice.com.tw" + halfUrl

def getNextPage(thisPage):
    resp = requests.get(thisPage)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, features="html.parser")
    for b in soup.findAll("a", {"data-name": "page"}):
        text = str(b)
        text = text[text.index('\">') + 2 : text.index('</a>')]
        if text.__eq__('下一頁'):
            print(b.get("href"))
            return b.get("href")
            break

if __name__ == "__main__":
    startCraw()
    print(crawlableInnerUrls)

