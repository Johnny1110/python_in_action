#  自己寫的 Restful API 服務測試工具 (myPoster)

<br>

Restful API poster

<br>

---

<br>

## API 介紹

* import package : 
    
    ```python
  import Poster.myPoster.poster as poster
    ```
   
   <br>
   
* 測試 Login :

    預設提供 2 組 login 功能，分別是 loginWithEmail 與 loginWithUsername。
    
    ```python
  import Poster.myPoster.poster as poster

  poster.loginWithUsername("username", "password", "/url")

  poster.loginWithEmail("email", "password", "/url")
    ```
    
    這兩個方法，都會把 server 回傳的 accessToken 加入到 Headers 中，供接下來 runtime 期間其他 API 使用。
    
    如果要使用自訂登入，請改用 poster.post() 自行定義，別忘記把 token 加入 Header。
    
    
   <br>
   
* GET 與 POST

    ```python
  import Poster.myPoster.poster as poster

  poster.get("/url")
  
  poster.post("/url", data={})
    ```
    
  這兩個方法預設帶上 Header，並且回傳 JSON 資料。