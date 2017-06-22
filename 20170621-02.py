# -*- coding: utf-8 -*-
"""
集保中心~集保戶股權分散表查詢，資料抓取

@author: Bryson Xue
@target_rul: 
	查詢網頁 => http://www.tdcc.com.tw/smWeb/QryStock.jsp
@Note: 
	集保中心~集保戶股權分散表查詢
	每日資料結轉寫入資料庫
	抓取目標為上市、上櫃股票

@Ref:
	http://www.largitdata.com/course/53/
"""
import sqlite3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from random import randint
from dateutil import parser
import datetime
from dateutil.relativedelta import relativedelta
import os.path
import sys

def DO_WAIT():
	#隨機等待一段時間
	#sleep_sec = randint(30,120)
	sleep_sec = randint(5,10)
	print("間隔等待 " + str(sleep_sec) + " secs.\n")
	time.sleep(sleep_sec)

def GET_DATE_LIST():
	global err_flag
	rt_flag = True

	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
	session = requests.session()

	# 拋送查詢條件到頁面，並取回查詢結果內容
	try:
		URL = 'http://www.tdcc.com.tw/smWeb/QryStock.jsp'
		r = requests.get(URL, headers=headers)
		r.raise_for_status()	#https://stackoverflow.com/questions/15258728/requests-how-to-tell-if-youre-getting-a-404
		r.encoding = 'big5'
	except Exception as e:
		err_flag = True
		print("Err from GET_DATE_LIST(): \n$$$ 集保中心網站讀取錯誤，請確認網頁是否正常. $$$\n" + str(e) + "\n")
		file.write("Err from GET_DATE_LIST(): \n$$$ 集保中心網站讀取錯誤，請確認網頁是否正常. $$$\n" + str(e) + "\n")
		return []

	sp = BeautifulSoup(r.text, 'html.parser')
	opt = sp.select('option')

	dt_list = [item.text.strip() for item in opt]
	dt_list = sorted(dt_list, reverse=False)
	#print(dt_list)
	
	return dt_list


def GET_DATA(arg_stock, arg_date):
	global err_flag
	rt_flag = True

	sear_comp_id = arg_stock[0]
	comp_id = arg_stock[0].replace(".TW","")
	comp_name = arg_stock[1]
	print("\n抓取" + sear_comp_id + " " + comp_name + " 日期" + arg_date + "集保戶股權分散資料.")

	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
	session = requests.session()

	# 拋送查詢條件到頁面，並取回查詢結果內容
	try:
		URL = 'http://www.tdcc.com.tw/smWeb/QryStock.jsp?SCA_DATE=' + arg_date + '&SqlMethod=StockNo&StockNo=' + comp_id + '&StockName=&sub=%ACd%B8%DF'
		r = requests.get(URL, headers=headers)
		r.raise_for_status()
		r.encoding = 'big5'
	except Exception as e:
		err_flag = True
		rt_flag = False
		print("Err from GET_DATA(): \n")
		print("$$$ 抓取" + sear_comp_id + " " + comp_name + " 日期 " + arg_date + " 集保戶股權分散資料失敗.$$$\n" + str(e) + "\n")
		file.write("Err from GET_DATA(): \n")
		file.write("$$$ 抓取" + sear_comp_id + " " + comp_name + " 日期 " + arg_date + " 集保戶股權分散資料失敗.$$$\n" + str(e) + "\n")
		return []

	sp = BeautifulSoup(r.text, 'html.parser')
	tb = sp.select('.mt')[1]
	#print(tb)

	all_data = []
	for tr in tb.select('tr'):
		rdata = [td.text.replace("\u3000","").replace(",","").strip() for td in tr.select('td')]
		all_data.append(rdata)
	
	ls_head = ['SEQ', 'LV_DESC', 'NUM_OF_PEOPLE', 'STOCK_SHARES', 'PER_CENT_RT']
	#df = pd.DataFrame(all_data[1:len(all_data)-1], columns=ls_head)	#最後一筆合計資料不要
	df = pd.DataFrame(all_data[1:], columns=ls_head)	#最後一筆合計資料不要

	#插入其他必要欄位
	df['QUO_DATE'] = arg_date
	df['SEAR_COMP_ID'] = sear_comp_id
	df['COMP_NAME'] = comp_name

	# 最後維護日期時間
	str_date = str(datetime.datetime.now())
	date_last_maint = parser.parse(str_date).strftime("%Y%m%d")
	time_last_maint = parser.parse(str_date).strftime("%H%M%S")
	prog_last_maint = "GET_TDCC_STOCK_DISPERSION"
	df['DATE_LAST_MAINT'] = date_last_maint
	df['TIME_LAST_MAINT'] = time_last_maint
	df['PROG_LAST_MAINT'] = prog_last_maint

	colorder = ('QUO_DATE', 'SEAR_COMP_ID', 'COMP_NAME', 'SEQ', 'LV_DESC', 'NUM_OF_PEOPLE', 'STOCK_SHARES', 'PER_CENT_RT', 'DATE_LAST_MAINT', 'TIME_LAST_MAINT', 'PROG_LAST_MAINT')
	df = df.reindex_axis(colorder, axis=1)	#調整datagrame欄位順序	http://nullege.com/codes/search/pandas.DataFrame.reindex_axis

	df.to_sql(name='STOCK_DISPERSION', con=conn, index=False, if_exists='replace')

	#print(df)
	return rt_flag



