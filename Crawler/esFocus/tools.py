import datetime
import hashlib
import re
from abc import abstractmethod
from bs4 import BeautifulSoup

site = '${SITENAME}'

def toMD5(data):
    m = hashlib.md5()
    m.update(data.encode("utf-8"))
    return m.hexdigest()

def generateTxDate(date_str):
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return date

# define
def extractPostDate(date_str):
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return date

# define
def generateEsUrl(target):
    return "https://www.eventsinfocus.org" + target

# define
def extractAuthorName(content_str):
    author = re.search("焦點事件記者.+?報導", content_str)
    return author.group() if (author is not None) and (len(author.group()) < 15) else ""


class PreCrawlerProcessor:
    @abstractmethod
    def fillDataToQueue(self, url) -> BeautifulSoup:
        pass

    @abstractmethod
    def getNextPage(self, pagesBar) -> str:
        pass

    def fillUrlQueue(self, frontPage):
        pagesBar = self.fillDataToQueue(frontPage)  # TxDate > PostDate : break，pagesBar = None
        nextPageUrl = self.getNextPage(pagesBar)
        if nextPageUrl is not None:
            self.fillUrlQueue(nextPageUrl)


class Entity:
    def __init__(self):
        self.__content = ""
        self.__site = site
        self.__parent = None

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, entity):
        self.__parent = entity

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
        return newRecord

if __name__ == '__main__':
    content = "焦點事件記者梁家瑋報導「蘇花改通車了」，行政院院長蘇貞昌於蘇花改谷風隧道口這麼說；今日（1/6）上午，民進黨政府於谷風隧道口風風光光的舉行蘇花改通車典禮，下午4時，蘇花改全線通車。"
    ans = extractAuthorName(content)
    print(ans)