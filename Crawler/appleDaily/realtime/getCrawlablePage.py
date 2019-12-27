from queue import Queue, Empty

import requests
from bs4 import BeautifulSoup

frontpage = "https://tw.news.appledaily.com/politics/realtime/15"

outqueue = Queue()

def startCraw():
    getCrawlableInnerPage(frontpage)
    pass


## 遞回爬取 Next Page
def getCrawlableInnerPage(frontpage):
    print("正在掃描 : " + frontpage)
    resp = requests.get(frontpage)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, features="lxml")
    news_list = soup.find(class_="abdominis rlby clearmen")
    news_li_tags = news_list.findAll("li")
    newrecord = []
    for tag in news_li_tags:
        newrecord.append(generateAppleDailyUrl(tag.a.get("href")))
    outqueue.put(newrecord)
    nextPageUrl = getNextPageUrl(soup)
    if (not nextPageUrl == None) and (not nextPageUrl.strip().__eq__("")):
        getCrawlableInnerPage(nextPageUrl)


def getNextPageUrl(soup):
    try:
        currentPageTag = soup.find(class_="enable")
        nextPageTag = currentPageTag.next_sibling
        return generateAppleDailyUrl(nextPageTag.get("href"))
    except AttributeError:
        pass

########## tools ##########

def generateAppleDailyUrl(halfUrl):
    return "https://tw.news.appledaily.com" + halfUrl

########## tools ##########

if __name__ == "__main__":
    startCraw()
    while 1:
        try:
            print(outqueue.get(block=False))
        except Empty:
            break
