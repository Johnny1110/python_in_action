import datetime

from bs4 import BeautifulSoup

from Crawler.facebookFansPage.fb_date_tools import speculateArticlePostDate
from Crawler.facebookFansPage.tools_2 import session, PreCrawlerProcessor, generateMFBUrl, generateDate

frontPage = "https://m.facebook.com/apple.realtimenews?refid=46&ref=dbl"
txDate = generateDate('2020-03-23')

def login():
    data = {
        'lsd': 'AVq1Hm_O',
        'jazoest': '2668',
        'li': 'AEp4XssNBBL4pR5EvIMg-jEb',
        'try_number': '0',
        'unrecognized_tries': '0',
        'm_ts': str(int(datetime.datetime.now().timestamp())),
        'email': 'FrizoStudio@gmail.com',
        'pass': 'Frizo1234',
        'login': '登入',
    }
    url = "https://m.facebook.com/login/device-based/regular/login/?refsrc=https%3A%2F%2Fm.facebook.com%2Flogin%2F%3Fref%3Ddbl&lwv=100&ref=dbl"
    resp = session.post(url=url, data=data)
    session.cookies.save()
    resp.encoding = 'utf-8'
    print('cookies: ', session.cookies)


def startCraw():
    resp = session.get(frontPage)
    session.cookies.save()
    pass

class Processor(PreCrawlerProcessor):
    def getCrawablePage(self, url) -> BeautifulSoup:
        print("frontPage url: ", url)
        resp = session.get(url)
        session.cookies.save()
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        pageBar = soup.find("a", text="顯示更多")
        articles = soup.findAll("div", {"role": "article"})
        for a in articles:
            try:
                abbr = a.find("abbr").getText()
                postDate = speculateArticlePostDate(abbr)
                print(postDate)
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
