import datetime
import re

from bs4 import BeautifulSoup

from Crawler.facebookFansPage.fb_tools import speculateArticlePostDate, login
from Crawler.facebookFansPage.tools_2 import session, PreCrawlerProcessor, generateMFBUrl, generateDate, randomSleep

frontPage = "https://m.facebook.com/YahooTWNews?refid=46&ref=dbl"
txDate = generateDate('2020-01-01')
years_stack = 0

urlList = []

def getNextPageBar(soup):
    pageBar = soup.find("a", text="顯示更多")
    if pageBar is None:
        global years_stack
        years_stack += 1
        targetYear = (txDate.now() - datetime.timedelta(days=years_stack*365)).year
        print("target year: ", targetYear)
        pageBar = soup.find("a", text=re.compile("^{}年$".format(targetYear)))
        print("New Year Bar: ", pageBar)
    return pageBar


class Processor(PreCrawlerProcessor):
    def getCrawablePage(self, url) -> BeautifulSoup:
        print("frontPage url: ", url)
        randomSleep()
        resp = session.get(url)
        session.cookies.save()
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        pageBar = getNextPageBar(soup)
        articles = soup.findAll("article", id=re.compile("^u_0_[0-9]$"))
        for a in articles:
            try:
                abbr = a.find("abbr").getText()
                postDate = speculateArticlePostDate(abbr)
                if postDate is None:
                    continue
                if postDate >= txDate:
                    target = {
                        'url': generateMFBUrl(a.find("a", text="完整動態").get("href"))
                    }
                    urlList.append(target)
                    print("取得文章 postDate: ", postDate, " 取得文章 url: ", target)
                else:
                    pageBar = None
                    break
            except Exception:
                continue
        return pageBar

    def getNextPage(self, pageBar) -> str:
        url = generateMFBUrl(pageBar.get("href"))
        return url

def startCraw():
    processor = Processor()
    processor.start(frontPage)

if __name__ == '__main__':
    login()
    startCraw()
