import datetime
from queue import Queue, Empty
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

def extractCutoffDate(date_str):
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return date

frontpage = "https://tw.appledaily.com/life/realtime"
txDate = extractCutoffDate("2020-02-01")
outqueue = Queue()

def startCraw(frontpage):
    getCrawlableInnerPage(frontpage)


## 遞回爬取 Next Page
def getCrawlableInnerPage(frontpage):
    keepGo = True
    print("正在掃描 : " + frontpage)
    resp = requests.get(frontpage)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, features="lxml")
    catalog = soup.find(class_="abdominis rlby clearmen")
    news_list = bindingDateAndArticle(catalog)
    for d, urls in news_list:
        if d >= txDate:
            for u in urls:
                newRecord = []
                newRecord.append(str(d))
                newRecord.append(u)
                outqueue.put(newRecord)
        else:
            keepGo = False
            break

    if keepGo:
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

def bindingDateAndArticle(soup):
    dateTags = soup.findAll("h1", {"class": "dddd"})
    urlTags = soup.findAll("ul", {"class": "rtddd slvl"})
    for i in range(len(dateTags)):
        dateTags[i] = extractDate(dateTags[i].time.text)
    for i in range(len(urlTags)):
        liTags = urlTags[i].findAll("li")
        for j in range(len(liTags)):
            liTags[j] = generateAppleDailyUrl(liTags[j].a.get("href"))
        urlTags[i] = liTags

    aggregation = zip(dateTags, urlTags)
    return aggregation

########## tools ##########

def generateAppleDailyUrl(halfUrl):
    host = urlparse(frontpage)
    return host.scheme + "://" + host.netloc + halfUrl

def extractCutoffDate(date_str):
    date = datetime.datetime.strptime(date_str.strip(), "%Y-%m-%d")
    return date

def extractDate(date_str):
    date = datetime.datetime.strptime(date_str.strip(), "%Y / %m / %d")
    return date


########## tools ##########

if __name__ == "__main__":
    startCraw(frontpage)
    while 1:
        try:
            print(outqueue.get(block=False))
        except Empty:
            break
