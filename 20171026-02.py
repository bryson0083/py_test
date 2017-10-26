# -*- coding: utf-8 -*-
"""
GMAIL郵件發送_V4

@author: Bryson Xue

@Note: 
	1. 測試透過使用API發送GMAIL郵件

@Ref:
	http://robertwdempsey.com/python3-email-with-attachments-using-gmail/
"""
import util.Mailer as GMail

m = GMail.Mailer()
m.send_from = 'xxx@gmail.com'			# 寄件者
m.gmail_password = 'password'			# 寄件者 GMAIL 密碼
m.recipients = ['yyy@gmail.com']		# 收件者
m.subject = 'Test Mail from program'    # 郵件主題
m.message = 'This is a test msg from program.'  # 郵件內文
#m.attachments = ['a.csv','b.csv','c.csv']  # 郵件附件檔案(如果有附件)
m.send_email()  # 寄出郵件