import datetime
import sqlite3

from Crawler.facebookFansPage.tools_2 import session


def checkAccout(email, passwd):
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
            return False
    return True


def resetLockedAccount():
    db_file = "fake_account.db"
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        result = conn.execute("SELECT a.id, a.email, a.passwd, a.locked FROM account a WHERE a.locked = 1;")
        acc_list = result.fetchall()
        print("acc_list : ", acc_list)
        for acc in acc_list:
            locked = checkAccout(acc[1], acc[2])
            if locked:
                print("解除帳號鎖定 : ", acc[1])
                conn.execute("UPDATE account  SET locked = 0 WHERE email = '{}';".format(acc[1]))
                print('---'*30)
    except Exception as e:
        conn.rollback()
        print(e)
    finally:
        if conn:
            conn.commit()
            conn.close()

if __name__ == '__main__':
    resetLockedAccount()