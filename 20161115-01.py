# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 13:26:03 2016

@author: yu63158
"""





"""
#! coding=UTF-8
# 本程式目的為抓取證交所建材營造類指數從2010年到今天的每日指數
__author__ = 'john.chen'

import requests,time, os
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta

'''
檔案儲存路徑與檔名，最後的格式應該是逗點分隔的csv
2001/01/04,100
2001/01/05,102
2001/01/06,101
...

'''
# 表頭：date是民國日期，格式：99/01/04
payload = {
           "download":"",
           "qdate": "105/11/14",
           "selectType":"MS"
           }

# TWSE 臺灣證券交易所 > 每日收盤行情 > 大盤統計資訊
url = "http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php"
res = requests.post(url, data = payload)
# print res.encoding # 找出網頁編碼
soup = BeautifulSoup(res.text.encode('utf-8'))
print(soup)
"""







import requests
from bs4 import BeautifulSoup
import time

headers = {'User-Agent':'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
session = requests.session()

# 讀取查詢頁面
r = session.get("http://mops.twse.com.tw/mops/web/t164sb04", headers=headers)

print("Going to wait!!")
time.sleep(5)


# 拋送查詢條件到頁面，並取回查詢結果內容
URL = 'http://mops.twse.com.tw/mops/web/ajax_t163sb04'
payload = {
           "encodeURIComponent": "1",
           "step": "1",
           "firstin": "1",
           "off": "1",
           "TYPEK": "sii",
           "year": "105",
           "season": "01"
           }

r = requests.post(URL, data=payload, headers=headers)
print("Going to post!!")
time.sleep(5)
print("Proc Awake!!")

r.encoding = "utf-8"
soup = BeautifulSoup(r.text, 'html.parser')
print(soup)


