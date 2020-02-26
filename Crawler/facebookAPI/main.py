import json

import facebook

token = "EAAnHZAP9UjkQBADaPj9FT8xQUPZCg7NmUxRw54MszTsOMZBSl5h43nZC3aNTmGbPdVf9szyAAXTkJ00QkLPe3Bm7IfPRX62jnBBRhZBeSSaLsw8ibzvXpKqUTAPCip5QS8jcuZC7PYKHoWQU3fDBcyUUZBwBBd1rDjE7vz9WzgxXp7ifZAhRlGWnySBKi4WYwBhHFdaMX2NhvwZDZD"
app_id = "104745697704783"

graph = facebook.GraphAPI(access_token=token, version="3.1")

def testConnections():
    posts = graph.get_connections(id='me', connection_name='posts')
    print(posts)

def getFullMessage():
        posts = graph.get_object(id=app_id, fields='posts{message,created_time,from,comments{id,message,created_time}}')
        data = json.dumps(posts, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)
        print(data)

def getPost():
    posts = graph.get_object(id=app_id, fields='posts{message,created_time, from, comments{id, message, created_time}}')
    posts = posts['posts']['data']

    for post in posts:
        print("==="*40)
        print("貼文 ID : ", post['id'])
        print("貼文內容: ", post['message'])
        print("貼文時間: ", post['created_time'])
        print("貼文作者: ", post['from']['name'])

        print('---'*17 + " 留言區 " + '---'*17)

        for comment in post['comments']['data']:
            print("留言>>>>>>>>>>")
            print("留言 ID: ", comment['id'])
            print("留言時間: ", comment['created_time'])
            print("留言內容: ", comment['message'])

        print('==='*40)

if __name__ == '__main__':
    getPost()

