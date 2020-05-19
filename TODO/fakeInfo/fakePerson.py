import re
import random

import requests
from bs4 import BeautifulSoup

url = "https://fauxid.com/fake-name-generator/taiwan"

def generatePhoneBody(count=3):
    box = [random.randint(0, 9) for a in range(count)]
    result = ""
    for n in box:
        result += str(n)
    return result


# 09 開頭 + 10~89
def generatePhoneNumber():
    result = None
    head = "09"
    id = random.randint(10, 89)
    body1 = generatePhoneBody()
    body2 = generatePhoneBody()
    n_type = random.randint(1, 3)
    if n_type is 1:
        result = "{}{}{}{}".format(head, id, body1, body2)
    if n_type is 2:
        result = "{}{}-{}-{}".format(head, id, body1, body2)
    if n_type is 3:
        result = "{}{} {} {}".format(head, id, body1, body2)
    return result

# 8 碼或 9 碼，開頭 02 ~ 07
def generateHomePhoneNumber():
    length = random.randint(8, 9)
    head = random.randint(2, 7)
    head = "0{}".format(head)
    result = None
    body1 = None
    body2 = None
    sub = ""
    if length is 8:
        body1 = generatePhoneBody(3)
        body2 = generatePhoneBody(3)
    if length is 9:
        body1 = generatePhoneBody(3)
        body2 = generatePhoneBody(4)

    needSub = random.randint(0, 6)
    if needSub is 0:
        length = random.randint(1, 5)
        sub = generatePhoneBody(length)
        sub = "#{}".format(sub)

    n_type = random.randint(1, 7)
    if n_type is 1:
        result = "{}{}{}{}".format(head, body1, body2, sub)
    if n_type is 2:
        result = "{}{}{}".format(body1, body2, sub)
    if n_type is 3:
        result = "({}){}{}{}".format(head, body1, body2, sub)
    if n_type is 4:
        result = "({}) {}{}{}".format(head, body1, body2, sub)
    if n_type is 5:
        result = "{} {}{}{}".format(head, body1, body2, sub)
    if n_type is 6:
        result = "{} {} {} {}".format(head, body1, body2, sub)
    if n_type is 7:
        result = "{}-{}-{}{}".format(head, body1, body2, sub)
    return result


def getFakePerson(amount=1):
    for a in range(amount):
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        content = soup.find("div", class_="content")
        jsonUrl = content.find("a", text="Download as JSON").get("href")
        resp = requests.get(jsonUrl)
        resp.encoding = 'utf-8'
        personData = resp.json()
        personData = personData[0]
        name = getNameAndId()
        id = personData['miscellaneous']['personal_identity_number']
        address = personData['address_1']
        person_email = personData['email']
        company_email = personData['company_email']
        cc_number = personData['cc_number']
        phone = generatePhoneNumber()
        homePhone = generateHomePhoneNumber()
        record = "{},{},{},{},{},{},{},{}\n".format(name, id, person_email, company_email, cc_number, phone, homePhone, address)
        with open("data.csv", mode='a', encoding='utf-8') as file:
            file.write(record)
            file.flush()
            file.close()
        print(record)

def getNameAndId():
    postData = {
        "name_count": 1,
        "break": 4,
    }
    resp = requests.post("http://www.richyli.com/name/index.asp", data=postData)
    resp.encoding = "big5"
    soup = BeautifulSoup(resp.text, features='lxml')
    td = soup.find("td", {"valign": "top"})
    target = td.getText()
    dataList = re.findall(".{3}?, [A-Z].{9}?", target)
    dataStr = dataList[0]
    dataList = dataStr.split(", ")
    return dataList[0]

if __name__ == '__main__':
    getFakePerson(10)
