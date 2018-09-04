# -*- coding: utf-8 -*-
"""
集保中心~集保戶股權分散表查詢，資料抓取 V2

@Note:
	查詢網頁
	https://www.tdcc.com.tw/smWeb/QryStock.jsp

	股權分散表資料來源
	https://smart.tdcc.com.tw/opendata/getOD.ashx?id=1-5

	下載檔案在chrome headless模式下，目前測試無法運作
	僅能在有開啟瀏覽器的狀態下，下載成功。

	方法1:get_comp_name
	測試起來效能比較差

	方法2:get_comp_name2
	效能只需要方法1的約一半時間

@Ref:
	https://www.dataquest.io/blog/python-pandas-databases/
	https://chrisalbon.com/python/data_wrangling/pandas_dataframe_importing_csv/
	https://stackoverflow.com/questions/15017072/pandas-read-csv-and-filter-columns-with-usecols
	http://hant.ask.helplib.com/python/post_4799128


"""
import os
import csv
import datetime
import time
import pandas as pd
import sqlite3
from dateutil import parser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import timeit

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

def get_comp_name(arg_sear_comp_id):
	global conn
	strsql = "select COMP_NAME from STOCK_COMP_LIST where SEAR_COMP_ID='" + arg_sear_comp_id + "'"
	df = pd.read_sql_query(strsql, conn)
	
	if not df.empty:
		comp_name = df['COMP_NAME'].iloc[0]
	else:
		comp_name = ' '

	#print(comp_name)
	return comp_name

def rd_comp_list():
	global conn
	strsql = "select SEAR_COMP_ID, COMP_NAME from STOCK_COMP_LIST  order by SEAR_COMP_ID limit 100"
	df = pd.read_sql_query(strsql, conn)
	#print(df)
	return df

def get_comp_name2(arg_sear_comp_id):
	if not co_df[co_df.SEAR_COMP_ID == arg_sear_comp_id].empty:
		comp_name = co_df[co_df.SEAR_COMP_ID == arg_sear_comp_id].iloc[0]['COMP_NAME']
	else:
		comp_name = ' '

	return comp_name

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
	global co_df

	cwd = os.getcwd()
	file_name = cwd + r"\tdcc_data\TDCC_OD_1-5.csv"
	#print(file_name)
	is_existed = os.path.exists(file_name)
	#print(is_existed)

	ls_head = ['QUO_DATE', 'SEAR_COMP_ID', 'SEQ', 'NUM_OF_PEOPLE', 'STOCK_SHARES','PER_CENT_RT']

	if is_existed:
		df = pd.read_csv(file_name, header=0, names=ls_head)
		data_dt = str(df.loc[0]['QUO_DATE'])

		#print(data_dt)
		#print(df.head(2))

		df = df.fillna(0)
		df['SEAR_COMP_ID'] = df['SEAR_COMP_ID'] + ".TW"

		co_df = rd_comp_list()	#讀取股票資料清單
		df['COMP_NAME'] = df.apply(lambda row: get_comp_name2(row['SEAR_COMP_ID']), axis=1)
		#df['COMP_NAME'] = df.apply(lambda row: get_comp_name(row['SEAR_COMP_ID']), axis=1)
		
		df['LV_DESC'] = df.apply(lambda row: lv_desc_dic(str(row['SEQ'])), axis=1)

		# 最後維護日期時間
		str_date = str(datetime.datetime.now())
		df['DATE_LAST_MAINT'] = parser.parse(str_date).strftime("%Y%m%d")
		df['TIME_LAST_MAINT'] = parser.parse(str_date).strftime("%H%M%S")
		df['PROG_LAST_MAINT'] = "GET_TDCC_STOCK_DISPERSION"

		colorder = ('QUO_DATE', 'SEAR_COMP_ID', 'COMP_NAME', 'SEQ', 'NUM_OF_PEOPLE', 'STOCK_SHARES',
		            'PER_CENT_RT', 'LV_DESC', 'DATE_LAST_MAINT', 'TIME_LAST_MAINT', 'PROG_LAST_MAINT')
		# 調整datagrame欄位順序	http://nullege.com/codes/search/pandas.DataFrame.reindex_axis
		df = df.reindex(colorder, axis=1)
		#print(df.head(20))

		df.to_sql("STOCK_DISPERSION", conn, if_exists="replace", index=False)

		#檔案rename保存
		new_file_name = cwd + "\\tdcc_data\\" + data_dt + ".csv"
		is_existed2 = os.path.exists(new_file_name)

		if is_existed2:
			os.remove(new_file_name)
		
		os.rename(file_name, new_file_name)
	else:
		print("無TDCC_OD_1-5.csv資料檔案存在.")


def MAIN_GET_TDCC():
	global conn

	timer_start = timeit.default_timer()
	#建立資料庫連線
	conn = sqlite3.connect('market_price.sqlite')

	download_tdcc_file()
	chk_tdcc_file()

	#關閉資料庫連線
	conn.close()
	timer_end = timeit.default_timer()
	print("\n\n\n耗時 %f sec\n" % (timer_end - timer_start))

if __name__ == "__main__":
	MAIN_GET_TDCC()