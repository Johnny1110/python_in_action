import datetime
import re

from bs4 import BeautifulSoup

from Crawler.facebookFansPage.fb_tools import speculateArticlePostDate, login
from Crawler.facebookFansPage.tools_2 import session, PreCrawlerProcessor, generateMFBUrl, generateDate, randomSleep

frontPage = "https://m.facebook.com/apple.realtimenews"
txDate = generateDate('2018-04-10')
years_stack = 0

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
        recent = soup.find("div", id="recent")
        articles = recent.findAll("article")
        for a in articles:
            try:
                abbr = a.find("abbr").getText()
                postDate = speculateArticlePostDate(abbr)
                print("取得文章 url，postDate = ", postDate)
                if postDate >= txDate:
                    target = {
                        'url': generateMFBUrl(a.find("a", text="完整動態").get("href"))
                    }
                    print(target)
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
