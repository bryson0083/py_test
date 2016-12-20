# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 10:13:09 2016

@author: bryson0083
"""

import requests
from bs4 import BeautifulSoup
import time
from random import randint

headers = {'User-Agent':'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
session = requests.session()

# 拋送查詢條件到頁面，並取回查詢結果內容
URL = 'http://www.tse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php'
payload = {
           "download": "csv",
           "qdate": "105/12/12",
           "selectType": "ALLBUT0999"
           }

r = requests.post(URL, data=payload, headers=headers)
#print("Going to post!!")
#time.sleep(10)
#print("Proc Awake!!")

r.encoding = "utf-8"
#r.encoding = "big5"

with open('ccc.csv', 'wb') as f:
	for chunk in r.iter_content(chunk_size=1024): 
		if chunk: # filter out keep-alive new chunks
			f.write(chunk)

f.close()

print("End of prog...")