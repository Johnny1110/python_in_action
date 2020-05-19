# 隨機生成假資料
# 格式: [姓名, 信箱, 身分證, 帳戶, 電話, 手機]
import re

import requests
from bs4 import BeautifulSoup

generate_amount = 1

def getNameAndId():
    postData = {
        "name_count": generate_amount,
        "break": 4,

    }
    resp = requests.post("http://www.richyli.com/name/index.asp", data=postData)
    resp.encoding = "big5"
    soup = BeautifulSoup(resp.text, features='lxml')
    td = soup.find("td", {"valign": "top"})
    target = td.getText()
    dataList = re.findall(".{3}?, [A-Z].{9}?", target)
    print(dataList)

if __name__ == '__main__':
    getNameAndId()