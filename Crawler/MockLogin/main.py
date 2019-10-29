from Crawler.MockLogin.login import *
import Crawler.MockLogin.header_info as header_info
import Crawler.MockLogin.search as search

def run():
    alive = True
    my_session = login('10646029', 'NzVkMWZmYWJiMDBmNjY4OA==')
    print("公告 : 搜尋範圍僅限 2014 ~ 2019 年期間的商業週刊，祝您作弊愉快~XD")

    while alive:
        search.max_period = int(input("請輸入搜尋期刊最大 range (期數 ex: 1630)\n"))
        search.min_period = int(input("請輸入搜尋期刊最小 range (期數 ex: 1628)\n"))
        keyword = input("請輸入關鍵字，越詳細越好喔!\n")
        result = search.do_search(my_session, keyword)
        print("結果 :" + str(result))
        continue_using = input("輸入 q 離開，輸入其他任意鍵繼續。\n")
        if continue_using == 'q':
            alive = False

if __name__ == '__main__':
    run()