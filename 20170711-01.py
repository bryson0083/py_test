"""
券商進出分點資料查詢(上市、上櫃)

說明:
抓取台股上市櫃公司，每日券商進出分點資料。
分三種模式抓取

mode_c: 
mode_h: 
mode_a: 

資料來源:
網站: https://www.nvesto.com/
資料: https://www.nvesto.com/tpe/2034/majorForce#!/fromdate/2017-07-04/todate/2017-07-04/view/summary

備註:
由於證交所、櫃買中心進出分點僅提供當天資料，歷史資料未提供。
因此直接從nvesto網站抓取。

GET_BROKER_TRADING.py
"""
import os
import time
import datetime
from random import randint
import requests
from bs4 import BeautifulSoup
import json
import codecs
import pandas as pd
from dateutil import parser
from dateutil.relativedelta import relativedelta
import sqlite3

def DO_WAIT():
	#隨機等待一段時間
	#sleep_sec = randint(30,120)
	sleep_sec = randint(5,10)
	print("間隔等待 " + str(sleep_sec) + " secs.\n")
	time.sleep(sleep_sec)


def CHK_DATA_EXIST(arg_sear_comp_id, arg_quo_date):
	arg_quo_date = parser.parse(arg_quo_date).strftime("%Y%m%d")

	#檢查當天該股票是否已有資料
	strsql  = "select count(*) from STOCK_BROKER_BS "
	strsql += "where "
	strsql += "QUO_DATE = '" + arg_quo_date + "' and "
	strsql += "SEAR_COMP_ID = '" + arg_sear_comp_id + "' "

	cursor = conn.execute(strsql)
	result = cursor.fetchone()
	rows_cnt = result[0]

	#關閉cursor
	cursor.close()

	return rows_cnt

def Login_nvesto():
	global err_flag, s, headers
	flag = False

	#讀取帳密參數檔
	with open('account.json') as data_file:
		data = json.load(data_file)

	acc_id = data['nvesto']['id']
	acc_pwd = data['nvesto']['pwd']
	#print('acc=' + acc_id)
	#print('pwd=' + acc_pwd)

	#網站登入
	URL = 'https://www.nvesto.com/user/login?normal_login=1'

	payload = {
			'LoginForm[email]': acc_id,
			'LoginForm[password]': acc_pwd,
			'LoginForm[rememberMe]': '0'
			}

	r = s.post(URL, data=payload, headers=headers)
	#print(r.text)

	#確認登入網站是否成功(成功登入可以看到使用者代號)
	URL = 'https://www.nvesto.com/'
	r = s.get(URL, headers=headers)
	#print(r.text)

	sp = BeautifulSoup(r.text, 'html.parser')
	div_msg = sp.findAll('div', attrs={'id':'userlogin-click'})
	#print(div_msg)
	user_id_posi = str(div_msg).find("Bryson Xue")

	if user_id_posi > 0:
		flag = True

	return flag


