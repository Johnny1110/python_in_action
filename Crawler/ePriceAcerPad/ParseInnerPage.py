# coding=UTF-8
import datetime

import requests
from bs4 import BeautifulSoup
import GetUrlPage as gup
from DBEntity import Entity

dbData = []

def startCrawInnerPage(url):
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    parseHTML(url, resp.text)


def extractDate(text):
    date = datetime.datetime.strptime(text, "%Y-%m-%d %H:%M")
    return date

def parseEassyContext(url, text):
    entity = Entity()
    entity.set_id(url+'_1')
    entity.set_rid(entity.get_id())
    entity.set_url(url)
    soup = BeautifulSoup(text, features="html.parser")
    entity.set_title(soup.select('h1.title')[0].text)
    entity.set_author(soup.select('a.nickname')[0].text)
    date_str = soup.select('span.date')[0].text[4:].strip()
    entity.set_postDate(extractDate(date_str))
    entity.set_updateDate(entity.get_postDate())
    entity.set_content(soup.select('div.user-comment-block')[0].text)
    entity.set_lang('zh_TW')
    dbData.append(entity)

    print("EassytTitle ->" + entity.get_title())


def parseEassyResponse(url, text, id_index=1):
    soup = BeautifulSoup(text, features="html.parser")
    for resp in soup.findAll("dd", {"class": "enabled"}):
        id_index += 1
        entity = Entity()
        entity.set_author(resp.select("a.nickname")[0].text)
        entity.set_title(soup.select('h1.title')[0].text)
        entity.set_id(url + '_' + str(id_index))
        entity.set_pid(url + '_1')
        entity.set_rid(url + '_1')
        entity.set_url(url)
        entity.set_content(resp.select('div.comment')[0].text)
        entity.set_lang('zh_TW')
        date_str = resp.select('span.date')[0].text[4:].strip()
        entity.set_postDate(extractDate(date_str))
        entity.set_updateDate(entity.get_postDate())
        dbData.append(entity)

    pages =  soup.findAll("a", {"data-name": "page"})
    if not len(pages).__eq__(0):
        nextPageText = pages[-1].text
        if nextPageText.__eq__('下一頁'):
            nextUrl = generateEpriceUrl(pages[-1].get("href"))
            nextResp = requests.get(nextUrl)
            nextResp.encoding = 'utf-8'
            parseEassyResponse(nextUrl, nextResp.text, id_index)


def parseHTML(url, text):
    # 解析內文
    parseEassyContext(url, text)
    # 解析回應
    parseEassyResponse(url, text)

def generateEpriceUrl(halfUrl):
    return "https://www.eprice.com.tw" + halfUrl

if __name__ == '__main__':
    gup.startCraw()
    accessbleUrl = gup.crawlableInnerUrls
    print("所有可爬URL : ")
    print(accessbleUrl)
