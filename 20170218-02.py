# -*- coding: utf-8 -*-

import requests
import os.path
import csv
import pandas as pd
import sqlite3

def DownloadList():
	file_name = "./suspend_listing.csv"
		
	headers = {'User-Agent':'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
	session = requests.session()

	URL = "http://www.tse.com.tw/ch/listed/suspend_listing.php"
	payload = {
		"download": "csv"
	}
	r = requests.post(URL, data=payload, headers=headers)
	r.encoding = "utf-8"

	with open(file_name, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024): 
			if chunk: # filter out keep-alive new chunks
					f.write(chunk)

		#close file
		f.close()

def ReadCSV():
	file_name = "./suspend_listing.csv"
	is_existed = os.path.exists(file_name)

	if is_existed == True:
		print("is existed.")

		#讀取每日報價CSV檔
		with open(file_name, 'r') as f:
			reader = csv.reader(f)
			quo_list = list(reader)
		
		#關閉CSV檔案
		f.close

		#去掉抬頭的部分，自己定義資料抬頭
		quo_list = quo_list[2:]
		#print(quo_list)

		#quo_list list拋到pandas
		df = pd.DataFrame(quo_list, columns = ['終止上市日期', '公司名稱', '上市編號', 'col_a'])

		#去掉多出來的欄位col_a
		df2 = df.loc[:,['終止上市日期', '公司名稱', '上市編號']]
		#print(df2)

		ProcessDB(df2)


	else:
		print("檔案 suspend_listing.csv 不存在!")
		return


def ProcessDB(arg_df):
	#建立資料庫連線
	conn = sqlite3.connect("market_price.sqlite")

	for i in range(0,len(arg_df)):
		#print(str(df.index[i]))
		comp_name = str(arg_df.iloc[i][1])
		sear_comp_id = str(arg_df.iloc[i][2]) + ".TW"

		print(sear_comp_id + comp_name)

		sqlstr  = "select NOUSE_CODE from STOCK_COMP_LIST "
		sqlstr += "where SEAR_COMP_ID='" + sear_comp_id + "' and "
		sqlstr += "COMP_NAME = '" + comp_name + "'"

		cursor = conn.execute(sqlstr)
		result = cursor.fetchone()
		
		j = 0
		if result is not None:
			print("aaaa==>" + sear_comp_id + " code=" + result[0])
		else:
			j +=1
			#print("bbbb==>" + sear_comp_id)




	#關閉cursor
	cursor.close()

	#關閉資料庫連線
	conn.close()



############################################################################
# Main                                                                     #
############################################################################
print("Executing SUSP_STK_LIST...")


#DownloadList()
ReadCSV()

print("End of prog...")