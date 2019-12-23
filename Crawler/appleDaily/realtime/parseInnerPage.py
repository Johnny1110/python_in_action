from queue import Queue, Empty

from Crawler.appleDaily.realtime.getCrawlablePage import startCraw
from Crawler.appleDaily.realtime import getCrawlablePage


def startParse(url):
    print(url)


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
