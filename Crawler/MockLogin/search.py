import Crawler.MockLogin.header_info as header_info
from bs4 import BeautifulSoup

max_period = 1667
min_period = 1500


searching_url = 'https://eresources.ntub.edu.tw:3005/ndapp/KnoBase/magol/researchContent?key=bsw'
result_list = []

def do_search(my_session, key_word):
    print("正在進行資料檢索，請稍後...")
    for i in range(min_period, max_period+1):
        post_data = {
            'addkeyword': key_word,
            'search': 'VOLNO:'+ str(i),
            'range': 'VOLNO:'+ str(i),
            'title': '',
            'forlist': 'list'
        }
        resp = my_session.post(searching_url, data=post_data, headers=header_info.header)
        fill_list(resp.text)
    return result_list


def fill_list(text):
    # 過濾 html 資訊
    html_str = text
    soup = BeautifulSoup(html_str,features="lxml")
    box_selector = "form dl dt a"
    period_selector = "form dl dd"
    box = [i.text for i in soup.select(box_selector)]
    period = [i.text for i in soup.select(period_selector)]
    if len(box) > 0:
        for i in range(len(box)):
            node = box[i] + " ||| " + period[i]
            result_list.append(node)

def flush_result_list():
    result_list.clear()
