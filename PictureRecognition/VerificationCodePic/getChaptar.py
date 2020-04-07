from time import sleep

import requests
import http.cookiejar as cookiejar

from bs4 import BeautifulSoup

headers = {
    'Host': 'irs.thsrc.com.tw',
    'Pragma': 'no-cache',
    'Referer': 'https://www.google.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'Sec-Fetch-Site': 'cross-site',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

session = requests.session()
session.cookies = cookiejar.LWPCookieJar(filename="LibCookies.txt")
session.headers = headers

def getChapter(count=1):
    for i in range(count):
        sleep(3)
        resp = session.get("https://irs.thsrc.com.tw/IMINT/")
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        imgSrc = soup.find("img").get("src")
        imgUrl = "https://irs.thsrc.com.tw" + imgSrc
        print("imgUrl: ", imgUrl)
        img = session.get(imgUrl)
        with open('imgs/{}.jpg'.format(i+1), 'wb') as file:
            file.write(img.content)
            file.flush()
            print("已存入圖片: {}.jpg".format(i+1))


if __name__ == '__main__':
    getChapter(count=20)
