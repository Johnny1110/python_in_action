import datetime
import hashlib
import json
import re

from dateutil.parser import parse

from bs4 import BeautifulSoup

site = "test_site_id"

def getNeededJsonData(text):
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

def toMD5(data):
    m = hashlib.md5()
    m.update(data.encode("utf-8"))
    return m.hexdigest()

def excludeIframeCode(content):
    soup = BeautifulSoup(content, features="lxml")
    return soup.text.strip()

def extractPostDate(date_str):
    data = parse(date_str)
    data = data.replace(microsecond=0, tzinfo=None)
    return data.__str__()

def extractAuthor(appleContent):
    author = re.search("[（(].{1,10}／.*報導[)）]", appleContent)
    return author.group() if (author is not None) and (len(author.group()) < 15) else ""


class Entity:
    def __init__(self):
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
        newRecord.append(self.__authorName)
        newRecord.append(self.__title)
        newRecord.append(self.__content)
        newRecord.append(self.__articleDate)
        newRecord.append(self.__site)
        newRecord.append(self.__postId)
        newRecord.append(self.__rid)
        newRecord.append(self.pid)  # pid
        return newRecord

if __name__ == '__main__':
    file = open("./index.html", encoding="utf-8")
    data = file.read()
    excludeIframeCode(data)