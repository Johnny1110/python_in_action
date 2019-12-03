#  爬網基本練習 (ePrice-Acer-Pad)

<br>

-----

<br>

## 介紹

這次爬網對象是 [ePrice 的 Acer Pad 討論板](https://www.eprice.com.tw/pad/talk/4474/0/1)。沒什麼特別的地方，主要練習一下使用 BeautifulSoup 套件，
總體難度並不高。

<br>

##  實作

1.  [DBEntity.py](./DBEntity.py)

    爬取的資料封裝類，比較特別的是 set_id() 是使用 MD5 加密 url。
    
    <br>

2.  [GetUrlPage.py](./GetUrlPage.py)

    取得符合日期範圍內的目標 URL 資料列。
    
    爬文條件在開頭位置設定即可 : 
    ```python
    # 截止日期 2016-01-01 00:00:00
    cutoffDate = datetime.datetime(2016, 1, 1)
    # 目標首頁
    frontpage = 'https://www.eprice.com.tw/pad/talk/4474/0/1'
    ```
    
    <br>

3.  [ParseInnerPage.py](./ParseInnerPage.py)

    解析 GetUrlPage.py 傳送過來的 URL 內文並把資料放入 dbData 陣列中，
    可以直接執行。
    
    ```python
    if __name__ == '__main__':
    gup.startCraw()
    accessbleUrl = gup.crawlableInnerUrls
    print("所有可爬URL : ")
    print(accessbleUrl)

    for url in accessbleUrl:
        startCrawInnerPage(url)
        print(dbData)
    ```

    

