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
import requests
from bs4 import BeautifulSoup
import json
import codecs
import pandas as pd
from dateutil import parser
from dateutil.relativedelta import relativedelta
import sqlite3

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
		comp_id = str(arg_df.loc[i]['COMP_ID'])
		#print(comp_id)

		#讀取查詢網頁結果
		#URL = 'https://www.nvesto.com/tpe/2034/majorForce#!/fromdate/2017-07-04/todate/2017-07-04/view/summary'
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
		print(df_buy)


		print("\n\n\n")

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
		print(df_sell)



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

if Login_nvesto == False:
	file.write("$$$ Nvesto網站登入失敗，程式中止. $$$")
	sys.exit("$$$ Nvesto網站登入失敗，程式中止. $$$")

	#關閉LOG檔、資料庫連線
	file.close()
	conn.close()

#讀取上市櫃公司清單
strsql  = "select SEAR_COMP_ID, COMP_ID, COMP_NAME, STOCK_TYPE from STOCK_COMP_LIST "
strsql += "where SEAR_COMP_ID = '2034.TW' "
strsql += "order by STOCK_TYPE, SEAR_COMP_ID "
strsql += "limit 1"

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