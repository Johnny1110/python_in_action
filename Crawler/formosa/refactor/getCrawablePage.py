import requests
from bs4 import BeautifulSoup

from Crawler.formosa.refactor.tools_2 import generateDate, PreCrawlerProcessor, session
from Crawler.formosa.tools import generateFormosaUrl

frontPage = "http://www.my-formosa.com/KM/M_5.htm"
txDate = generateDate("2020-02-01")

# 實作 fillDataToQueue() 與 getNextPage() 就可以了。
class Processor(PreCrawlerProcessor):
    def getCrawablePage(self, url) -> BeautifulSoup:
        resp = session.get(url)
        resp.encoding = 'big5'
        soup = BeautifulSoup(resp.text, features='lxml')
        main_tag = soup.find("div", class_="content")
        for section in main_tag.findAll("section", id="featured-news"):
            try:
                url = {
                    "url": generateFormosaUrl(section.findAll("a")[0].get("href").strip())
                }
                print("已取得URL: ", url)
            except Exception:
                pass



    def getNextPage(self, pagesBar) -> str:
        pass


if __name__ == '__main__':
    processor = Processor()
    processor.start(frontPage)