import datetime
import re

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
        if re.match("昨天上午.*", date_str):
            return yesterday.replace(hour=int(time[0]), minute=int(time[1]), microsecond=0)
        else:
            return yesterday.replace(hour=int(time[0])+12, minute=int(time[1]), microsecond=0)

    if re.match("^1?[0-9]+月[1-3]?[0-9]+日[上下]午.*$", date_str):
        date = re.search("1?[0-9]+月[1-3]?[0-9]+日", date_str).group()
        year = datetime.datetime.today().year
        date = "{}年{}".format(year, date)
        date = datetime.datetime.strptime(date, "%Y年%m月%d日")
        time = str(re.sub("1?[0-9]+月[1-3]?[0-9]+日[上下]午", "", date_str)).split(":")
        if re.match(".*上午.*", date_str):
            return date.replace(hour=int(time[0]), minute=int(time[1]), microsecond=0)
        else:
            return date.replace(hour=int(time[0])+12, minute=int(time[1]), microsecond=0)

    if re.match("^[0-9]{4}年1?[0-9]+月[1-3]?[0-9]+日[上下]午.*$", date_str):
        temp = re.sub("[上下]午[1]?[0-9]+:[1-5]?[0-9]+", "", date_str)
        date = datetime.datetime.strptime(temp, "%Y年%m月%d日")
        time = str(re.sub("[0-9]{4}年1?[0-9]+月[1-3]?[0-9]+日[上下]午", "", date_str)).split(":")
        if re.match(".*上午.*", date_str):
            return date.replace(hour=int(time[0]), minute=int(time[1]), microsecond=0)
        else:
            return date.replace(hour=int(time[0])+12, minute=int(time[1]), microsecond=0)