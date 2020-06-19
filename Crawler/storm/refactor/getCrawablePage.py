from bs4 import BeautifulSoup

from Crawler.storm.refactor.tools_2 import generateDate, PreCrawlerProcessor, session, generateStormUrl

frontPage = "https://www.storm.mg/category/118"
txDate = generateDate("2020-06-01")

# 實作 fillDataToQueue() 與 getNextPage() 就可以了。
class Processor(PreCrawlerProcessor):
    def getCrawablePage(self, url) -> BeautifulSoup:
        resp = session.get(url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        pageBar = soup.find("div", class_="pages_wrapper pagination_content")
        items = soup.findAll("div", {"class": "category_card card_thumbs_left"})
        for it in items:
            date_str = it.find("span", class_="info_time")
            postDate = generateDate(date_str.text)
            if postDate > txDate:
                data = {
                    "url": it.find("a", class_="card_link link_img").get("href")
                }
                print("取得文章URL: ", data)
            else:
                pageBar = None
                break

        return pageBar

    def getNextPage(self, pagesBar) -> str:
        currentPageTag = pagesBar.find("a", class_="pages active")
        if not str(currentPageTag.text).__eq__("100"):  # 超過 100 頁會 404
            nextPageTag = currentPageTag.find_next_sibling('a')
            nextPageUrl = generateStormUrl(nextPageTag.get("href"))
            return nextPageUrl


if __name__ == '__main__':
    processor = Processor()
    processor.start(frontPage)