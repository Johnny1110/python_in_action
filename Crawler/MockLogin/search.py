import Crawler.MockLogin.header_info as header_info

max_period = 1624
min_period = 1364

searching_url = 'https://eresources.ntub.edu.tw:3005/ndapp/KnoBase/magol/researchContent?key=bsw'
result_list = []

def do_search(my_session, key_word):

    result = []
    for i in range(1364, 1624):
        post_data = {
            'addkeyword': key_word,
            'search': 'VOLNO:'+ str(i),
            'range': 'VOLNO:'+ str(i),
            'title': '',
            'forlist': 'list'
        }
        resp = my_session.post(searching_url, data=post_data, headers=header_info.header)
        fill_list(resp.text)
    return result


def fill_list(text):
    # 過濾 html 資訊
    pass