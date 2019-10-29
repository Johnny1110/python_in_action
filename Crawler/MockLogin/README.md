# MockLogin 爬蟲實現模擬登入(http.cookiejar)

<br>

----------------------------

<br>

## 簡介

學校期中考的個案討論課程，老師要求我們學生根據考卷上的關鍵字自己去商業週刊上找到堆應文章來答題。

兩三百期週刊，一刊 20 多篇，這馬上上我想到 python 爬蟲解決問題。商業週刊網址: https://eresources.ntub.edu.tw:3005/ndapp/KnoBase/magol/getContent?key=bsw#fm

這個小專案的難題在於怎麼做到維持登入的 cookies，參考 CSDN 的一篇文章來實現 : https://blog.csdn.net/zwq912318834/article/details/79571110

最後發現其實那個網站根本就已經有這個檢索功能了......嘎，白做了。

<br>

## 實作

*   [login.py](./login.py)

    這個網站需要登入才可以瀏覽內頁，也就是要保留 cookies。所以我想到使用 requests 的 session() 方法來模擬瀏覽器收送 cookies。但是直接使用 session 無法成功保留 cookies。例如 :

        my_session = requests.session()
        resp = my_session.post(login_url, data=post_data)
    
    第一次登入可以看到內頁，但是繼續瀏覽其他頁面就失敗。返回statusCode 200，顯示無權訪問。

    後來查閱資料後發現要使用 http.cookiejar.LWPCookieJar 來取代 request.session() 的 cookies 實作，例如:

        my_session.cookies = cookiejar.LWPCookieJar(filename = "LibCookies.txt")
        #-- ...post data... --#
        my_session.cookies.save()

    用此方法，在發送 request 並接收到 response 之後要用 my_session.cookies.save() 儲存 cookies，會在專案資料夾下以 LibCookies.txt 儲存。下次再次使用 session 時便會自動帶上 cookies。

<br>

*   [search.py](./search.py)

    由於該網站後端並不是使用 restful API 的方式串接，而是直接套模板，所以需要進行 html 解析。這邊使用 BeautifulSoup 套件解析資料。

        from bs4 import BeautifulSoup

        # 把 response 轉成 str 物件
        html_str = my_session.get(url).text

        # 把 html_str 傳入到 BeautifulSoup 中
        soup = BeautifulSoup(html_str,features="lxml")

        # 搜尋選擇條件( form 之 dl 之 dt 之 a )
        box_selector = "form dl dt a"

        # box 就是<a>標籤中的內容集合。 
        box = [i.text for i in soup.select(box_selector)]

<br>     

* [main.py](./main.py)

    主程式進入點。

<br>

* [header_info.py](./header_info.py)

    生成 header 資訊，每一次 post 與 get 都要附帶 header，所以包成一個檔案給所有程式共享。


<br>

## 心得

雖然之後發現園網站本來就有全域檢索功能了，但是自己實做了模擬登入，與 html 分析之後，還是學到不錯的經驗。可喜可賀~XD。