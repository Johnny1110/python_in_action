import requests
from bs4 import BeautifulSoup

from Crawler.newsMarket.refactor.tools_2 import generateDate, PreCrawlerProcessor, session

frontPage = "https://www.newsmarket.com.tw/recent/"
txDate = generateDate("2020-06-01")

# 實作 fillDataToQueue() 與 getNextPage() 就可以了。
class Processor(PreCrawlerProcessor):
    def getCrawablePage(self, url) -> BeautifulSoup:
        resp = session.get(url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        news_list = soup.find("section", class_="recent-posts")
        navBar = news_list.find("div", class_="navigation")
        for news in news_list.findAll("section", class_="entry-body"):
            date_str = news.find("time", class_="entry-date").get("datetime")
            postDate = generateDate(date_str)
            if postDate > txDate:
                url = {
                    "url": news.find("h3", class_="entry-title").a.get("href")
                }
                print("目標 date:{}, url:{}".format(postDate, url))
            else:
                navBar = None
                break
        return navBar

    def getNextPage(self, pagesBar) -> str:
        link_tag = pagesBar.find("a", class_="next page-numbers")
        if link_tag is not None:
            return link_tag.get("href")


if __name__ == '__main__':
    processor = Processor()
    processor.start(frontPage)