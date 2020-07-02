import requests
from bs4 import BeautifulSoup

from Crawler.commonWealth.refactor.tools_2 import generateDate, PreCrawlerProcessor, session

frontPage = "https://www.cw.com.tw/masterChannel.action?idMasterChannel=9"
txDate = generateDate("2020-06-01")

# 實作 fillDataToQueue() 與 getNextPage() 就可以了。
class Processor(PreCrawlerProcessor):
    def getCrawablePage(self, url) -> BeautifulSoup:
        resp = session.get(url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')

        pagination = soup.find("ul", class_="pagination")

        li_tags = soup.findAll("div", class_="caption")
        for li in li_tags:
            postDate = generateDate(li.time.text.strip())
            if postDate >= txDate:
                href = li.h3.a.get("href").strip()
                url = {
                    "url": href
                }
                print("蒐集目標情資: ", url)
            else:
                pagination = None
                break

        return pagination


    def getNextPage(self, pagesBar) -> str:
        nextTag = pagesBar.find("li", class_="next")
        if nextTag is not None:
            return nextTag.a.get("href")
        else:
            print("到最後一頁拉..")


if __name__ == '__main__':
    processor = Processor()
    processor.start(frontPage)