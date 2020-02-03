import datetime
from queue import Queue

import selenium.webdriver as driver
from bs4 import BeautifulSoup

def extractCutoffDate(date_str):
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return date

driver_path = "D:\Mike_workshop\driver\geckodriver.exe"
headless = driver.FirefoxOptions()
# headless.add_argument("-headless")  # 無頭模式
headless.set_preference('permissions.default.image', 2)
outqueue = Queue()
txDate = extractCutoffDate("2020-01-10")
title_class = "107"  # 人物類


def startParse(fontpage):
    browser = driver.Firefox(executable_path=driver_path, options=headless)
    browser.get(fontpage)
    pageNum = -1  # 起始頁是 -1
    while True:
        try:
            print("解析 pageNum : ", pageNum)
            script = generateAjaxScript(pageNum)
            html = browser.execute_script(script)
            extractCrawablePage(html)
            pageNum = pageNum + 1
        except Exception as e:
            break
    browser.close()
    browser.quit()



def extractCrawablePage(html):
    soup = BeautifulSoup(html, features="lxml")
    ul = soup.find_all("li")
    print("len(ul)", len(ul))
    if len(ul) == 0:
        raise RuntimeError("CrawablePage 已爬完")
    for li in ul:
        date = extractArticleDate(li.find("time").text)
        if txDate <= date:
            outqueue.put(generateNextMgzNewsUrl(li.a.get("href")))
        else:
            raise RuntimeError("時間中止")


###### tools ######
def generateAjaxScript(pageNum):
    pageNum = str(pageNum)
    script = '''
    var tags = '';
    $.ajax({
        url:"/section/getNext/''' + title_class + '''/0/10/''' + pageNum + '''/20/?",
        cache:false,
        dataType:"html",
        async:false
    })
    .done(function(data) {
        tags = data
    })
    return tags
    '''
    return script

def extractCutoffDate(date_str):
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    return date

def extractArticleDate(date_str):
    date = datetime.datetime.strptime(date_str.strip(), "%Y年%m月%d日 %H:%M")
    return date

def generateNextMgzNewsUrl(half_url):
    return "https://tw.nextmgz.com/{}".format(half_url)

###### tools ######
if __name__ == '__main__':
    startParse("/#")
    while True:
        try:
            url = outqueue.get(block=False)
            print(url)
        except Exception:
            break