from queue import Queue, Empty

from Crawler.appleDaily.realtime.getCrawlablePage import startCraw
from Crawler.appleDaily.realtime import getCrawlablePage
import selenium.webdriver as driver


def startParse(url):
    browser = driver.Chrome(executable_path="D:\Mike_workshop\driver\chromedriver.exe")
    browser.get(url)
    resp = browser.page_source
    print(resp)


if __name__ == "__main__":
    startCraw()
    inqueue = getCrawlablePage.outqueue
    while 1:
        try:
            url_list = inqueue.get(block=False)
            for url in url_list:
                startParse(url)
        except Empty:
            break
