from queue import Queue

import requests
from bs4 import BeautifulSoup

from Crawler.upMedia.tools import Entity, toMD5, generateDate, randomSleep

outqueue = Queue()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
    'Host': 'www.upmedia.mg',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://www.upmedia.mg/'
}

def startParse(url):
    try:
        randomSleep()
        resp = requests.get(url, headers=headers)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        main_tag = soup.find("div", id="news-info")
        article = Entity()
        article.url = url
        article.postId = toMD5(url)
        article.rid = article.postId
        article.title = main_tag.find("h2", id="ArticleTitle").getText()
        author_tag = main_tag.find("div", class_="author")
        article.authorName = author_tag.a.getText()
        author_tag.a.decompose()
        article.articleDate = generateDate(author_tag.getText().strip(), Chinese=True)
        content = main_tag.find("div", class_="editor")
        for p in content.findAll("p"):
            article.content += p.getText().strip() + '\r\n'
        outqueue.put(article.toList())
        return article
    except Exception as e:
        print("內文解析失敗 url: ", url)


if __name__ == '__main__':
    url = "https://www.upmedia.mg/news_info.php?SerialNo=81598"
    article = startParse(url)
    for data in article.toList():
        print(data)
        print("---"*30)