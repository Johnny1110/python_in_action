import requests
from time import sleep
from stem import Signal
from stem.control import Controller

# 在 windows 上用 Tor Browser
Win32Proxies = {
    'http': 'socks5h://localhost:9150',
    'https': 'socks5h://localhost:9150',
}

# 在 Unix like 上用 Tor Proxy
UnixProxies = {
    'http': 'socks5h://localhost:9050',
    'https': 'socks5h://localhost:9050',
}

def switchIP(waiting=8):
    with Controller.from_port(port=9151) as controller:
        while controller.is_newnym_available():
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
            break
        sleep(waiting)  # 不知道什麼時間能換完，等 `waiting` 秒。

def sendRequests(url):
    session = requests.session()
    session.proxies = Win32Proxies
    resp = session.get(url)
    resp.encoding = 'utf-8'
    print(resp.text)

if __name__ == '__main__':
    url = 'http://httpbin.org/ip'
    while True:
        sendRequests(url)
        switchIP(waiting=6)
