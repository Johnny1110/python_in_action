from queue import Queue

from Crawler.upMedia.tools import generateDate, PreCrawlerProcessor, generateUpUrl, urlToByteList, randomSleep, \
    dateStrFilter

outqueue = Queue()

import requests
from bs4 import BeautifulSoup

frontPage = "https://www.upmedia.mg/news_list.php?Type=3"
txDate = generateDate("2020-02-01")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
    'Host': 'www.upmedia.mg',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://www.upmedia.mg/'
}

# 實作 fillDataToQueue() 與 getNextPage() 就可以了。
class Processor(PreCrawlerProcessor):
    def fillDataToQueue(self, url) -> BeautifulSoup:
        randomSleep()
        resp = requests.get(url, headers=headers)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        navBar = soup.find("div", id="page")
        items = soup.findAll("dd")
        for item in items:
            try:
                date_tag = item.find("div", class_="time")
                postDate = generateDate(dateStrFilter(date_tag.getText().strip()), Chinese=True)
                if postDate >= txDate:
                    dd = date_tag.parent
                    for div in dd.findAll("div"):
                        div.decompose()
                    url = generateUpUrl(dd.a.get("href"))
                    print("put url : ", url)
                    outqueue.put(urlToByteList(url))
                else:
                    navBar = None
                    break
            except Exception as e:
                box = item.find("div", class_="author")
                box.a.decompose()
                postDate = generateDate(dateStrFilter(box.getText().strip()), Chinese=True)
                if postDate >= txDate:
                    dd = box.parent
                    for div in dd.findAll("div"):
                        div.decompose()
                    url = generateUpUrl(dd.a.get("href"))
                    print("put url : ", url)
                    outqueue.put(urlToByteList(url))
                else:
                    navBar = None
                    break
        return navBar


    def getNextPage(self, pagesBar) -> str:
        if pagesBar is not None:
            activate = pagesBar.find("a", class_="active")
            next_page = activate.next_sibling.get("href")
            if not next_page.__eq__("javascript:void(0);"):
                nextUrl = generateUpUrl("news_list.php" + next_page)
                print("nextUrl : ", nextUrl)
                return nextUrl


if __name__ == '__main__':
    processor = Processor()
    processor.start(frontPage)
    while True:
        try:
            print(outqueue.get(block=False))
        except Exception:
            break