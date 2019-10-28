import requests
import http.cookiejar as cookielib
import Crawler.MockLogin.header_info as header_info


my_session = requests.session()
my_session.cookies = cookielib.LWPCookieJar(filename = "LibCookies.txt")

def login(account, password):
    reverse1_url = "https://eresources.ntub.edu.tw:3005/ndapp/member/MbFixLogin?pToUrl=/ndapp/KnoBase/magol/getContent?key=bsw"
    reverse2_url = "https://eresources.ntub.edu.tw:3005/ndapp/KnoBase/magol/getContent?key=bsw#fm"
    login_url = "https://eresources.ntub.edu.tw:3001/login"
    login_data = {
        'url': 'https://udndata.com/library/bsw',
        'uid': account,
        'pwd': password
    }

    my_session.post(login_url, data=login_data, headers=header_info.header)
    my_session.get(reverse1_url, headers=header_info.header)
    my_session.get(reverse2_url, headers=header_info.header)
    my_session.cookies.save()

    return my_session