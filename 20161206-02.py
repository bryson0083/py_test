# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 15:54:42 2016

@author: bryson0083
"""
import requests
from bs4 import BeautifulSoup
import time

name = "aaaa.txt"
file = open(name, 'a', encoding = 'UTF-8')

headers = {'User-Agent':'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
session = requests.session()

# 讀取查詢頁面
r = session.get("http://mops.twse.com.tw/mops/web/t163sb05", headers=headers)

time.sleep(5)

URL = 'http://mops.twse.com.tw/mops/web/ajax_t163sb05'

payload = {
"encodeURIComponent": "1",
"step": "1",
"firstin": "1",
"off": "1",
"TYPEK": "sii",
"year": '105',
"season": '03'
}
r = requests.post(URL, data=payload, headers=headers)
r.encoding = "utf-8"

#file.write(r.text)

#print(r.text)

sp = BeautifulSoup(r.text, 'html.parser')
print(sp)
file.close()