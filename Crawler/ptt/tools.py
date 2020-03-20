import datetime
import hashlib
import re
import requests

from abc import abstractmethod
from bs4 import BeautifulSoup
from dateutil.parser import parse


site = '${SITENAME}'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
    'Accept': 'text/html,application/xhtml+xml,application/json;q=0.9,image/webp,*/*;q=0.8',
}

cookies = {
    "over18": "1"
}

session = requests.session()
proxies = {
    'http': 'socks5h://localhost:9150',
    'https': 'socks5h://localhost:9150',
}
session.proxies = proxies
session.headers = headers

def toMD5(data):
    m = hashlib.md5()
    m.update(data.encode("utf-8"))
    return m.hexdigest()

def generateIpDate(parent_date, date_str):
    date_str = re.sub('((1?[0-9]{1,2}|2[0-4][0-9]|25[0-5])\\.){3}(1?[0-9]{1,2}|2[0-4][0-9]|25[0-5]){1} ', "", date_str)
    year = parent_date.year
    temp = "{} {}".format(year, date_str).strip()
    result = datetime.datetime.strptime(temp, "%Y %m/%d %H:%M")
    return result

def generateDate(date_str):
    try:
        return parse(date_str).replace(microsecond=0, tzinfo=None)
    except:
        return datetime.datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y")

# define
def generatePTTUrl(target):
    return "https://www.ptt.cc" + target

# define
def extractAuthorName(content_str):
    author = re.search(".*?", content_str)
    return author.group() if (author is not None) and (len(author.group()) < 15) else ""


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
        self.__int1 = 0
        self.__int2 = 0
        self.__int3 = 0
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

    def toArticleMap(self):
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
        newRecord['replycnt'] = sum([self.__int1, self.__int2, self.__int3])
        return newRecord

    def toCommentMap(self):
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
        newRecord['int1'] = 0
        newRecord['int2'] = 0
        newRecord['int3'] = 0
        newRecord['replycnt'] = 0
        return newRecord

if __name__ == '__main__':
    ans = generateIpDate(datetime.datetime.now(), "03/16 14:05")
    print(ans)