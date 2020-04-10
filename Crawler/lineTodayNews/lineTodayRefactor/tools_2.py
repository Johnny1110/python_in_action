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

session = requests.session()
# proxies = {
#     'http': 'socks5h://localhost:9150',
#     'https': 'socks5h://localhost:9150',
# }
# session.proxies = proxies
# session.headers = headers

def toMD5(data):
    m = hashlib.md5()
    m.update(data.encode("utf-8"))
    return m.hexdigest()

def generateDate(date_str):
    return parse(date_str).replace(microsecond=0, tzinfo=None)

# define
def generateBTUrl(target):
    return "https://#" + target

# define
def extractAuthorName(content_str):
    author = re.search(".*?", content_str)
    return author.group() if (author is not None) and (len(author.group()) < 15) else ""


#   取得 Line Today 留言的 API
def generateArticleCommonsAPI(postId, commentsAmount="0", categoryId=None):
    if commentsAmount.__eq__("0"):
        commentsAmount = "50"
    api = "https://api.today.line.me/webapi/article/dinfo?articleIds=" + postId +"&categoryId=" + categoryId + "&country=TW&sort=POPULAR&commentSize=" + commentsAmount
    return api

#   取得 Line Today 留言回應的 API
def generateCommonsReplysAPI(postId, replycnt, commentSn):
    api = "https://api.today.line.me/webapi/comment/list?articleId=" + postId + "&limit=" + str(replycnt) + "&country=TW&parentCommentSn=" + str(commentSn)
    return api

def msTransToDate(param):
    ms = param
    return datetime.datetime.fromtimestamp(ms/1000.0).replace(microsecond=0).__str__()


def extarctDate(date_str):
    return datetime.datetime.strptime(date_str[5:], "%Y年%m月%d日%H:%M").replace(microsecond=0).__str__()


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
    def likescnt(self) -> str:
        return self.__likescnt

    @likescnt.setter
    def likescnt(self, likescnt: str):
        self.__likescnt = likescnt

    @property
    def dislikescnt(self) -> str:
        return self.__dislikescnt

    @dislikescnt.setter
    def dislikescnt(self, dislikescnt: str):
        self.__dislikescnt = dislikescnt

    @property
    def replycnt(self) -> str:
        return self.__replycnt

    @replycnt.setter
    def replycnt(self, replycnt: str):
        self.__replycnt = replycnt

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
        newRecord['postId'] = toMD5(self.__postId)
        newRecord['rid'] = toMD5(self.__rid)
        newRecord['pid'] = toMD5(self.pid) if not self.pid.__eq__("") else self.pid
        newRecord['likescnt'] = self.__likescnt
        newRecord['dislikescnt'] = self.__dislikescnt
        newRecord['replycnt'] = self.__replycnt
        return newRecord

if __name__ == '__main__':
    ans = toMD5("")
    print(ans)