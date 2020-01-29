import json

import requests

headers = {
    "Content-Type": "application/json"
}

cookies = {

}

def addHeader(key, value):
    headers[key] = value

def addCookie(key, value):
    cookies[key] = value

def loginWithUsername(username, password, url):
    data = {
        "username": username,
        "password": password
    }
    postData = json.dumps(data)
    resp = requests.post(url=url, data=postData, header=headers, cookies=cookies)
    resp.encoding = 'utf-8'
    respData = json.load(resp.text)
    setToken(respData['tokenType'], respData['accessToken'])
    return respData


def setToken(tokenType, token):
    addHeader("Authorization", "{} {}".format(tokenType, token))


def loginWithEmail(email, password, url):
    data = {
        "email": email,
        "password": password
    }
    postData = json.dumps(data)
    resp = requests.post(url=url, data=postData, headers=headers, cookies=cookies)
    resp.encoding = 'utf-8'
    respData = json.loads(resp.text)
    setToken(respData['tokenType'], respData['accessToken'])
    return respData



def get(url):
    resp = requests.get(url=url, headers=headers)
    resp.encoding = 'utf-8'
    respData = json.loads(resp.text)
    return respData

def post(url, data):
    postData = json.dumps(data)
    resp = requests.post(url=url, headers=headers, data=postData)
    resp.encoding = 'utf-8'
    respData = json.loads(resp.text)
    return respData