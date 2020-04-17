import requests
from bs4 import BeautifulSoup

from Crawler.EYNY.tools_2 import headers

cookies = {
    "612e55XbD_e8d7_agree": "1",
    "612e55XbD_e8d7_videoadult": "1",
}

def getUrlMap():
    with open("EYNY_URL.txt", "r", encoding='utf-8') as url_file:
        lines = url_file.readlines()
        urlsMap = {}
        for line in lines:
            data = line.split(";")
            urlsMap.update({data[0]: data[1].strip()})
        return urlsMap


def urlWriteToFile(name, url):
    with open("new_url.txt", encoding='utf-8', mode='a') as file:
        file.write(name + ";" + url + "\n")
        file.flush()
        file.close()

if __name__ == '__main__':
    urlMap = getUrlMap()
    for name, url in urlMap.items():
        resp = requests.get(url, cookies=cookies, headers=headers)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, features='lxml')
        moderate = soup.find("form", id="moderate")
        if moderate is None:
            print("無法訪問: ", name, url)
            print(soup.getText())
        else:
            print("正常: ", name)
            urlWriteToFile(name, url)