############################################################################
# Main                                                                     #
############################################################################
print("Executing GET_TDCC_STOCK_DISPERSION ...\n\n")
global err_flag
err_flag = False

#LOG檔
str_date = str(datetime.datetime.now())
str_date = parser.parse(str_date).strftime("%Y%m%d")
name = "GET_TDCC_STOCK_DISPERSION_LOG_" + str_date + ".txt"
file = open(name, "a", encoding="UTF-8")

print_dt = str(str_date) + (' ' * 22)
print("##############################################")
print("##           集保戶股權分散表查詢           ##")
print("##             (上市、上櫃股票)             ##")
print("##                                          ##")
print("##  datetime: " + print_dt +               "##")
print("##############################################")

#依據所選模式，決定抓取方式
#mode A:抓取最近一周資料
#mode B:抓取日期清單所有資料
try:
	run_mode = sys.argv[1]
	run_mode = run_mode.upper()
except Exception as e:
	run_mode = "A"

print("you choose mode " + run_mode)
if run_mode == "A":
	print("A: 抓取最近一周資料...\n")
	file.write("A: 抓取最近一周資料...\n")
elif run_mode == "B":
	print("B: 抓取日期清單所有資料...\n")
	file.write("B: 抓取日期清單所有資料...\n")
else:
	print("模式錯誤，結束程式...\n")
	file.write("模式錯誤，結束程式...\n")
	sys.exit("模式錯誤，結束程式...\n")

tStart = time.time()#計時開始
file.write("\n\n\n*** LOG datetime  " + str(datetime.datetime.now()) + " ***\n")
#file.write("結轉日期" + start_date + "~" + end_date + "\n")

#建立資料庫連線
conn = sqlite3.connect("market_price.sqlite")

#抓取網站日期清單
dt_list = GET_DATE_LIST()
#print(dt_list)

#依據所選模式抓取資料
if len(dt_list) > 0:
	#讀取上市櫃股票清單
	strsql  = "select SEAR_COMP_ID,COMP_NAME, STOCK_TYPE from STOCK_COMP_LIST "
	#strsql += "where SEAR_COMP_ID = '0050.TW' "
	strsql += "order by STOCK_TYPE, SEAR_COMP_ID "
	strsql += "limit 2"

	cursor = conn.execute(strsql)
	result = cursor.fetchall()

	df_result = pd.DataFrame()
	if len(result) > 0:
		for stock in result:
			#print(stock)

			if run_mode == "A":
				str_date = str(dt_list[-1:][0])
				#print(str_date)
				rt = GET_DATA(stock, str_date)
				DO_WAIT()	# 避免過度讀取網站，隨機間隔時間再讀取網頁

	#關閉cursor
	cursor.close()
else:
	print("$$$ 未取得日期清單資料，請確認來源網頁是否正常 $$$")



"""

date_fmt = "%Y%m%d"
a = datetime.datetime.strptime(start_date, date_fmt)
b = datetime.datetime.strptime(end_date, date_fmt)
delta = b - a
int_diff_date = delta.days
#print("days=" + str(int_diff_date) + "\n")

i = 1
cnt = 1
dt = ""
while i <= (int_diff_date+1):
	#print(str(i) + "\n")
	if i==1:
		str_date = start_date
	else:
		str_date = parser.parse(str(dt)).strftime("%Y%m%d")

	#print(str_date + "\n")
	print("擷取 " + str_date + " 集保戶股權分散表查詢.\n")
	#rt = GET_DATA(str_date)
	rt = GET_DATE_LIST()

	if rt == True:
		cnt += 1
		print(str_date + " 抓取程序正常結束.\n")
	
	dt = datetime.datetime.strptime(str_date, date_fmt).date()
	dt = dt + relativedelta(days=1)	
	i += 1
	
	# 累計抓滿有收盤資料90天就強制跳出迴圈
	#if cnt == 90:
	#	print("抓滿90天，強制結束.")
	#	file.write("抓滿90天，強制結束.\n")
	#	break




"""

tEnd = time.time()#計時結束
file.write("\n\n\n結轉耗時 %f sec\n" % (tEnd - tStart)) #會自動做進位
file.write("*** End LOG ***\n")

# Close File
file.close()

#關閉資料庫連線
conn.close()

#若執行過程無錯誤，執行結束後刪除log檔案
if err_flag == False:
	os.remove(name)

print("End of prog...")