def READ_BROKER_BS(arg_df, arg_date):
	global err_flag, s, headers
	#print(arg_date)
	#print(arg_df)

	for i in range(0,len(arg_df)):
		sear_comp_id = str(arg_df.loc[i]['SEAR_COMP_ID'])
		comp_id = str(arg_df.loc[i]['COMP_ID'])
		comp_name = str(arg_df.loc[i]['COMP_NAME'])
		#print(comp_id)

		#檢查資料庫是否已有資料存在，若已有資料則略過，減少網站讀取
		rt_cnt = CHK_DATA_EXIST(sear_comp_id, arg_date)
		#print("rt_cnt=" + str(rt_cnt))
		if rt_cnt == 0:	#確認資料庫無資料，讀取網頁資料
			print("抓取" + sear_comp_id + " " + comp_name + " 日期:" + arg_date + " 券商進出分點資料.")
			file.write("抓取" + sear_comp_id + " " + comp_name + " 日期:" + arg_date + " 券商進出分點資料.")

			all_df = pd.DataFrame()

			#讀取查詢網頁結果
			URL = 'https://www.nvesto.com/tpe/' + comp_id + '/majorForce#!/fromdate/' + arg_date + '/todate/' + arg_date + '/view/summary'
			r = s.get(URL, headers=headers)
			sp = BeautifulSoup(r.text, 'html.parser')
			rt_msg = sp.findAll('script', type="text/javascript")[4]
			#print(rt_msg)

			#For test 讀取local網頁存檔
			#f=codecs.open("C:/Users/bryson0083/Desktop/Nvesto.html", 'r',encoding = 'utf8')
			#data = f.read()
			#sp = BeautifulSoup(data, 'html.parser')
			#rt_msg = sp.findAll('script', type="text/javascript")[6]
			#print(rt_msg)

			#讀取券商進出(買超)
			str_buy = rt_msg
			msg_posi = str(str_buy).find("MajorForce_JS_VARS")
			str_buy = str(str_buy)[msg_posi:]
			msg_posi = str(str_buy).find("[")
			str_buy = str(str_buy)[msg_posi:]
			msg_posi = str(str_buy).find("]")
			str_buy = str(str_buy)[:msg_posi+1]

			js_buy_data = json.loads(str_buy)
			df_buy = pd.DataFrame.from_dict(js_buy_data, orient='columns')
			df_buy = df_buy.loc[:,['name', 'buy', 'sell', 'net', 'price', 'level']]
			#print(df_buy)
			all_df = pd.concat([all_df,df_buy],ignore_index=True)

			#讀取券商進出(賣超)
			str_sell = rt_msg
			msg_posi = str(str_sell).find("MajorForce_JS_VARS")
			str_sell = str(str_sell)[msg_posi:]
			msg_posi = str(str_sell).find("[")
			str_sell = str(str_sell)[msg_posi+1:]
			msg_posi = str(str_sell).find("[")
			str_sell = str(str_sell)[msg_posi:]
			msg_posi = str(str_sell).find("]")
			str_sell = str(str_sell)[:msg_posi+1]

			js_sell_data = json.loads(str_sell)
			df_sell = pd.DataFrame.from_dict(js_sell_data, orient='columns')
			df_sell = df_sell.loc[:,['name', 'buy', 'sell', 'net', 'price', 'level']]
			#print(df_sell)
			all_df = pd.concat([all_df,df_sell],ignore_index=True)
			#print(all_df)

			#資料寫入料庫
			arg_ls = [arg_date, sear_comp_id, comp_name]
			flag = STORE_DB(arg_ls, all_df)

			if flag == True:
				print("資料庫寫入成功.\n")
				file.write("資料庫寫入成功.\n")

			DO_WAIT()	# 避免過度讀取網站，隨機間隔時間再讀取網頁

		else:
			err_flag = True
			print(sear_comp_id + " " + comp_name + " 日期" + arg_date + " 資料筆數=" + str(rt_cnt) + " 資料已存在，不再重新抓取.\n")
			file.write(sear_comp_id + " " + comp_name + " 日期" + arg_date + " 資料筆數=" + str(rt_cnt) +  " 資料已存在，不再重新抓取.\n")


def STORE_DB(arg_ls, arg_df):
	global err_flag
	rt_flag = True

	quo_date = parser.parse(arg_ls[0]).strftime("%Y%m%d")
	sear_comp_id = arg_ls[1]
	comp_name = arg_ls[2]
	df = arg_df

	#資料寫入資料庫
	for index, row in df.iterrows():
		# 最後維護日期時間
		str_date = str(datetime.datetime.now())
		date_last_maint = parser.parse(str_date).strftime("%Y%m%d")
		time_last_maint = parser.parse(str_date).strftime("%H%M%S")
		prog_last_maint = "GET_BROKER_TRADING"

		strsql  = "insert into STOCK_BROKER_BS ('QUO_DATE', 'SEAR_COMP_ID', 'COMP_NAME', 'BROKER_NAME', 'BUY_VOL', 'SELL_VOL', 'NET_VOL', 'AVG_PRICE', 'LV', 'DATE_LAST_MAINT', 'TIME_LAST_MAINT', 'PROG_LAST_MAINT') values ("
		strsql += "'" + quo_date + "', "
		strsql += "'" + sear_comp_id + "', "
		strsql += "'" + comp_name + "', "
		strsql += "'" + row['name'] + "', "
		strsql += str(row['buy']) + ", "
		strsql += str(row['sell']) + ", "
		strsql += str(row['net']) + ", "
		strsql += str(row['price']) + ", "
		strsql += str(row['level']) + ", "
		strsql += "'" + date_last_maint + "', "
		strsql += "'" + time_last_maint + "', "
		strsql += "'" + prog_last_maint + "' "
		strsql += ")"

		try :
			#print(strsql)
			conn.execute(strsql)
			conn.commit()
		except sqlite3.Error as er:
			err_flag = True
			rt_flag = False
			conn.execute("rollback")
			print("insert STOCK_BROKER_BS er=" + er.args[0] + "\n")
			print(strsql + "\n")
			file.write("insert STOCK_BROKER_BS er=" + er.args[0] + "\n")
			file.write(strsql + "\n")

	return rt_flag

