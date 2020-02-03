import datetime
import hashlib
import re
from queue import Queue
import selenium.webdriver as driver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Crawler.nextmgzNews import getCrawablePage

driver_path = "D:\Mike_workshop\driver\geckodriver.exe"
headless = driver.FirefoxOptions()
headless.add_argument("-headless")  # 無頭模式
headless.set_preference('permissions.default.image', 2)
outqueue = Queue()
site = "test_site_id"





def startParse(url):
    browser = driver.Firefox(executable_path=driver_path)
    browser.get(url)
    try:
        locator = (By.XPATH, '//iframe[contains(@title, "fb:comments Facebook Social Plugin")]')
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located(locator)
        )
        soup = BeautifulSoup(browser.page_source, features="lxml")
        article = parseArticle(url, soup.find("article"))
        collectFBCommentsToArticle(article, browser)
        browser.close()
        browser.quit()
        parseComments(article)
    except Exception as ex:
        print("網頁解析失敗 : ", url)


def parseArticle(url, soup):
    article = Entity()
    article.url = url
    article.postTitle = soup.find("header").h2.text
    article.articleDate = extractArticleDate(soup.find("time", {"class": "time"}).text)
    content = soup.find("div", {"class": "article-content"})
    article.content = ''
    for p in content.find_all("p"):
        article.content += p.text
    article.authorName = extractAuthor(article.content)
    article.site = site
    article.postId = toMD5(url)
    article.rid = article.postId
    article.pid = ""
    outqueue.put(article.toList())
    return article

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


###### tools ######
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


def extractAuthor(content):  # ex:（撰文╱特約記者傅紀鋼　攝影╱蘇立坤）
    match = re.search("（撰文.+?）", content)
    return match.group() if match is not None else "?"

def extractArticleDate(date_str):
    date = datetime.datetime.strptime(date_str.strip(), "%Y年%m月%d日")
    return date
####################

if __name__ == '__main__':
    fontpage = "https://tw.nextmgz.com/breakingnews/news"
    urlqueue = getCrawablePage.outqueue
    getCrawablePage.startParse(fontpage)
    while True:
        try:
            url = urlqueue.get(block=False)
            startParse(url)
        except Exception as ex:
            break

    while True:
        try:
            data = outqueue.get(block=False)
            for item in data:
                print(item)
                print("---"*20)
        except Exception:
            break
