import datetime
import hashlib
import re
import sqlite3
from http import cookiejar
import random

import requests

from abc import abstractmethod
from bs4 import BeautifulSoup
from dateutil.parser import parse

site = '${SITENAME}'

db_file = "eyny_fakeAcc.db"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
    'Accept': 'text/html,application/xhtml+xml,application/json;q=0.9,image/webp,*/*;q=0.8',
}

session = requests.session()
session.headers = headers
session.cookies = cookiejar.LWPCookieJar(filename="LibCookies.txt")
session.cookies.save()

# proxies = {
#     'http': 'socks5h://localhost:9150',
#     'https': 'socks5h://localhost:9150',
# }
# session.proxies = proxies


def toMD5(data):
    m = hashlib.md5()
    m.update(data.encode("utf-8"))
    return m.hexdigest()

def generateDate(date_str):
    return parse(date_str).replace(microsecond=0, tzinfo=None)

# define
def generateEYNYUrl(target):
    return "http://www36.eyny.com/" + target

# define
def extractAuthorName(content_str):
    author = re.search(".*?", content_str)
    return author.group() if (author is not None) and (len(author.group()) < 15) else ""

def getRandomAccount():
    conn = None
    account = None
    try:
        conn = sqlite3.connect(db_file)
        result = conn.execute("SELECT a.username, a.cookies FROM account a WHERE a.locked = 'N';")
        acc_list = result.fetchall()
        if len(acc_list) == 0:
            raise RuntimeError("db 中沒有剩餘可用帳號了。")
        acc_index = random.randint(0, len(acc_list) - 1)
        account = acc_list[acc_index]
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()
        return account[0], account[1]

def login():
    username, cookies = getRandomAccount()
    print("使用 EYNY 帳號 :　", username)
    with open("LibCookies.txt", 'w') as cookieFile:
        cookieFile.write(cookies)
        cookieFile.close()
    session.cookies.load(ignore_discard=True, ignore_expires=True)
    print('cookies: ', session.cookies)
    return username

class PreCrawlerProcessor:
    @abstractmethod
    def getCrawablePage(self, url) -> BeautifulSoup:
        pass

    @abstractmethod
    def getNextPage(self, pagesBar) -> str:
        pass

    def start(self, frontPage):
        pagesBar = self.getCrawablePage(frontPage)  # TxDate > PostDate : break，pagesBar = None
        if pagesBar is not None:
            nextPageUrl = self.getNextPage(pagesBar)
            if nextPageUrl is not None:
                self.start(nextPageUrl)


class Entity:
    def __init__(self):
        self.__content = ""
        self.__site = site
        self.__parent = None
        self.__attr = {}

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, entity):
        self.__parent = entity
        self.url = entity.url
        self.title = entity.title

    @property
    def url(self) -> str:
        return self.__url

    @url.setter
    def url(self, url: str):
        self.__url = url

    @property
    def authorName(self) -> str:
        return self.__authorName

    @authorName.setter
    def authorName(self, authorName: str):
        self.__authorName = authorName

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str):
        self.__title = title

    @property
    def content(self) -> str:
        return self.__content

    @content.setter
    def content(self, content: str):
        self.__content = content

    @property
    def articleDate(self) -> str:
        return self.__articleDate

    @articleDate.setter
    def articleDate(self, articleDate: str):
        self.__articleDate = articleDate

    @property
    def postId(self) -> str:
        return self.__postId

    @postId.setter
    def postId(self, postId: str):
        self.__postId = postId

    @property
    def rid(self) -> str:
        return self.__rid

    @rid.setter
    def rid(self, rid: str):
        self.__rid = rid

    @property
    def pid(self) -> str:
        if self.__parent is not None:
            return self.__parent.postId
        else:
            return ""

    def getAttr(self, key):
        return self.__attr[key]

    def setAttr(self, key, value):
        self.__attr.update({key: value})

    def toMap(self):
        newRecord = {}
        newRecord['url'] = self.__url
        newRecord['authorName'] = self.__authorName
        newRecord['title'] = self.__title
        newRecord['content'] = self.__content
        newRecord['articleDate'] = self.__articleDate
        newRecord['site'] = self.__site
        newRecord['postId'] = self.__postId
        newRecord['rid'] = self.__rid
        newRecord['pid'] = self.pid
        return newRecord

if __name__ == '__main__':
    login()