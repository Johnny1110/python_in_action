import re

import requests
from bs4 import BeautifulSoup

from Crawler.EYNY.tools_2 import generateDate, PreCrawlerProcessor, generateEYNYUrl, headers

frontPage = "http://www36.eyny.com/forum-526-3D41XTMV.html"
txDate = generateDate("2020-01-01")

cookies = {
    "612e55XbD_e8d7_agree": "1",
    "612e55XbD_e8d7_videoadult": "1",
}

class Processor(PreCrawlerProcessor):
    def getCrawablePage(self, url) -> BeautifulSoup:
        resp = requests.get(url, cookies=cookies, headers=headers)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        nextPageBar = soup.find("div", class_="pg")
        moderate = soup.find("form", id="moderate")
        stickthreads = moderate.findAll("tbody")
        if str(moderate).__contains__("id=\"separatorline\""):  # 去除公告
            for index, stick in enumerate(stickthreads):
                if (stick.get("id").__eq__("separatorline")):
                    stickthreads = stickthreads[index+1:]

        for stick in stickthreads:
            a_Tags = stick.findAll("a")
            time_area = a_Tags[-1]
            date_matcher = re.search("([1-9][0-9][0-9][0-9]-[1]*[0-9]+-[1-3]*[0-9].*?[AP]M)", str(time_area))
            postDate_str = date_matcher.group(0)
            postDate = generateDate(postDate_str)
            if (postDate >= txDate):
                url = {
                    "url": generateEYNYUrl(a_Tags[0].get("href")),
                    "postDate": str(postDate)
                }
                print(url)
            else:
                nextPageBar = None
                break

        return nextPageBar

    def getNextPage(self, pagesBar) -> str:
        nextPageTag = pagesBar.find("a", text="下一頁")
        nextUrl = generateEYNYUrl(nextPageTag.get("href"))
        return nextUrl


if __name__ == '__main__':
    processor = Processor()
    processor.start(frontPage)