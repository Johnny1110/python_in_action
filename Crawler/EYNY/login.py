import sqlite3
from time import sleep

from bs4 import BeautifulSoup

from Crawler.EYNY.tools_2 import session

db_file = "eyny_fakeAcc.db"


def saveCookiesToDB(username):
    with open("LibCookies.txt") as cookiesFile:
        fileContentBuf = cookiesFile.read()
        cookiesFile.close()
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            conn.execute(
                "UPDATE account SET cookies = '{}' WHERE username = '{}'".format(
                    fileContentBuf, username))
        except Exception as e:
            conn.rollback()
            print(e)
        finally:
            if conn:
                conn.commit()
                conn.close()


def login(username, passwd):
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
        'username': username,
        'password': passwd,
        'questionid': "0",
        'answer': "",
        'cookietime': "2592000",
    }
    session.post(url, data=postData)
    session.cookies.save()
    print('cookies: ', session.cookies)
    saveCookiesToDB(username)
    print(username, '登入完成')

def refreshAccount():
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        result = conn.execute("SELECT a.username, a.passwd, a.locked FROM account a WHERE a.locked = 'N';")
        acc_list = result.fetchall()
        print("acc_list : ", acc_list)
        for acc in acc_list:
            sleep(1)
            login(acc[0], acc[1])
    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        if conn:
            conn.commit()
            conn.close()

if __name__ == '__main__':
    refreshAccount()