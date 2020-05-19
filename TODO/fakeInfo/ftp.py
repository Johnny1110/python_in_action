from ftplib import FTP  #載入ftp模組


def testUploadFile(ftp, filename):
    bufsize = 1024
    with open(filename, "rb") as file:
        ftp.storbinary("STOR {}".format(filename), file, bufsize)  # 上傳目標檔案


def testDownloadFile(ftp, filename):
    bufsize = 1024
    with open(filename, "wb") as file:
        ftp.retrbinary("RETR {}".format(filename), file.write, bufsize)


def playFtp():
    ftp = FTP()
    ftp.set_debuglevel(2)  # 開啟除錯級別2，顯示詳細資訊
    ftp.connect("192.168.17.113", 21)  # 連線的ftp sever和埠
    ftp.login("trainee15", "goat")  # 連線的使用者名稱，密碼

    print(ftp.getwelcome())  # 列印出歡迎資訊
    print(ftp.dir())

    testUploadFile(ftp, "kyphosis.csv")
    testDownloadFile(ftp, "kyphosis.csv")


if __name__ == '__main__':
    playFtp()