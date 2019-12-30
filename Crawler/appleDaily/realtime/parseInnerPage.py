import datetime
import hashlib
import time
from queue import Queue, Empty

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

from Crawler.appleDaily.realtime.getCrawlablePage import startCraw
from Crawler.appleDaily.realtime import getCrawlablePage
import selenium.webdriver as driver

outqueue = Queue()
selenium_driver_path = "D:\Mike_workshop\driver\chromedriver.exe"
site = "test_site"

def startParse(url):
    article = parseArticle(url)
    parseComments(article)



def parseArticle(url):
    article = Entity()
    ## 待實作 ##
    return article



def parseComments(article):
    browser = driver.Chrome(executable_path=selenium_driver_path)
    browser.get(article.url)
    fb_frame = browser.find_element_by_xpath('//iframe[contains(@title, "fb:comments Facebook Social Plugin")]')
    print(fb_frame.get_attribute("name"))
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
    commentsBlock = soup.findAll(class_="_3-8y _5nz1 clearfix")
    for i in range(len(commentsBlock)):
        parent = fillParentCommentDataToQueue(commentsBlock[i], article, i)
        fillChildCommentDataToQueue(commentsBlock[i].find("div", {"class": "_44ri _2pis"}), parent)



def fillParentCommentDataToQueue(commentTag, article, index):
    comment = Entity()
    comment.parent = article
    comment.index = index
    comment.url = article.url
    comment.authorName = commentTag.find("span", {"class": "UFICommentActorName"}).text
    comment.postTitle = article.postTitle
    comment.content = commentTag.find("span", {"class": "_5mdd"}).text
    comment.articleDate = commentTag.find("abbr", {"class": "UFISutroCommentTimestamp livetimestamp"}).text
    comment.postId = toMD5("{}_{}".format(comment.url, index))
    comment.site = site
    comment.rid = article.postId
    comment.pid = article.postId
    outqueue.put(comment.toList())
    return comment


def fillChildCommentDataToQueue(childCommentTag, parent):
    replys = childCommentTag.findAll("div", {"class": "_3-8y clearfix"})
    for i in range(len(replys)):
        reply = Entity()
        reply.url = parent.url
        reply.authorName = replys[i].find("a", {"class":"UFICommentActorName"})
        reply.postTitle = parent.postTitle
        reply.content = replys[i].find("span", {"class":"_5mdd"})
        reply.articleDate = replys[i].find("abbr", {"class": "UFISutroCommentTimestamp livetimestamp"}).text
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
        newRecord.append(self.postId)
        newRecord.append(self.site)
        newRecord.append(self.rid)
        newRecord.append(self.pid)
        return newRecord

def msTransToDate(param):
    sec = int(param)
    return datetime.datetime.fromtimestamp(sec).__str__()

def toMD5(data):
    m = hashlib.md5()
    m.update(data.encode("utf-8"))
    return m.hexdigest()
########## tools ##########

if __name__ == "__main__":
    startCraw()
    inqueue = getCrawlablePage.outqueue
    while 1:
        try:
            url_list = inqueue.get(block=False)
            for url in url_list:
                startParse(url)
        except Empty:
            break
