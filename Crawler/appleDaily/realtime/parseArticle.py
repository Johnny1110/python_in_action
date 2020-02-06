import requests

from tools import *

def startParse(url):
    try:
        resp = requests.get(url)
        resp.encoding = "utf-8"
        contentJson = getNeededJsonData(resp.text)
        article = Entity()
        article.title = contentJson["headlines"]["basic"]
        article.url = url
        article.content = excludeIframeCode(contentJson["content_elements"][0]['content'])
        article.authorName = extractAuthor(article.content)
        article.articleDate = extractPostDate(contentJson["last_updated_date"])
        article.postId = toMD5(url)
        article.rid = article.postId

        for data in article.toList():
            print(data)
    except Exception as ex:
        print("解析失敗 url : ", url)
        raise ex

if __name__ == '__main__':
    # startParse("https://tw.finance.appledaily.com/property/20200205/ZUAF32ZVIIXOYQR5GER56PRJRM/")  # 財經
    # startParse("https://tw.news.appledaily.com/politics/20200206/G2LYN2PMX3W6GP726336IGZQJY/")  # 政治
    # startParse("https://tw.entertainment.appledaily.com/entertainment/20200206/2LFRIWP37T7AIA5ARAVTPE7KOQ/")  # 娛樂
    # startParse("https://tw.news.appledaily.com/life/20200206/T7KDVPQ5WD6IA4I4S7B3JZVUIA/")  # 生活
    # startParse("https://tw.appledaily.com/property/20200130/SC5T7ZCRTBPXFPU3AX2BQSI7MM/")  # 專題
    # startParse("https://tw.news.appledaily.com/local/20200206/6VI7JXFNEC3AQ6HP6KYYOF7TOQ/")  # 社會
    # startParse("https://tw.news.appledaily.com/international/20200206/XHEAUAFLC2DZABPPPEHYYEO6Y4/")  # 國際
    # startParse("https://tw.lifestyle.appledaily.com/gadget/realtime/20200205/1699741/")  # 3C
    # startParse("https://tw.lifestyle.appledaily.com/supplement/20200206/WOBI45KPM46NYEGLGNE2BIMVQE/")  # 吃喝玩樂
    # startParse("https://tw.sports.appledaily.com/sports/20200206/MUKYC4FI6GERYPEKGADHPSJB2Q/")  # 體育
    # startParse("https://tw.news.appledaily.com/forum/20200204/I6UYUHYOZUCKT77YFAMSJFXIZE/")  # 論壇

    startParse("https://tw.sports.appledaily.com/realtime/20200203/1698681/")