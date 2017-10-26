# -*- coding: utf-8 -*-
"""
GMAIL郵件發送_V3

@author: Bryson Xue

@Note: 
	1. 測試郵件中，增加附件檔案(多檔案)

@Ref:
	http://robertwdempsey.com/python3-email-with-attachments-using-gmail/
    https://gist.github.com/rdempsey/3dd81628a17398485010#449f17bc9b885a0f1d9a8f3b6f8e3561ebfcd1dc/Mailer.py
"""
import os
import sys
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '

def main():
    sender = 'xxx@gmail.com'
    gmail_password = 'password'
    recipients = ['aaa@gmail.com', 'bbb@gmail.com']
    
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'EMAIL SUBJECT'
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    # List of attachments
    attachments = ['a.xlsx','b.docx']

    # Add the attachments to the message
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise

    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Email sent!")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise

if __name__ == '__main__':
    main()