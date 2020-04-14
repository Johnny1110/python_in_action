import datetime
import sqlite3
from time import sleep

from bs4 import BeautifulSoup

from Crawler.facebookFansPage.tools_2 import session

db_file = "fake_account.db"

def lockedAccount(email, msg):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("UPDATE account SET locked = 'Y', locked_msg = '{}', cookies_file = '' WHERE email = '{}'".format(msg, email))
    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        if conn:
            conn.commit()
            conn.close()

def unlockedAccount(email, cookieContentFile):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("UPDATE account SET locked = 'N', locked_msg = '', cookies_file = '{}' WHERE email = '{}'".format(cookieContentFile, email))
    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        if conn:
            conn.commit()
            conn.close()


def testLogin(email, passwd):
    session.cookies.clear()
    print("嘗試登入 FB 帳號 :　", email)
    data = {
        'lsd': 'AVq1Hm_O',
        'jazoest': '2668',
        'li': 'AEp4XssNBBL4pR5EvIMg-jEb',
        'try_number': '0',
        'unrecognized_tries': '0',
        'm_ts': str(int(datetime.datetime.now().timestamp())),
        'email': email,
        'pass': passwd,
        'login': '登入',
    }
    url = "https://m.facebook.com/login/device-based/regular/login/?refsrc=https%3A%2F%2Fm.facebook.com%2Flogin%2F%3Fref%3Ddbl&lwv=100&ref=dbl"
    resp = session.post(url=url, data=data)
    session.cookies.save()
    resp.encoding = 'utf-8',
    print('cookies: ', session.cookies)
    for cookie in session.cookies:
        if cookie.name.__eq__("c_user"):
            with open("LibCookies.txt") as cookieFile:
                fileContentBuf = cookieFile.read()
                cookieFile.close()
                unlockedAccount(email, fileContentBuf)
            return
    soup = BeautifulSoup(resp.text, features='lxml')
    lockedAccount(email, soup.getText())



def checkAllAccount():
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        result = conn.execute("SELECT a.id, a.email, a.passwd, a.locked FROM account a WHERE a.chackable = 'Y';")
        acc_list = result.fetchall()
        print("acc_list : ", acc_list)
        for acc in acc_list:
            sleep(5)
            testLogin(acc[1], acc[2])
    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        if conn:
            conn.commit()
            conn.close()

if __name__ == '__main__':
    checkAllAccount()
    # testLogin("mani67kijh@gmail.com", "trinityyt")