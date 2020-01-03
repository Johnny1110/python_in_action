import datetime
from queue import Queue, Empty

import requests
from bs4 import BeautifulSoup

def extractCutoffDate(date_str):
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return date

frontpage = "https://tw.news.appledaily.com/politics/realtime"
txDate = extractCutoffDate("2020-01-03")
outqueue = Queue()

def startCraw():
    getCrawlableInnerPage(frontpage)
    pass


## 遞回爬取 Next Page
def getCrawlableInnerPage(frontpage):
    keepGo = True
    print("正在掃描 : " + frontpage)
    resp = requests.get(frontpage)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, features="lxml")
    catalog = soup.find(class_="abdominis rlby clearmen")
    news_list = bindingDateAndArticle(catalog)
    newRecord = []
    for d, urls in news_list:
        if d >= txDate:
            for u in urls:
                newRecord.append([str(d), u])
        else:
            keepGo = False
            break
    outqueue.put(newRecord)

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
    return "https://tw.news.appledaily.com" + halfUrl

def extractCutoffDate(date_str):
    date = datetime.datetime.strptime(date_str.strip(), "%Y-%m-%d")
    return date

def extractDate(date_str):
    date = datetime.datetime.strptime(date_str.strip(), "%Y / %m / %d")
    return date


########## tools ##########

if __name__ == "__main__":
    startCraw()
    while 1:
        try:
            print(outqueue.get(block=False))
        except Empty:
            break
