# coding=UTF-8

import hashlib

class Entity:

    def set_id(self, id):
        m = hashlib.md5()
        m.update(id.encode('utf-8'))
        self.id = m.hexdigest()

    def get_id(self):
        return self.id

    def set_site(self, site):
        self.site = site

    def get_site(self):
        return self.site

    def set_rid(self, rid):
        self.rid = rid

    def get_rid(self):
        return self.rid

    def set_pid(self, pid):
        self.pid = pid

    def get_pid(self):
        return self.pid

    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def set_title(self, title):
        self.title = title

    def get_title(self):
        return self.title

    def set_content(self, content):
        self.content = content

    def get_content(self):
        return self.content

    def set_author(self, author):
        self.author = author

    def get_author(self):
        return self.author

    def set_postDate(self, postDate):
        self.postDate = postDate

    def get_postDate(self):
        return self.postDate

    def set_updateDate(self, updateDate):
        self.updateDate = updateDate

    def get_updateDate(self):
        return self.updateDate

    def set_replycnt(self, replycnt):
        self.replycnt = replycnt

    def get_replycnt(self):
        return self.replycnt

    def set_updatecnt(self, updatecnt):
        self.updatecnt = updatecnt

    def get_updatecnt(self):
        return self.updatecnt

    def set_lang(self, lang):
        self.lang = lang

    def get_lang(self):
        return self.lang

    def toList(self):
        newRecord = []
        newRecord.append(self.id)
        newRecord.append(self.url)
        newRecord.append(self.content)
        newRecord.append(self.postDate)