from bs4 import BeautifulSoup

from Crawler.EYNY.tools_2 import session

def login():
    resp = session.get("http://www36.eyny.com/member.php?mod=logging&action=login")
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, features='lxml')
    formhash = soup.find("input", {"name": "formhash"}).get("value")
    session.cookies.clear()
    url = "http://www36.eyny.com/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=LrR74"
    postData = {
        'formhash': formhash,
        'loginfield': 'username',
        'referer': "http://www36.eyny.com/home.php?mod=space&do=home",
        'username': "NetproTrinity",
        'password': "trinity",
        'questionid': "0",
        'answer': "",
        'cookietime': "2592000",
    }
    session.post(url, data=postData)
    session.cookies.save()
    print('cookies: ', session.cookies)
    print('登入完成')

if __name__ == '__main__':
    login()