# LineToday 爬蟲

<br>

-----

<br>

## 簡介

這次來爬一下 Line Today 的文章以及留言。

值得注意的是，這次有把留言進行分類歸總，針對主文的留言以及針對留言的留言。

由於爬蟲基本上都是有時效性，過一段時間 class 換掉，API 換掉就要重新來過，所以這邊紀錄一下實作日期為 2019-12-19。

話不多說，來看一下吧 !

<br>

## 說明

1.  [getCrawlablePage.py](./getCrawlablePage.py)

    getCrawlablePage 負責將 Line Today 的某一個新聞分類的可爬取連結蒐集起來，準備交給下一段腳本處理。

    啟動 startCraw() 方法，將會開始解析 frontPage 變數提供的主題文章，這邊使用 NBA 的文章連結 :

    ```python
    frontPage = "https://today.line.me/TW/pc/main/100457"
    ```

    爬取的結果將以陣列的方式存入 queue 中，陣列的格式統一為

    *   第 0 個索引為 ArticleId

    *   地 1 個索引為 URL

<br>

2.  [parseInnerPage.py](./parseInnerPage.py)


    parseInnerPage 依賴於 getCrawlablePage 所提供的可爬取 URL queue。提出 queue 的每一筆紀錄再一一進行內文留言爬取。

    startParse() 可開啟爬取功能，依照順序會依次解析主文、留言、留言的留言。

    內置 Entity 類別提供物件的方式來存储資料，主文、留言、留言的留言之間的關係用物件嵌套的方式表達，Entity.parent 用來存放父級物件。

    *   解析主文

        ```python
        parseArticle(postId, url, soup)
        ```

    *   解析留言

        ```python
        parseComments(article) # 傳入父類別 Entity
        ```

    *   解析留言的留言

        ```python
        parseReply(comment) # 傳入父類別 Entity
        ```

    解析主文使用的是 bs4 套件解析 html，留言的部分因為有提供 API 所以直接解析 json 就可以了。

    解析的結果放置到 parseInnerPage 的 queue 物件之中。
