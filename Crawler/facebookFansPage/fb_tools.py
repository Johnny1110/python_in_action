import datetime
import re

from Crawler.facebookFansPage.tools_2 import session


def login():
    data = {
        'lsd': 'AVq1Hm_O',
        'jazoest': '2668',
        'li': 'AEp4XssNBBL4pR5EvIMg-jEb',
        'try_number': '0',
        'unrecognized_tries': '0',
        'm_ts': str(int(datetime.datetime.now().timestamp())),
        'email': 'gmo.netpro@gmail.com',
        'pass': '89631965',
        'login': '登入',
    }
    url = "https://m.facebook.com/login/device-based/regular/login/?refsrc=https%3A%2F%2Fm.facebook.com%2Flogin%2F%3Fref%3Ddbl&lwv=100&ref=dbl"
    resp = session.post(url=url, data=data)
    session.cookies.save()
    resp.encoding = 'utf-8'
    print('cookies: ', session.cookies)


def speculateArticlePostDate(date_str):
    if re.match("^[1-5]?[0-9]+ 分鐘$", date_str):
        minutes = int(date_str.replace("分鐘", "").strip())
        return (datetime.datetime.today() - datetime.timedelta(minutes=minutes)).replace(microsecond=0)

    if re.match("^[1-2]?[0-9]+ 小時$", date_str):
        hours = int(date_str.replace("小時", "").strip())
        return (datetime.datetime.today() - datetime.timedelta(hours=hours)).replace(microsecond=0)

    if re.match("^昨天[上下]午.*$", date_str):
        time = str(re.sub("昨天[上下]午", "", date_str)).split(":")
        yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
        if re.match("昨天[(上午)(下午12:)].*", date_str):
            return yesterday.replace(hour=int(time[0]), minute=int(time[1]), microsecond=0)
        else:
            return yesterday.replace(hour=int(time[0])+12, minute=int(time[1]), microsecond=0)

    if re.match("^星期[一二三四五六日][上下]午.*$", date_str):
        target_weekday = re.search("星期[一二三四五六日]", date_str).group()
        weekday_map = {
            '星期六': 1,
            '星期日': 2,
            '星期一': 3,
            '星期二': 4,
            '星期三': 5,
            '星期四': 6,
            '星期五': 7,
        }
        time = str(re.sub(".*[上下]午", "", date_str)).split(":")
        today = datetime.datetime.today()
        if re.match(".*[(上午)(下午12:)].*", date_str):
            today = today.replace(hour=int(time[0]), minute=int(time[1]), microsecond=0)
        else:
            today = today.replace(hour=int(time[0])+12, minute=int(time[1]), microsecond=0)
        today_weekday = today.weekday() + 1 + 2  # 加 1 因亞洲地區比歐美快一天，加 2 因裡拜六為第一天
        distance = today_weekday - weekday_map[target_weekday]
        target_day = today - datetime.timedelta(days=distance)
        return target_day


    if re.match("^1?[0-9]+月[1-3]?[0-9]+日[上下]午.*$", date_str):
        date = re.search("1?[0-9]+月[1-3]?[0-9]+日", date_str).group()
        year = datetime.datetime.today().year
        date = "{}年{}".format(year, date)
        date = datetime.datetime.strptime(date, "%Y年%m月%d日")
        time = str(re.sub("1?[0-9]+月[1-3]?[0-9]+日[上下]午", "", date_str)).split(":")
        if re.match(".*[(上午)(下午12:)].*", date_str):
            return date.replace(hour=int(time[0]), minute=int(time[1]), microsecond=0)
        else:
            return date.replace(hour=int(time[0])+12, minute=int(time[1]), microsecond=0)

    if re.match("^[0-9]{4}年1?[0-9]+月[1-3]?[0-9]+日[上下]午.*$", date_str):
        temp = re.sub("[上下]午[1]?[0-9]+:[1-5]?[0-9]+", "", date_str)
        date = datetime.datetime.strptime(temp, "%Y年%m月%d日")
        time = str(re.sub("[0-9]{4}年1?[0-9]+月[1-3]?[0-9]+日[上下]午", "", date_str)).split(":")
        if re.match(".*[(上午)(下午12:)].*", date_str):
            return date.replace(hour=int(time[0]), minute=int(time[1]), microsecond=0)
        else:
            return date.replace(hour=int(time[0])+12, minute=int(time[1]), microsecond=0)

if __name__ == '__main__':
    ans = speculateArticlePostDate("星期六下午12:12")
    print(ans)