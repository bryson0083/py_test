# -*- coding: utf-8 -*-
"""
GMAIL郵件發送_V1

@author: Bryson Xue

@Note: 
	1. 前置作業
	   A. 參考參考資料網頁指示，降低個人GMAIL帳號安全性為低度
	   B. 啟用個人google帳號，兩部驗證
	   C. 針對要發送郵件的設備(EX:PC)，在google安全設定中新增應用程式專用密碼
	      (跟個人google帳號之密碼不同，只有for應用程式使用)

	2. 其他動作參考網頁範例程式

@Ref:
	https://amoshyc.github.io/blog/shi-yong-python-cong-gamil-zi-dong-ji-fa-email.html
	https://jamching.com/article/Python-to-Send-Email-1.html
	https://free.com.tw/google-2-step-verification/

"""
import smtplib
from email.mime.text import MIMEText

gmail_user = 'aaa@gmail.com'
gmail_password = 'password' # your gmail password

msg = MIMEText('content')
msg['Subject'] = 'Test'
msg['From'] = gmail_user
msg['To'] = 'xxx@yyy.com'

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(gmail_user, gmail_password)
server.send_message(msg)
server.quit()

print('Email sent!')