"""
測試讀取公開觀測資訊站=>股利分派情形彙總表
歷史股利分派情形
"""
import requests
from bs4 import BeautifulSoup
import time

headers = {'User-Agent':'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
session = requests.session()

# 拋送查詢條件到頁面，並取回查詢結果內容
URL = 'http://mops.twse.com.tw/server-java/t05st09sub'
payload = {
           "step": "1",
           "TYPEK": "sii",
           "YEAR": "105",
           "first": ""
           }

r = requests.post(URL, data=payload, headers=headers)

r.encoding = "big5"
soup = BeautifulSoup(r.text, 'html.parser')
print(soup)