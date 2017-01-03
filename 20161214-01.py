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
from dateutil.relativedelta import relativedelta
import os.path

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
	           "qdate": sear_date,
	           "selectType": "ALLBUT0999"
	           }
	
	r = requests.post(URL, data=payload, headers=headers)
	r.encoding = "utf-8"
	print(sear_date + str(r.status_code) + "\n")
	
	"""
	data_yn = "Y"
	if r.status_code==200:
		print(sear_date + "沒有資料...")
		data_yn = "N"

	if data_yn == "Y":
		file_name = "./tse_quo_data/" + sear_date.replace("/","") + ".csv"
		is_existed = os.path.exists(file_name)
		
		if is_existed == False:
			with open(file_name, 'wb') as f:
				for chunk in r.iter_content(chunk_size=1024): 
					if chunk: # filter out keep-alive new chunks
						f.write(chunk)
						f.close()	
	"""

# 起訖日期
start_date = "2016/02/01"
end_date = "2016/02/04"

date_fmt = "%Y/%m/%d"
a = datetime.datetime.strptime(start_date, date_fmt)
b = datetime.datetime.strptime(end_date, date_fmt)
delta = b - a
int_diff_date = delta.days
print("days=" + str(int_diff_date) + "\n")

i = 1
dt = ""
while i <= (int_diff_date+1):
	print(str(i) + "\n")
	if i==1:
		str_date = start_date
	else:
		str_date = parser.parse(str(dt)).strftime("%Y/%m/%d")

	#print(str_date + "\n")
	
	# 轉民國年日期
	arg_date = str(int(str_date[0:4]) - 1911) + str_date[4:]
	print(arg_date + "\n")
	DailyQuoCSV(arg_date)
	
	dt = datetime.datetime.strptime(str_date, date_fmt).date()
	dt = dt + relativedelta(days=1)
	i += 1








print("End of prog...")