import datetime
import hashlib
import time
import requests
import re
from queue import Queue, Empty

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

import getCrawlablePage
import selenium.webdriver as driver

outqueue = Queue()
selenium_driver_path = "D:/lab/selenium_driver/chromedriver.exe"
site = "test_site"

def startParse(url):
    article = parseArticle(url)
    parseComments(article)



def parseArticle(url):
    resp = requests.get(url)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, features="lxml")
    article = Entity()
    article.url = url
    article.authorName = extractAuthor(soup.find("div", {"class": "ndArticle_margin"}).p.text)
    article.postTitle = soup.find("hgroup").h1.text
    article.content = soup.find("div", {"class": "ndArticle_margin"}).p.text
    article.articleDate = extractDate(soup.find("hgroup").div.text)
    article.postId = toMD5(url)
    article.site = site
    article.rid = article.postId
    article.pid = ""
    outqueue.put(article.toList())

    return article



def parseComments(article):
    browser = driver.Chrome(executable_path=selenium_driver_path)
    browser.get(article.url)
    fb_frame = browser.find_element_by_xpath('//iframe[contains(@title, "fb:comments Facebook Social Plugin")]')
    browser.switch_to.frame(fb_frame)
    time.sleep(3)
    while 1:
        try:
            loadOtherBtn = browser.find_element_by_tag_name("button")  # load 按鈕
            loadOtherBtn.click()
            browser.implicitly_wait(3)
        except NoSuchElementException:
            break
    soup = BeautifulSoup(browser.page_source, features="lxml")
    browser.close()
    browser.quit()
    commentsBlock = soup.findAll(class_="_3-8y _5nz1 clearfix")
    for i in range(len(commentsBlock)):
        parent = fillParentCommentDataToQueue(commentsBlock[i], article, i)
        fillChildCommentDataToQueue(commentsBlock[i].find("div", {"class": "_44ri _2pis"}), parent)



def fillParentCommentDataToQueue(commentTag, article, index):
    comment = Entity()
    comment.parent = article
    comment.index = index
    comment.url = article.url
    comment.authorName = "???"
    try:
        comment.authorName = commentTag.find("a", {"class": "UFICommentActorName"}).text
    except Exception:
        comment.authorName = commentTag.find("span", {"class": "UFICommentActorName"}).text
    comment.postTitle = article.postTitle
    try:
        comment.content = commentTag.find("span", {"class": "_5mdd"}).text ## 沒有 _5mdd 的話，回復就只是貼圖
    except Exception:
        comment.content = "圖片回復"
    comment.articleDate = sTransToDate(commentTag.find("abbr", {"class": "UFISutroCommentTimestamp livetimestamp"}).get("data-utime"))
    comment.postId = toMD5("{}_{}".format(comment.url, index))
    comment.site = site
    comment.rid = article.postId
    comment.pid = article.postId
    outqueue.put(comment.toList())
    return comment


def fillChildCommentDataToQueue(childCommentTag, parent):
    if childCommentTag is not None:
        replys = childCommentTag.findAll("div", {"class": "_3-8y clearfix"})
        for i in range(len(replys)):
            reply = Entity()
            reply.url = parent.url
            reply.authorName = "???"
            try:
                reply.authorName = replys[i].find("a", {"class":"UFICommentActorName"}).text
            except Exception:
                reply.authorName = replys[i].find("span", {"class": "UFICommentActorName"}).text
            reply.postTitle = parent.postTitle
            try:
                reply.content = replys[i].find("span", {"class":"_5mdd"}).text
            except Exception:
                reply.content = "圖片回復"
            reply.articleDate = sTransToDate(replys[i].find("abbr", {"class": "UFISutroCommentTimestamp livetimestamp"}).get("data-utime"))
            reply.postId = toMD5("{}_{}_{}".format(reply.url, parent.index, i))
            reply.site = site
            reply.rid = parent.postId
            reply.pid = parent.parent.postId
            outqueue.put(reply.toList())



########## tools ##########
class Entity(object):
    def __init__(self):
        pass

    def toList(self):
        newRecord = []
        newRecord.append(self.url)
        newRecord.append(self.authorName)
        newRecord.append(self.postTitle)
        newRecord.append(self.content)
        newRecord.append(self.articleDate)
        newRecord.append(self.site)
        newRecord.append(self.postId)
        newRecord.append(self.rid)
        newRecord.append(self.pid)
        return newRecord

def sTransToDate(param):
    sec = int(param.strip())
    return datetime.datetime.fromtimestamp(sec).__str__()

def toMD5(data):
    m = hashlib.md5()
    m.update(data.encode("utf-8"))
    return m.hexdigest()

def extractDate(dateStr): ## 出版時間：2019/12/30 12:33
    dateStr = dateStr.strip()
    return datetime.datetime.strptime(dateStr[5:], "%Y/%m/%d %H:%M").__str__()

def extractAuthor(appleContent):
    author = re.search("（.{3,10}／.*報導）", appleContent)
    return author.group() if author is not None else ""
########## tools ##########

if __name__ == "__main__":
    getCrawlablePage.startCraw()
    inqueue = getCrawlablePage.outqueue
    while 1:
        try:
            url_list = inqueue.get(block=False)
            for url in url_list:
                startParse(url)
        except Empty:
            break
