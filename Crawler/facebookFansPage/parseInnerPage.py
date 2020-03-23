import re

import requests
from bs4 import BeautifulSoup

from Crawler.facebookFansPage.fb_date_tools import speculateArticlePostDate
from Crawler.facebookFansPage.tools_2 import session, Entity, toMD5, generateMFBUrl


def setReplyAttr(article, replyBarUrl):
    resp = session.get(replyBarUrl)
    resp.encoding = 'utf-8'


def parseArticle(url):
    resp = session.get(url)
    resp.encoding = 'utf-8'
    session.cookies.save()
    soup = BeautifulSoup(resp.text, features='lxml')
    article = Entity()
    article.url = url
    article.postId = toMD5(url)
    article.rid = article.postId
    authorName = soup.findAll("table", {"role": "presentation"})[2].getText()
    article.articleDate = speculateArticlePostDate(soup.find("abbr").getText())
    if authorName:
        article.authorName = authorName
    else:
        article.authorName = "???"
    article.content = soup.find("title").getText()
    print(article.content)
    title = re.search("^.*[？?！!。~～.]+", article.content)
    if title:
        article.title = title.group()
    else:
        article.title = article.content[0:20]
    replyBar = soup.find("div", id="add_comment_switcher_placeholder").next_siblings.a
    replyBarUrl = generateMFBUrl(replyBar.get("href"))
    setReplyAttr(article, replyBarUrl)
    print(article.toMap())


def startParse(url):
    article = parseArticle(url)


if __name__ == '__main__':
    url = 'https://m.facebook.com/story.php?story_fbid=2718474544942401&id=352962731493606&refid=17&ref=dbl&_ft_=mf_story_key.2718474544942401%3Atop_level_post_id.2718474544942401%3Atl_objid.2718474544942401%3Acontent_owner_id_new.352962731493606%3Athrowback_story_fbid.2718474544942401%3Apage_id.352962731493606%3Aphoto_id.2718416124948243%3Astory_location.4%3Astory_attachment_style.photo%3Atds_flgs.3%3Apage_insights.%7B%22352962731493606%22%3A%7B%22page_id%22%3A352962731493606%2C%22actor_id%22%3A352962731493606%2C%22dm%22%3A%7B%22isShare%22%3A0%2C%22originalPostOwnerID%22%3A0%7D%2C%22psn%22%3A%22EntStatusCreationStory%22%2C%22post_context%22%3A%7B%22object_fbtype%22%3A266%2C%22publish_time%22%3A1584904920%2C%22story_name%22%3A%22EntStatusCreationStory%22%2C%22story_fbid%22%3A%5B2718474544942401%5D%7D%2C%22role%22%3A1%2C%22sl%22%3A4%2C%22targets%22%3A%5B%7B%22actor_id%22%3A352962731493606%2C%22page_id%22%3A352962731493606%2C%22post_id%22%3A2718474544942401%2C%22role%22%3A1%2C%22share_id%22%3A0%7D%5D%7D%7D%3Athid.352962731493606%3A306061129499414%3A2%3A0%3A1585724399%3A8894510529520450224&__tn__=%2AW-R#footer_action_list'
    startParse(url)