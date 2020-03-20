# pbsocket（實現 protobuf 3 varint32RawHeader 協定的 python 資料傳輸 socket）

<br>

為了實現 Java 與 Python 之間做資料交換，所以這次使用 Google 推出的工具 __protobuf 3__。

Java 端有 __Netty__ 對 Protobuf 有良好的支援，所以就使用 Netty 來實作傳輸。具體細節就不放在本篇講解，Python 端目前有可以序列化 Protobuf 的工具，但是沒有支援封裝訊框（Frame）的功能。所以需要自己動手寫實現。 

本篇筆記第一次嘗試看看寫在 Medium 上分享，所以這邊附上目錄連結供參考，具體細節要去 Medium 上查看。

<br>

----

<br>
<br>

## 簡介