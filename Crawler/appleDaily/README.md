#  蘋果日報爬蟲 ( 使用 selenium )

<br>

---

<br>

## 簡介

不得不說，蘋果家似乎沒有後端工程師。基本的檔權限都沒做好，關掉 JS 之後文章就被看光光。
這邊還是留一點口德...

進入正題，這次來寫爬蟲爬蘋果日報 "可見部分" 的文章，以及底下的留言，由於蘋果家的留言部分使用
FaceBook plugin API，所以在最初本來打算使用 API 來取得 JSON，但是後來發現部分文章的留言透過 API 
無法正常取得，最後才決定要使用 selenium 這個下下策。

selenium 不是說不好，只是運用在大量爬網下效能極差。在自動化 Web 測試上倒是不錯的選擇。

這邊實作的是針對蘋果即時新聞的設計實作。

<br>

## 實作

1. [facebookAPI.py](./realtime/facebookAPI.py)

    這邊不算是實作的部分，只是不太捨得研究一段時間的 facebookAPI 就這麼涼著。
    放在這邊給需要的時候參考使用。
    
    <br>
    
2.  [getCrawlablePage.py](./realtime/getCrawlablePage.py)

    這個部分沒有甚麼特別的，單純把 realtime 部分的 url 抓下來，供給後面主要爬網程式使用。
    
    啟動方法 : 設定好 frontpage，啟動 startCraw() 方法
    
    ```python
    from Crawler.appleDaily.realtime.getCrawlablePage import startCraw, frontpage
    
    frontpage = "target url"
    
    startCraw()
    ```
    
    <br>
    
3.  [parseInnerPage.py](./realtime/parseInnerPage.py)

    啟動方法為 startParse(url)，將要爬的文章 url 放入參數中即可。
    可以搭配 getCrawlablePage.startCraw() 使用，把 startCraw() 傳回的 queue 
    依序取出值，再交給 startParse(url) 執行。
    
    ```python
    from Crawler.appleDaily.realtime.getCrawlablePage import *
    from Crawler.appleDaily.realtime.parseInnerPage import *
    
    startCraw()
    inqueue = outqueue
    while 1:
        try:
            url_list = inqueue.get(block=False)
            for url in url_list:
                 startParse(url)
        except Empty:
            break
       ```

    

