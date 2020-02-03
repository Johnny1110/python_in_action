import datetime
import hashlib
import re
import selenium.webdriver as driver

from queue import Queue, Empty
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

import getCrawlablePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

outqueue = Queue()
selenium_driver_path = "D:\Mike_workshop\driver\geckodriver.exe"   #  ./cfg/geckodriver
headless = driver.FirefoxOptions()
headless.add_argument("-headless")  # 無頭模式
headless.set_preference('permissions.default.image', 2)
site = "test_site"


def startParse(d, url):
    print("正在解析 : ", url)
    try:
        article = parseNormalArticle(d, url)
        parseComments(article)
    except Exception as ex:
        print("網頁解析失敗，目標 url : ", url)
        raise e


def collectFBCommentsToArticle(article, browser):
    fb_frame = browser.find_element_by_xpath('//iframe[contains(@title, "fb:comments Facebook Social Plugin")]')
    browser.switch_to.frame(fb_frame)
    locator = (By.CLASS_NAME, '_2pi8')
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located(locator)
    )

    while 1:
        try:
            html = browser.find_element_by_id("facebook")
            html.send_keys(Keys.END)
            loadOtherBtn = browser.find_element_by_tag_name("button")  # load 按鈕
            loadOtherBtn.click()
            browser.implicitly_wait(3)
        except NoSuchElementException:
            break
    commentSoup = BeautifulSoup(browser.page_source, features="lxml")
    article.commentSoup = commentSoup




def parseNormalArticle(d, url):
    article = Entity()
    browser = driver.Firefox(executable_path=selenium_driver_path, options=None)
    browser.get(url)
    try:
        locator = (By.XPATH, '//iframe[contains(@title, "fb:comments Facebook Social Plugin")]')
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located(locator)
        )
        soup = BeautifulSoup(browser.page_source, features="lxml")
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

        collectFBCommentsToArticle(article, browser)
    except Exception as e:
        print("非正常頁面，使用特殊格式解析.")
        article = parseSpecialArticle(d, url, browser)
    finally:
        browser.close()
        browser.quit()
        return article


def parseSpecialArticle(d, url, browser):
    try:
        locator = (By.XPATH, '//iframe[contains(@title, "fb:comments Facebook Social Plugin")]')
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(locator)
        )
        soup = BeautifulSoup(browser.page_source, features="lxml")
        resultHeader = soup.find("div", {"class": "article__header"}).text
        resultBody = soup.find("div", {"id": "articleBody"}).text
        article = Entity()
        article.url = url
        article.authorName = extractAuthor(resultBody)
        article.postTitle = resultHeader
        article.content = resultBody
        article.articleDate = d
        article.postId = toMD5(url)
        article.site = site
        article.rid = article.postId
        article.pid = ""
        outqueue.put(article.toList())

        collectFBCommentsToArticle(article, browser)
        return article
    except Exception as ex:
        print("特殊格式解析失敗.")


def parseComments(article):
    soup = article.commentSoup
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
    author = re.search("[（(].{1,10}／.*報導[)）]", appleContent)
    return author.group() if author is not None else ""
########## tools ##########

if __name__ == "__main__":
    #getCrawlablePage.startCraw("https://tw.news.appledaily.com/politics/realtime")  # 政治板 (一般)
    getCrawlablePage.startCraw("https://tw.lifestyle.appledaily.com/gadget/realtime")  # 3C板 (特殊版)
    inqueue = getCrawlablePage.outqueue
    while 1:
        try:
            url_list = inqueue.get(block=False)
            for li in url_list:
                startParse(li[0], li[1])
        except Empty:
            break

    while 1:
        try:
            out_list = outqueue.get(block=False)
            for out in out_list:
                print(out)
        except Empty:
            break
