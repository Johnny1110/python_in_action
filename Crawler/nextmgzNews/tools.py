import datetime
import hashlib
import re

site = "test_site_id"

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
    pass