import requests
from bs4 import BeautifulSoup

frontPage = "#"
txDate = generateDate("2020-02-01")

# 實作 fillDataToQueue() 與 getNextPage() 就可以了。
class Processor(PreCrawlerProcessor):
    def getCrawablePage(self, url) -> BeautifulSoup:
        resp = session.get(url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')

    def getNextPage(self, pagesBar) -> str:
        pass


if __name__ == '__main__':
    processor = Processor()
    processor.start(frontPage)