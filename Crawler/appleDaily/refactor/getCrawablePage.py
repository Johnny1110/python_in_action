from bs4 import BeautifulSoup

from Crawler.appleDaily.refactor.tools_2 import generateDate, PreCrawlerProcessor, session, Entity, toMD5, \
    generateAppleDailyUrl

frontPage = "https://tw.appledaily.com/realtime/topic"
txDate = generateDate("2020-05-01")


def collectData(elem):
    article = Entity()
    article.url = generateAppleDailyUrl(elem['website_url'])
    article.title = elem['headlines']['basic']
    article.articleDate = generateDate(elem['created_date'])
    article.postId = toMD5(elem['_id'])
    article.rid = article.postId
    article.authorName = elem['owner']['id']
    for content in elem['content_elements']:
        try:
            tag = BeautifulSoup(content['content'], features='lxml')
            article.content += tag.getText()
        except Exception:
            continue
    return article

# 實作 fillDataToQueue() 與 getNextPage() 就可以了。
class Processor(PreCrawlerProcessor):
    def getCrawablePage(self, url) -> BeautifulSoup:
        resp = session.get(url)
        resp.encoding = 'utf-8'
        jsonData = resp.json()
        print(jsonData)
        content_elems = jsonData['content_elements']
        for elem in content_elems:
            publish_date = generateDate(elem['display_date'])
            print(publish_date)
            if publish_date >= txDate:
                try:
                    article = collectData(elem)
                except Exception:
                    continue
                print(article.toMap())

    def getNextPage(self, pagesBar) -> str:
        pass

def generateAPI(clazz):
    return "https://tw.appledaily.com/pf/api/v3/content/fetch/query-feed?query=%7B%22feedOffset%22%3A0%2C%22feedQuery%22%3A%22taxonomy.primary_section._id%3A%5C%22%2Frealtime%2F{}%5C%22%2BAND%2Btype%3Astory%2BAND%2Bpublish_date%3A%5Bnow-1000h%2Fh%2BTO%2Bnow%5D%22%2C%22feedSize%22%3A%22100%22%2C%22sort%22%3A%22display_date%3Adesc%22%7D".format(clazz)

if __name__ == '__main__':
    processor = Processor()
    clazz = frontPage.split("/")[-1]
    url = generateAPI(clazz)
    url = "https://tw.appledaily.com/pf/api/v3/content/fetch/content-by-tag?query={%22size%22%3A100%2C%22tag%22%3A%22mt_%E5%B0%88%E9%A1%8C%22%2C%22website%22%3A%22tw-appledaily%22}"
    processor.start(url)