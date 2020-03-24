import re
from time import sleep

from bs4 import BeautifulSoup

from Crawler.facebookFansPage.fb_tools import speculateArticlePostDate, login
from Crawler.facebookFansPage.tools_2 import session, Entity, toMD5, generateMFBUrl


def setReplyAttr(article, replyBarUrl):
    resp = session.get(replyBarUrl)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, features='lxml')
    for ul in soup.findAll("ul"):
        ul.decompose()
    react_alts = ['讚', '怒', '哇', '哈', '嗚', '大心']
    for index, alt in enumerate(react_alts):
        react = soup.find("img", {"alt": alt})
        if react is not None:
            reactCnt = int(react.next_sibling.getText())
            if index+1 == 1:
                article.int1 = reactCnt
            if index+1 == 2:
                article.int2 = reactCnt
            if index+1 == 3:
                article.int3 = reactCnt
            if index+1 == 4:
                article.int4 = reactCnt
            if index+1 == 5:
                article.int5 = reactCnt
            if index+1 == 6:
                article.int6 = reactCnt



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
    title = re.search("^.*[？?！!。~～.]+", article.content)
    if title:
        article.title = title.group()
    else:
        article.title = article.content[0:20]
    replyBar = soup.find("div", {"id": "add_comment_switcher_placeholder"}).next_sibling.a
    replyBarUrl = generateMFBUrl(replyBar.get("href"))
    setReplyAttr(article, replyBarUrl)
    print(article.toMap())
    article.setAttr("soup", soup)
    return article


def parseReplys(reply_area, comment, user_id):
    abbrs = reply_area.findAll("abbr")
    for abbr in abbrs:
        tag_withID = abbr.parent.parent.parent
        reply = Entity()
        reply.parent = comment
        reply.postId = toMD5('{}_{}'.format(comment.postId, tag_withID.get("id")))
        reply.rid = comment.parent.postId
        h3_authorName = tag_withID.find("h3")
        reply.authorName = h3_authorName.getText()
        reply.content = h3_authorName.next_sibling.getText()
        if reply.content.__eq__(""):
            reply.content = "圖片"
        reply.articleDate = speculateArticlePostDate(tag_withID.find("abbr").getText())
        react_like_tag = tag_withID.find("abbr").parent.find("span", {'id': re.compile('^like_.*')})
        ufi_url = react_like_tag.find("a", {"href": re.compile('^/ufi/reaction/profile/browser/.*')})
        if ufi_url:
            setReplyAttr(reply, generateMFBUrl(ufi_url.get("href")))
        print('寫入回應 : ', reply.toMap())

    more = reply_area.find("div", {"id": re.compile("^comment_replies_more_1.*")})
    if more:
        more_url = generateMFBUrl(more.get("href"))
        resp = session.get(more_url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        main_comment = soup.find("div", id=user_id)
        reply_area = main_comment.next_sibling
        parseReplys(reply_area, comment, user_id)



def processCommentAndReply(user_id, replyUrl, comment):
    resp = session.get(replyUrl)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, features='lxml')
    main_comment = soup.find("div", id=user_id)
    h3_authorName = main_comment.find("h3")
    comment.postId = toMD5('{}_{}'.format(comment.parent.url, user_id))
    comment.rid = comment.parent.postId
    comment.authorName = h3_authorName.getText()
    comment.content = h3_authorName.next_sibling.getText()
    if comment.content.__eq__(""):
        comment.content = "圖片"

    print("留言時間: ", main_comment.find("abbr").getText())
    comment.articleDate = speculateArticlePostDate(main_comment.find("abbr").getText())
    react_like_tag = main_comment.find("abbr").parent.find("span", {'id': re.compile('^like_.*')})
    ufi_url = react_like_tag.find("a", {"href": re.compile('^/ufi/reaction/profile/browser/.*')})
    if ufi_url:
        setReplyAttr(comment, generateMFBUrl(ufi_url.get("href")))
    print('寫入留言 : ', comment.toMap())

    reply_area = main_comment.next_sibling
    parseReplys(reply_area, comment, user_id)





def parseComments(article):
    sleep(3)
    soup = article.getAttr("soup")
    comment_tag = soup.find("div", {"id": "add_comment_link_placeholder"}).previous_sibling
    abbrs = comment_tag.findAll("abbr")
    for abbr in abbrs:
        user_comment = abbr.parent.parent.parent
        user_id = user_comment.get("id")
        replyUrl = generateMFBUrl(user_comment.find("a", text="回覆").get("href"))
        comment = Entity()
        comment.parent = article
        processCommentAndReply(user_id, replyUrl, comment)

    more = comment_tag.find("div", {"id": re.compile("^see_next_.*")})
    if more:
        more_url = generateMFBUrl(more.a.get("href"))
        resp = session.get(more_url)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, features='lxml')
        article.setAttr("soup", soup)
        parseComments(article)


def startParse(url):
    login()
    try:
        article = parseArticle(url)
        parseComments(article)
    except Exception:
        print('文章解析失敗 url: ', url)


if __name__ == '__main__':
    url = 'https://m.facebook.com/story.php?story_fbid=2718474544942401&id=352962731493606&refid=17&ref=dbl&_ft_=mf_story_key.2718474544942401%3Atop_level_post_id.2718474544942401%3Atl_objid.2718474544942401%3Acontent_owner_id_new.352962731493606%3Athrowback_story_fbid.2718474544942401%3Apage_id.352962731493606%3Aphoto_id.2718416124948243%3Astory_location.4%3Astory_attachment_style.photo%3Atds_flgs.3%3Apage_insights.%7B%22352962731493606%22%3A%7B%22page_id%22%3A352962731493606%2C%22actor_id%22%3A352962731493606%2C%22dm%22%3A%7B%22isShare%22%3A0%2C%22originalPostOwnerID%22%3A0%7D%2C%22psn%22%3A%22EntStatusCreationStory%22%2C%22post_context%22%3A%7B%22object_fbtype%22%3A266%2C%22publish_time%22%3A1584904920%2C%22story_name%22%3A%22EntStatusCreationStory%22%2C%22story_fbid%22%3A%5B2718474544942401%5D%7D%2C%22role%22%3A1%2C%22sl%22%3A4%2C%22targets%22%3A%5B%7B%22actor_id%22%3A352962731493606%2C%22page_id%22%3A352962731493606%2C%22post_id%22%3A2718474544942401%2C%22role%22%3A1%2C%22share_id%22%3A0%7D%5D%7D%7D%3Athid.352962731493606%3A306061129499414%3A2%3A0%3A1585724399%3A8894510529520450224&__tn__=%2AW-R#footer_action_list'
    startParse(url)