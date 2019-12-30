import json
import requests

token = "your token"
pageUrl = "https://tw.news.appledaily.com/politics/realtime/20191227/1682856/" ## 可行

# 1 查詢文章ID
api = "https://graph.facebook.com/?ids={}&fields=og_object".format(pageUrl)
articleId = json.loads(requests.get(api).text)[pageUrl]['og_object']['id']
print(articleId)

# 2 查詢文章第一層回應
api = "https://graph.facebook.com/{}/comments?summary=1&filter=toplevel&access_token={}".format(articleId, token)
commentsJson = json.loads(requests.get(api).text)
print(commentsJson)

# 3 查詢留言的回復
commentId = commentsJson['data'][4]['id']
api = "https://graph.facebook.com/{}/comments?summary=1&filter=toplevel&access_token={}".format(commentId, token)
replysJson = json.loads(requests.get(api).text)
print(replysJson)