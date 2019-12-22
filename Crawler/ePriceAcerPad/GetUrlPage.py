# coding=UTF-8

import requests
import datetime

from bs4 import BeautifulSoup

# 截止日期 2012-01-01 00:00:00
cutoffDate = datetime.datetime(2019, 12, 22)
# 目標首頁
frontpage = 'https://www.eprice.com.tw/mobile/talk/4546/0/1/'
# 所有可供爬網的 url list
crawlableInnerUrls = []


def startCraw():
    fillCrawlableInnerUrls(frontpage)

def fillCrawlableInnerUrls(url):
    try:
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        crawlableUrlfilter(resp.text)
        # 繼續往下爬
        nextPage = getNextPage(url)
        if(nextPage != None):
            fillCrawlableInnerUrls(generateEpriceUrl(nextPage))
    except Exception as ex:
        print(ex)

def crawlableUrlfilter(html_str):
    soup = BeautifulSoup(html_str, features="html.parser")
    date_selector = '.last-respond'
    for d in soup.findAll("ul", {"class": "field-list normal"}):
        dateTag = str(d.select(date_selector))
        dateStr = dateTag[dateTag.index('/\">') + 3 : dateTag.index('</a>')]
        date = datetime.datetime.strptime(dateStr, "%Y-%m-%d %H:%M")
        if date >= cutoffDate: # 最後回復大於截止日期
            print(dateTag)
            halfUrl = str(d.a.get('href'))
            url = generateEpriceUrl(halfUrl)
            crawlableInnerUrls.append(url)


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

