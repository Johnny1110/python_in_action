# TorProxyTools

<br>

利用 Tor 網路匿名爬網。

<br>

## 重要套件

* stem (發送信號給 Tor 的)

* PySock (Proxy 使用)


<br>
<br>
<br>

## Windows 系統

* Windows 系統在 Tor 切換路由時，要注意 Tor Browser 預設的 Proxy port 是 `9150`，switch IP 使用的 port 是 `9151`。

* 記得 Tor Browser 要一直打開。

<br>
<br>
<br>

## Unix like 系統 (Linux、MacOS)

* Linux 系統不必一定要安裝 Tor Browser，也可以直接裝 Tor Proxy Service。

    安裝步驟以 CentOS 舉例 :

    在終端機以 root 帳號操作

    ```bash
    yum install tor
    ```

    <br>
    <br>

* 安裝成功後如下方法使用 : 

    * 改變 tor 文件所有權，(這裡我的帳號是 `johnny` 群組是 `wheel`，根據你自己的 username 與 group 修改)

        ```bash
        sudo chown -R johnny:wheel /var/run/tor
        ```

        <br>

    * 再來我們要修改一下 tor 的 ControlPort 配置(可供改變 Proxy 的服務器 port)

        首先要複製一份 torrc 文件的樣本，並用 vim 打開編輯 :

        ```bash
        sudo mv /usr/local/etc/torrc.sample /usr/local/etc/torrc
        vim /usr/local/etc/torrc
        ```

        如果以上沒有找到相應 torrc 文件的話，請嘗試看看以下做法 :

        ```bash
        vim /etc/tor/torrc
        ```

        進入 torrc 後取消以下兩行註解 :

        ```bash
        ControlPort 9051
        CookieAuthentication 1
        ```

        <br>

    * 切換非 root 帳號 (Tor 在 root 帳號下啟動會失敗)，直接下指令啟動 tor :

        ```bash
        su - johnny
        tor
        ```

        啟動成功之後會看到 console 印出的 log，成功的話最後兩行會是 :

        ```bash
        Tor has successfully opened a circuit. Looks like client functionality is working.
        Bootstrapped 100%: Done
        ```

        <br>
        <br>

* 來驗證看看是否已經成功 :

    ```bash
    curl ipinfo.io            # 獲取本機的 IP 位址
    torsocks curl ipinfo.io   # Tor 幫我們找到的 IP，每隔幾分鐘換一次
    ```

    <br>
    <br>
    <br>

## Python 實作

* [點這裡看 code](./StealthAttack.py)
