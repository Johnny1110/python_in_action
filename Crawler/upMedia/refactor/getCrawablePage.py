from bs4 import BeautifulSoup

from Crawler.upMedia.refactor.tools_2 import generateDate, PreCrawlerProcessor, session, randomSleep, dateStrFilter, \
    generateUpUrl

frontPage = "https://www.upmedia.mg/news_list.php?Type=3"
txDate = generateDate("2020-04-20")

# 實作 fillDataToQueue() 與 getNextPage() 就可以了。
class Processor(PreCrawlerProcessor):
    def getCrawablePage(self, url) -> BeautifulSoup:
        resp = session.get(url)
        resp.encoding = 'utf-8'
        randomSleep()
        soup = BeautifulSoup(resp.text, features='lxml')
        navBar = soup.find("div", id="page")
        items = soup.findAll("dd")
        for item in items:
            try:
                date_tag = item.find("div", class_="time")
                postDate = generateDate(dateStrFilter(date_tag.getText().strip()), Chinese=True)
                if postDate >= txDate:
                    print("postDate: ", postDate)
                    sendUrlData(date_tag.parent)
                else:
                    navBar = None
                    break
            except Exception as e:
                print(e)
                box = item.find("div", class_="author")
                box.a.decompose()
                postDate = generateDate(dateStrFilter(box.getText().strip()), Chinese=True)
                if postDate >= txDate:
                    sendUrlData(box.parent)
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


def sendUrlData(elem):
    for div in elem.findAll("div"):
        div.decompose()
    data = {
        "url": generateUpUrl(elem.a.get("href"))
    }
    print("取得 url : ", data['url'])


if __name__ == '__main__':
    processor = Processor()
    processor.start(frontPage)