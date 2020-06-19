import requests
from bs4 import BeautifulSoup

from Crawler.gvm.refactor.tools_2 import generateDate, PreCrawlerProcessor, session

frontPage = "https://www.gvm.com.tw/category/business"
txDate = generateDate("2020-04-01")

# 實作 fillDataToQueue() 與 getNextPage() 就可以了。
class Processor(PreCrawlerProcessor):
    def getCrawablePage(self, url) -> BeautifulSoup:
        resp = session.get(url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        pagesBar = soup.find("ul", class_="article-list__pagination")
        main_tag = soup.find("div", id="article_list")
        url_tags = main_tag.findAll("div", class_="article-list-item__intro")
        for item in url_tags:
            postDate = generateDate(item.find("div", class_="time").text.strip())
            if postDate >= txDate:
                url = {
                    "url": item.findAll("a")[0].get("href").strip()
                }
                print(url)
            else:
                pagesBar = None
                break

        return pagesBar

    def getNextPage(self, pagesBar) -> str:
        if pagesBar is not None:
            currentPage = pagesBar.find("li", class_="active")
            nextPageTag = currentPage.next_sibling
            if nextPageTag is not None:
                nextUrl = nextPageTag.find("a").get("href").strip()
                return nextUrl


if __name__ == '__main__':
    processor = Processor()
    processor.start(frontPage)