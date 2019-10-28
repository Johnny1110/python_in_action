from Crawler.MockLogin.login import *
import Crawler.MockLogin.header_info as header_info
import Crawler.MockLogin.search as search

keyword = ''
alive = True
my_session = login('10646029', 'NzVkMWZmYWJiMDBmNjY4OA==')
print("公告 : 搜尋範圍僅限 2014 ~ 2019 年期間的商業週刊，祝您作弊愉快~XD")

while alive:
    keyword = input("請輸入關鍵字，越詳細越好喔!")
    result = search.do_search(my_session, keyword)
    print("結果 :" + str(result.text))
    continue_using = input("輸入 q 離開，輸入其他任意鍵繼續。")
    if continue_using == 'q':
        alive = False
