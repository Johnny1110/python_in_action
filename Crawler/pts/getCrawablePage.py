from queue import Queue

from Crawler.pts.tools import generateDate, PreCrawlerProcessor, getTitlesUrl, urlToByteList, generatePTSUrl

outqueue = Queue()

import requests
from bs4 import BeautifulSoup

frontPage = "https://news.pts.org.tw/category/2"
txDate = generateDate("2020-02-01")


def startParseUrl(main_tag):
    keepGo = True
    boxes = main_tag.findAll("div", class_="sweet-info flex-center")
    for box in boxes:
        date_str = box.i.find_next_sibling('span').getText()
        postDate = generateDate(date_str)
        if postDate >= txDate:
            url = box.parent.a.get("href")
            outqueue.put(urlToByteList(url))
        else:
            keepGo = False
            break
    return keepGo


def parseMoreUrl(cid, page):
    url = "https://news.pts.org.tw/subcategory/category_more.php"
    postData = {
        "cid": cid,
        "page": str(page),
    }
    resp = requests.post(url, data=postData)
    jsonData = resp.json()
    keepGo = True
    print("cid={}, page={}, json={}".format(cid, page, jsonData))
    if len(jsonData) is not 0:
        for data in jsonData:
            postDate = generateDate(data['news_date'])
            if postDate >= txDate:
                url = generatePTSUrl(data['news_id'])
                outqueue.put(urlToByteList(url))
            else:
                keepGo = False
                break
    else:
        keepGo = False

    if keepGo:
        parseMoreUrl(cid, page+1)


class Processor(PreCrawlerProcessor):
    def fillDataToQueue(self, url) -> BeautifulSoup:
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features="lxml")
        main_tag = soup.find("div", class_="col-md-9 col-sm-12 col-xs-12")
        keepGo = startParseUrl(main_tag)
        if keepGo:
            cid = url.split('/')[-1]
            page = 1
            parseMoreUrl(cid, page)




    def getNextPage(self, nextPageNum) -> str:
        pass


if __name__ == '__main__':
    titleUrls = getTitlesUrl(frontPage)
    processor = Processor()
    for url in titleUrls:
        processor.start(url)

    while True:
        try:
            url = outqueue.get(block=False)
            print(url)
        except Exception:
            break

