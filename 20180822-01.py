# -*- coding: utf-8 -*-
"""



@Note:
	查詢網頁
	https://www.tdcc.com.tw/smWeb/QryStock.jsp

	股權分散表資料來源
	https://smart.tdcc.com.tw/opendata/getOD.ashx?id=1-5

	下載檔案在chrome headless模式下，目前測試無法運作
	僅能在有開啟瀏覽器的狀態下，下載成功。

@Ref:

"""
import os
import csv
import datetime
import time
import pandas as pd
from dateutil import parser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def lv_desc_dic(param):
	code_dic = {
		'1': '1-999',
		'2': '1000-5000',
		'3': '5001-10000',
		'4': '10001-15000',
		'5': '15001-20000',
		'6': '20001-30000',
		'7': '30001-40000',
		'8': '40001-50000',
		'9': '50001-100000',
		'10': '100001-200000',
		'11': '200001-400000',
		'12': '400001-600000',
		'13': '600001-800000',
		'14': '800001-1000000',
		'15': '1000001以上',
		'16': '差異數調整（說明4）',
		'17': '合計'
	}
	lv_desc = code_dic.get(param, '')
	return lv_desc

def download_tdcc_file():
	cwd = os.getcwd()
	file_path = cwd + r"\tdcc_data"
	#print(file_path)

	chrome_options = Options()
	chrome_options.add_experimental_option("prefs", {
		"download.default_directory": file_path,
		"download.prompt_for_download": False,
		"download.directory_upgrade": True,
		"safebrowsing.enabled": True
	})

	#chrome_options.add_argument('--headless')
	#chrome_options.add_argument('--disable-gpu')
	driver = webdriver.Chrome(chrome_options=chrome_options)

	driver.get("https://smart.tdcc.com.tw/opendata/getOD.ashx?id=1-5")
	time.sleep(10)
	driver.quit()

def chk_tdcc_file():
	cwd = os.getcwd()
	file_name = cwd + r"\tdcc_data\TDCC_OD_1-5.csv"
	#print(file_name)
	is_existed = os.path.exists(file_name)
	#print(is_existed)

	ls_head = ['QUO_DATE', 'SEAR_COMP_ID', 'COMP_NAME', 'SEQ', 'NUM_OF_PEOPLE', 'STOCK_SHARES','PER_CENT_RT']

	if is_existed:
		df = pd.read_csv(file_name, columns=ls_head)
		data_dt = str(df.loc[0]['資料日期'])

		#print(data_dt)
		#print(df.head(1))

		df = df.fillna(0)
		df['證券代號'] = df['SEAR_COMP_ID'] + ".TW"
		df['LV_DESC'] = df.apply(lambda row: lv_desc_dic(str(row['持股分級'])), axis=1)

		# 最後維護日期時間
		str_date = str(datetime.datetime.now())
		date_last_maint = parser.parse(str_date).strftime("%Y%m%d")
		time_last_maint = parser.parse(str_date).strftime("%H%M%S")
		prog_last_maint = "GET_TDCC_STOCK_DISPERSION"
		df['DATE_LAST_MAINT'] = date_last_maint
		df['TIME_LAST_MAINT'] = time_last_maint
		df['PROG_LAST_MAINT'] = prog_last_maint

		colorder = ('QUO_DATE', 'SEAR_COMP_ID', 'COMP_NAME', 'SEQ', 'NUM_OF_PEOPLE', 'STOCK_SHARES',
		            'PER_CENT_RT', 'LV_DESC', 'DATE_LAST_MAINT', 'TIME_LAST_MAINT', 'PROG_LAST_MAINT')
		# 調整datagrame欄位順序	http://nullege.com/codes/search/pandas.DataFrame.reindex_axis
		df = df.reindex(colorder, axis=1)

		print(df.head(20))

		#for index, row in df.iterrows():
		#	print(row['資料日期'], row['證券代號'])
		#	lv_desc_dic(row['持股分級'])




		




#def MAIN_GET_TDCC():
#	is_existed = chk_tdcc_file()



if __name__ == "__main__":
	#download_tdcc_file()
	chk_tdcc_file()