#############################################################################
# Main																		#
#############################################################################
print("Executing GET_BROKER_TRADING...")

#全域變數設定
global err_flag, s, headers
err_flag = False

#Web Session, Header設定
s = requests.session()
headers = {'User-Agent':'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}

# 建立資料庫連線
conn = sqlite3.connect('market_price.sqlite')

# 寫入LOG File
dt = datetime.datetime.now()

print("##############################################")
print("##              Nvesto 上市櫃公司           ##")
print("##          券商每日進出分點資料讀取        ##")
print("##                                          ##")
print("##   datetime: " + str(dt) +            "   ##")
print("##############################################")

str_date = str(dt)
str_date = parser.parse(str_date).strftime("%Y%m%d")

name = "GET_BROKER_TRADING_LOG_" + str_date + ".txt"
file = open(name, 'a', encoding = 'UTF-8')

tStart = time.time()#計時開始
file.write("\n\n\n*** LOG datetime  " + str(datetime.datetime.now()) + " ***\n")

#登入網站
Login_nvesto = Login_nvesto()
#print(Login_nvesto)

if Login_nvesto == True:
	print("Nvesto網站登入成功. \n")
else:
	file.write("$$$ Nvesto網站登入失敗，程式中止. $$$")
	sys.exit("$$$ Nvesto網站登入失敗，程式中止. $$$")

	#關閉LOG檔、資料庫連線
	file.close()
	conn.close()

#讀取上市櫃公司清單
strsql  = "select SEAR_COMP_ID, COMP_ID, COMP_NAME, STOCK_TYPE from STOCK_COMP_LIST "
#strsql += "where SEAR_COMP_ID = '2034.TW' "
strsql += "order by STOCK_TYPE, SEAR_COMP_ID "
strsql += "limit 2"

df = pd.read_sql_query(strsql, conn)
#print(df)

#起訖日期(預設跑當天日期到往前推7天)
dt = datetime.datetime.now()
date_fmt = "%Y-%m-%d"
start_date = dt + datetime.timedelta(days=-7)
start_date = parser.parse(str(start_date)).strftime(date_fmt)
end_date = parser.parse(str(dt)).strftime(date_fmt)

#for需要時手動設定日期區間用
start_date = "2017-07-10"
end_date = "2017-07-10"

print("抓取日期" + start_date + "~" + end_date)

#計算區間的天數，作為迴圈終止條件
a = datetime.datetime.strptime(start_date, date_fmt)
b = datetime.datetime.strptime(end_date, date_fmt)
delta = b - a
int_diff_date = delta.days + 1
#print("days=" + str(int_diff_date) + "\n")

i = 1
dt = ""
while i <= int_diff_date:
	#print(str(i) + "\n")
	if i==1:
		str_date = start_date
	else:
		str_date = parser.parse(str(dt)).strftime(date_fmt)
		
	#print(str_date + "\n")
	#讀取日期當天進出分點資料
	READ_BROKER_BS(df, str_date)
	
	#日期往後推一天
	dt = datetime.datetime.strptime(str_date, date_fmt).date()
	dt = dt + relativedelta(days=1)
	i += 1

tEnd = time.time()#計時結束
file.write ("\n\n\n結轉耗時 %f sec\n" % (tEnd - tStart)) #會自動做進位
file.write("*** End LOG ***\n")

# Close File
file.close()

#若執行過程無錯誤，執行結束後刪除log檔案
if err_flag == False:
	os.remove(name)

print("End of prog...")