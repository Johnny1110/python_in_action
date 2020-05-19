import requests
from bs4 import BeautifulSoup

from Crawler.ePrice.tools_2 import generateDate, PreCrawlerProcessor, session, generateEpriceUrl

frontPage = "https://www.eprice.com.tw/mobile/talk/4544/0/1/"
txDate = generateDate("2020-04-01")

# 實作 fillDataToQueue() 與 getNextPage() 就可以了。
class Processor(PreCrawlerProcessor):
    def getCrawablePage(self, url) -> BeautifulSoup:
        resp = session.get(url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        pageBar = soup.findAll("a", {"data-name": "page"})
        for d in soup.findAll("ul", {"class": "field-list normal"}):
            if d.find(class_="title text-wrap highlight"):
                continue  # 跳過公告

            dateTag = str(d.select('.last-respond'))
            dateStr = dateTag[dateTag.index('/\">') + 3: dateTag.index('</a>')]
            postDate = generateDate(dateStr)

            if postDate >= txDate:
                url = {
                    "url": generateEpriceUrl(d.a.get('href'))
                }
                print("蒐集 : ", url)
            else:
                pageBar = None
                break

        return pageBar

    def getNextPage(self, pagesBar) -> str:
        for a in pagesBar:
            text = str(a)
            text = text[text.index('\">') + 2: text.index('</a>')]
            if text.__eq__('下一頁'):
                return generateEpriceUrl(a.get("href"))


if __name__ == '__main__':
    processor = Processor()
    processor.start(frontPage)