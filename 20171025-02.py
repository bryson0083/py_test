# -*- coding: utf-8 -*-
"""
GMAIL郵件發送_V2

@author: Bryson Xue

@Note: 
	1. 測試郵件中，增加附件檔案

@Ref:
	http://outofmemory.cn/code-snippet/1105/python-usage-smtplib-fa-email-carry-fujian-code
	http://techblogsearch.com/a/python-shi-yong-python-ji-song-han-fu-jian-li-csv-de-email-bing-ke-zheng-chang-xian-shi-zhong-wen
	https://stackoverflow.com/questions/26582811/gmail-python-multiple-attachments
"""
import smtplib
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

gmail_user = 'aaa@gmail.com'
gmail_password = 'password' # your gmail password

fileToSend = ["aaa.xlsx", "bbb.docx"]

msg = MIMEMultipart()
msg['Subject'] = 'Test mail with attachment.'
msg['From'] = gmail_user
msg['To'] = 'xxx@gmail.com'

msg.preamble = "I can send a mail with attachment."

ctype, encoding = mimetypes.guess_type(fileToSend)
if ctype is None or encoding is not None:
    ctype = "application/octet-stream"

maintype, subtype = ctype.split("/", 1)

if maintype == "text":
    fp = open(fileToSend)
    # Note: we should handle calculating the charset
    attachment = MIMEText(fp.read(), _subtype=subtype)
    fp.close()
elif maintype == "image":
    fp = open(fileToSend, "rb")
    attachment = MIMEImage(fp.read(), _subtype=subtype)
    fp.close()
elif maintype == "audio":
    fp = open(fileToSend, "rb")
    attachment = MIMEAudio(fp.read(), _subtype=subtype)
    fp.close()
else:
    fp = open(fileToSend, "rb")
    attachment = MIMEBase(maintype, subtype)
    attachment.set_payload(fp.read())
    fp.close()
    encoders.encode_base64(attachment)

attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
msg.attach(attachment)

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(gmail_user, gmail_password)
server.send_message(msg)
server.quit()

print('Email sent!')