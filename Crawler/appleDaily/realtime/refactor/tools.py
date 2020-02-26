import datetime
import hashlib
import json
import re
import requests
from json import JSONDecodeError
from urllib.parse import urlparse

from abc import abstractmethod
from bs4 import BeautifulSoup
from dateutil.parser import parse


site = '${SITENAME}'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
    'Accept': 'text/html,application/xhtml+xml,application/json;q=0.9,image/webp,*/*;q=0.8',
}

session = requests.session()
proxies = {
    'http': 'socks5h://localhost:9150',
    'https': 'socks5h://localhost:9150',
}
session.proxies = proxies
session.headers = headers

def getNeededJsonData(text):
    try:
        soup = BeautifulSoup(text, features="lxml")
        tags = soup.find_all("script")
        contentPart = None
        for t in tags:
            if t.text.startswith("window.Fusion=window.Fusion||{}"):
                contentPart = t.text
                break
        parts = str(contentPart).split("Fusion.")
        globalContent = ""
        for p in parts:
            if p.startswith("globalContent="):
                globalContent = p[14:-1]
        return json.loads(globalContent)
    except JSONDecodeError:
        pass

def excludeIframeCode(content):
    soup = BeautifulSoup(content, features="lxml")
    return soup.text.strip()

def toMD5(data):
    m = hashlib.md5()
    m.update(data.encode("utf-8"))
    return m.hexdigest()

def generateDate(date_str, Chinese=False):
    if Chinese:
        return datetime.datetime.strptime(date_str, "%Y / %m / %d")
    else:
        return parse(date_str).replace(microsecond=0, tzinfo=None)

# define
def generateAppleUrl(base, target):
    host = urlparse(base)
    return "{}://{}{}".format(host.scheme, host.netloc, target)

# define
def extractAuthor(appleContent):  # （吳國仲╱台北報導）
    author = re.search("[（(].{1,10}[／╱].*報導[)）]", appleContent)
    return author.group() if (author is not None) and (len(author.group()) < 15) else ""

def urlToByteList(url):
    try:
        newRecord = []
        newRecord.append(url)
        return pys.recordToByte(newRecord)
    except Exception:
        return url

class PreCrawlerProcessor:
    @abstractmethod
    def fillDataToQueue(self, url) -> BeautifulSoup:
        pass

    @abstractmethod
    def getNextPage(self, pagesBar) -> str:
        pass

    def start(self, frontPage):
        pagesBar = self.fillDataToQueue(frontPage)  # TxDate > PostDate : break，pagesBar = None
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

    def toList(self):
        newRecord = []
        newRecord.append(self.__url)
        newRecord.append(self.__authorName.split("\u0000")[0].strip())
        newRecord.append(self.__title.split("\u0000")[0].strip())
        newRecord.append(self.__content.split("\u0000")[0].strip())
        newRecord.append(self.__articleDate)
        newRecord.append(self.__site)
        newRecord.append(self.__postId)
        newRecord.append(self.__rid)
        newRecord.append(self.pid)  # pid
        try:
            return pys.recordToByte(newRecord)  # Trinity 使用
        except Exception:
            return newRecord

if __name__ == '__main__':
    pass