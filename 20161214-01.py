# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 10:13:09 2016

@author: bryson0083
"""

import requests
from bs4 import BeautifulSoup
import time
from random import randint
from dateutil import parser
import datetime

def DailyQuoCSV(sear_date):
	headers = {'User-Agent':'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
	session = requests.session()
	
	# 讀取查詢頁面
	r = session.get("http://www.tse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php", headers=headers)
	
	print("Going to wait!!")
	time.sleep(5)
	
	# 拋送查詢條件到頁面，並取回查詢結果內容
	URL = 'http://www.tse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php'
	payload = {
	           "download": "csv",
	           "qdate": "105/12/12",
	           "selectType": "ALLBUT0999"
	           }
	
	r = requests.post(URL, data=payload, headers=headers)
	r.encoding = "utf-8"
	
	with open('ccc.csv', 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
	
	f.close()

str_date = "20160101"
start_date = parser.parse(str_date).strftime("%Y%m%d")
date_1 = datetime.datetime.strptime(start_date, "%Y%m%d")

end_date = date_1 + datetime.timedelta(days=10)
str_end_date = parser.parse(end_date).strftime("%Y%m%d")

print(str(date_1) + "~" + str(str_end_date))


print("End of prog...")