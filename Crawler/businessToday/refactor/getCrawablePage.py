import requests
from bs4 import BeautifulSoup

from Crawler.businessToday.refactor.tools_2 import generateDate, PreCrawlerProcessor, session

frontPage = "https://www.businesstoday.com.tw/catalog/80391"
txDate = generateDate("2020-06-01")

pageNum = 1
overFlow = 0  # 當截止日期條件滿足 3 個再離開

# 實作 fillDataToQueue() 與 getNextPage() 就可以了。
class Processor(PreCrawlerProcessor):
    def getCrawablePage(self, url) -> BeautifulSoup:
        resp = session.get(url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        li_tags = soup.findAll("a", class_="article__item")
        if li_tags is not None:
            for a in li_tags:
                postDate = generateDate(a.find("p", class_="article__item-date").text)
                if postDate >= txDate:
                    data = {
                        'url': a.get("href").strip()
                    }
                    print("蒐集到 URL: ", data)
                else:
                    global overFlow
                    overFlow += 1
                    if overFlow >= 3:
                        soup = None
                        break
        global pageNum
        pageNum += 1
        return soup

    def getNextPage(self, pagesBar) -> str:
        return generateAjaxQuery(frontPage, pageNum)


def generateAjaxQuery(url, page):
    if page < 1000:
        return "{}/list/page/{}/ajax".format(url, page)
    else:
        return None


if __name__ == '__main__':
    processor = Processor()
    processor.start(frontPage)