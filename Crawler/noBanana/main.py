import os
import shutil
from pathlib import Path

import requests
from bs4 import BeautifulSoup

floder_path="D:/buffer/comics/sisters/"
# floder_path="D:/buffer/comics/secrets/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

img_headers = {
    "Accept": "image/webp,*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "www.no-banana.com",
    "Pragma": "no-cache",
    "Referer": "http://www.no-banana.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0",
}

def generateBananaUrl(data_str):
    return "http://www.no-banana.com{}".format(data_str)

def startParseMenu(main_url):
    print("取得目標目錄 url: ", main_url)
    url_list = []
    resp = requests.get(main_url, headers=headers)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, features='lxml')
    list_tag = soup.find("ul", class_="detail-list-select")
    for a in list_tag.findAll("a"):
        url_list.append(generateBananaUrl(a.get("href")))
    return url_list

def startParseImageUrls(url):
    img_urls_list = []
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, features='lxml')
    content = soup.find("div", class_="comicpage")
    for imgs_tag in content.findAll("img"):
        target = generateBananaUrl(imgs_tag.get("data-src"))
        print("已取得圖片 url: ", target)
        img_urls_list.append(target)
    return img_urls_list


def downloadImgs(url, chapter, page):
    img_name = "{}.jpg".format(page)
    path = "{}/{}/".format(floder_path, chapter)
    Path(path).mkdir(parents=True, exist_ok=True)
    if not os.path.isfile(path + img_name):
        resp = requests.get(url, stream=True, headers=img_headers)
        with open(path + img_name, 'wb') as out_file:
            shutil.copyfileobj(resp.raw, out_file)
        del resp
        print("圖片下載成功，章節: {} ，頁數: {}".format(chapter, page))
    else:
        print("圖片已下載，skiping...章節: {} ，頁數: {}".format(chapter, page))


if __name__ == '__main__':
    url = "http://www.no-banana.com/book/336" #  sisters
    # url = "http://www.no-banana.com/book/618"  # secrets
    menu_url = startParseMenu(url)
    for menu in menu_url:
        img_urls = startParseImageUrls(menu)
        for index, img_url in enumerate(img_urls):
            chapter = img_url.split('/')[-2]
            page = index+1
            downloadImgs(img_url, chapter, page)
