import smtplib
from email.mime.text import MIMEText

def playEmail():
    with open("email.html", 'r', encoding="utf-8") as file:
        html = file.read()
    mime=MIMEText(html, "html", "utf-8")
    mime["Subject"] = "test測試"  # 撰寫郵件標題
    mime["From"] = "trainee15"  # 撰寫你的暱稱或是信箱
    mime["To"] = "norman760926@gmail.com"  # 撰寫你要寄的人
    mime["Cc"] = "10646029@ntub.edu.tw"  # 副本收件人
    msg = mime.as_string()  # 將msg將text轉成str
    smtp = smtplib.SMTP("192.168.17.113", 25)  # google 的 ping
    smtp.connect("192.168.17.113", 25)
    smtp.ehlo()  # 申請身分
    from_addr = "trainee15"
    to_addr = ["norman760926@gmail.com"]
    status = smtp.sendmail(from_addr, to_addr, msg)
    if status == {}:
        print("郵件傳送成功!")
    else:
        print("郵件傳送失敗!")
    smtp.quit()

if __name__ == '__main__':
    playEmail()