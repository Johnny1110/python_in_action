from queue import Queue

from Crawler.ptt.tools import generateDate, PreCrawlerProcessor, headers, cookies, generatePTTUrl

outqueue = Queue()

import requests
from bs4 import BeautifulSoup

frontPage = "https://www.ptt.cc/bbs/Gossiping/index.html"
txDate = generateDate("2020-02-01")

def getIfDateSatisfy(page_soup):
    date_desc = page_soup.find("span", text="時間")
    date_str = date_desc.next_sibling.getText()
    postDate = generateDate(date_str)
    if postDate >= txDate:
        return page_soup


def cleanAnnouncement(soup):
    r_ents = soup.findAll("div", class_="r-ent")
    line = soup.find("div", class_="r-list-sep")
    if line is not None:
        announcements = line.next_siblings
        for i in announcements:
            try:
                r_ents.remove(i)
            except Exception:
                pass

    return r_ents


class Processor(PreCrawlerProcessor):
    def fillDataToQueue(self, url) -> BeautifulSoup:
        resp = requests.get(url, headers=headers, cookies=cookies)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        pagesBar = soup.find("div", class_="btn-group btn-group-paging")
        r_ent_tags = cleanAnnouncement(soup.find("div", class_="r-list-container action-bar-margin bbs-screen"))
        for r_ent in r_ent_tags:
            url = generatePTTUrl(r_ent.find("div", class_="title").a.get("href"))
            innerPage = requests.get(url, headers=headers, cookies=cookies)
            page_soup = BeautifulSoup(innerPage.text, features='lxml')
            html = getIfDateSatisfy(page_soup)
            if html is not None:
                map = {
                    "url": url,
                    "html": html
                }
                print(map['url'])
                # mySender(map)
            else:
                pagesBar = None
                break

        return pagesBar

    def getNextPage(self, pagesBar) -> str:
        prePage = pagesBar.find("a", text="‹ 上頁")
        href = generatePTTUrl(prePage.get("href"))
        if href is not None:
            print("下一頁 : ", href)
            return href

if __name__ == '__main__':
    processor = Processor()
    processor.start(frontPage)