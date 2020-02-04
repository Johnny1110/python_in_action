from queue import Queue

import selenium.webdriver as driver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Crawler.storm.GetCrawablePage import outqueue as url_queue, startCraw
from Crawler.storm.tools import Entity, extractPostDate, toMD5

site = "test_site_id"
outqueue = Queue()

driver_path = "D:\Mike_workshop\driver\geckodriver.exe"
headless = driver.FirefoxOptions()
# headless.add_argument("-headless")  # 無頭模式
headless.set_preference('permissions.default.image', 2)
browser = driver.Firefox(executable_path=driver_path, options=headless)





def startParse(url):
    browser.get(url)
    locator = (By.XPATH, '//iframe[contains(@title, "fb:comments Facebook Social Plugin")]')
    WebDriverWait(browser, 30).until(
        EC.presence_of_element_located(locator)
    )
    soup = BeautifulSoup(browser.page_source, features="lxml")
    article = parseArticle(url, soup.find("div", class_="page_wrapper"))


def parseArticle(url, contentSoup):
    article = Entity()
    article.url = url
    article.authorName = contentSoup.find("a", class_="link_author info_inner_content").text
    article.title = contentSoup.find("h1", id="article_title").text
    article.content = contentSoup.find("div", id="CMS_wrapper").text
    article.articleDate = extractPostDate(contentSoup.find("span", id="info_time").text)
    article.postId = toMD5(url)
    article.rid = article.postId
    outqueue.put(article.toList())


if __name__ == '__main__':
    startCraw()
    while True:
        try:
            urls = url_queue.get(block=False)
            for url in urls:
                startParse(url)
        except Exception as e:
            break

    while True:
        try:
            data = outqueue.get(block=False)
            print("---"*30)
            for item in data:
                print(item)
        except Exception:
            break

    browser.close()
    browser.quit()




