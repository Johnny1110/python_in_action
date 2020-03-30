import hashlib
import random
from http import cookiejar
from time import sleep

import requests

from abc import abstractmethod
from bs4 import BeautifulSoup
from dateutil.parser import parse


site = '${SITENAME}'

slow_down = False

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-TW,zh;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type':	'application/x-www-form-urlencoded',
    'DNT': '1',
    'Host': 'm.facebook.com',
    'Pragma': 'no-cache',
    'Referer': 'https://m.facebook.com/login/?next&ref=dbl&fl&refid=8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0'
}

session = requests.session()
session.headers = headers
session.cookies = cookiejar.LWPCookieJar(filename="LibCookies.txt")

# proxies = {
#     'http': 'socks5h://localhost:9150',
#     'https': 'socks5h://localhost:9150',
# }
# session.proxies = proxies

def randomSleep():
    if slow_down:
        ran_num = random.randint(1, 5)
        sleep(ran_num)

def toMD5(data):
    m = hashlib.md5()
    m.update(data.encode("utf-8"))
    return m.hexdigest()

def generateDate(date_str):
    return parse(date_str).replace(microsecond=0, tzinfo=None)


# define
def generateMFBUrl(target):
    return "https://m.facebook.com" + target

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
        self.__int1 = 0
        self.__int2 = 0
        self.__int3 = 0
        self.__int4 = 0
        self.__int5 = 0
        self.__int6 = 0


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

    @property
    def int1(self) -> int:
        return self.__int1

    @int1.setter
    def int1(self, int1: int):
        self.__int1 = int1

    @property
    def int2(self) -> int:
        return self.__int2

    @int2.setter
    def int2(self, int2: int):
        self.__int2 = int2

    @property
    def int3(self) -> int:
        return self.__int3

    @int3.setter
    def int3(self, int3: int):
        self.__int3 = int3

    @property
    def int4(self) -> int:
        return self.__int4

    @int4.setter
    def int4(self, int4: int):
        self.__int4 = int4

    @property
    def int5(self) -> int:
        return self.__int5

    @int5.setter
    def int5(self, int5: int):
        self.__int5 = int5

    @property
    def int6(self) -> int:
        return self.__int6

    @int6.setter
    def int6(self, int6: int):
        self.__int6 = int6

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
        newRecord['int1'] = self.__int1
        newRecord['int2'] = self.__int2
        newRecord['int3'] = self.__int3
        newRecord['int4'] = self.__int4
        newRecord['int5'] = self.__int5
        newRecord['int6'] = self.__int6
        newRecord['replycnt'] = sum([self.__int1, self.__int2, self.__int3, self.__int4, self.__int5, self.__int6])
        return newRecord

if __name__ == '__main__':
    pass