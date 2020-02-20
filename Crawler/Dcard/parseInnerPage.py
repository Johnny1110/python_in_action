from queue import Queue

from bs4 import BeautifulSoup

from Crawler.Dcard.tools import generateDcardUrl, Entity, toMD5, generateDate, session

outqueue = Queue()


def parseArticle(url, postDate):
    resp = session.get(url)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, features='lxml')
    article = Entity()
    article.url = url
    article.postId = toMD5(url)
    article.rid = article.postId
    main_tag = soup.find("div", {"role": "main"})
    article.title = main_tag.find("h1").getText()
    article.authorName = main_tag.find("div", class_="sc-1j1k45b-6 fKmTeh").getText().strip()
    article.articleDate = postDate
    article.content = main_tag.find("div", class_="sc-1ro4bpk-0 jXIcFN").getText().strip()
    outqueue.put(article.toList())
    return article


def parseComment(article):
    commentsCnt = 0
    url = genetateDacrdCommentsUrl(article.getAttr("_id"), commentsCnt)  # 前 30 筆
    while True:
        resp = session.get(url)
        resp.encoding = 'utf-8'
        jsonData = resp.json()
        if len(jsonData) != 0:
            for data in jsonData:
                try:
                    comment = Entity()
                    comment.parent = article
                    comment.postId = toMD5(article.url + "_" + str(commentsCnt))
                    comment.rid = article.postId
                    comment.authorName = data['school']
                    comment.content = data['content']
                    comment.articleDate = generateDate(data['createdAt'])
                    outqueue.put(comment.toList())
                except Exception as e:
                    print("comment 格式錯誤 : ", data)
                commentsCnt += 1
            url = genetateDacrdCommentsUrl(article.getAttr("_id"), commentsCnt)
        else:
            break



def genetateDacrdCommentsUrl(_id, cmtNum):
    return "https://www.dcard.tw/service/api/v2/posts/{}/comments?after={}".format(_id, cmtNum)


def startParse(siteClass, _id, postDate):
    url = generateDcardUrl(siteClass, _id)
    article = parseArticle(url, postDate)
    article.setAttr("_id", _id)
    parseComment(article)


if __name__ == '__main__':
    # siteClass = "dcard"
    # _id = "233016856"
    # postDate = "2020-01-01 03:41:17"
    # startParse(siteClass, _id, postDate)
    #
    # while True:
    #     try:
    #         data = outqueue.get(block=False)
    #         for d in data:
    #             print("---"*40)
    #             print(d)
    #     except Exception as e:
    #         break

    article = parseArticle("https://www.dcard.tw/f/dcard/p/233016856", "2020-01-01 03:41:17")
    for d in article.toList():
        print("---"*30)
        print(d)
    content = article.content
    print(content)

