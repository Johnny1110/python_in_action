from bs4 import BeautifulSoup

from Crawler.facebookFansPage.fb_tools import speculateArticlePostDate, login
from Crawler.facebookFansPage.tools_2 import session, PreCrawlerProcessor, generateMFBUrl, generateDate, randomSleep

frontPage = "https://m.facebook.com/apple.realtimenews?refid=46&ref=dbl"
txDate = generateDate('2020-01-01')



class Processor(PreCrawlerProcessor):
    def getCrawablePage(self, url) -> BeautifulSoup:
        print("frontPage url: ", url)
        randomSleep()
        resp = session.get(url)
        session.cookies.save()
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        pageBar = soup.find("a", text="顯示更多")
        print("soup :: ", soup)
        print("pageBar :: ", pageBar)
        articles = soup.findAll("div", {"role": "article"})
        for a in articles:
            try:
                abbr = a.find("abbr").getText()
                postDate = speculateArticlePostDate(abbr)
                print("postDate = ", postDate)
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
