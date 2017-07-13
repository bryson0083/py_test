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
from selenium import webdriver
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

def Login_nvesto(s):
	#global s, headers
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


global s, headers

driver = webdriver.PhantomJS() # or add to your PATH


#Web Session, Header設定
s = requests.session()
headers = {'User-Agent':'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}

#登入網站
Login_nvesto = Login_nvesto(s)
print(Login_nvesto)

#讀取查詢網頁結果
URL = 'https://www.nvesto.com/tpe/2034/majorforce#!/fromdate/2017-07-12/todate/2017-07-12/view/summary'
r = s.get(URL, headers=headers)
#print(r.text)
#sp = BeautifulSoup(r.text, 'html.parser')
sp = BeautifulSoup(r.content)
#rt_msg = sp.findAll('script', type="text/javascript")[4]
#print(rt_msg)

#For test 讀取local網頁存檔
#f=codecs.open("C:/Users/bryson0083/Desktop/Nvesto.html", 'r',encoding = 'utf8')
#data = f.read()
#print(data)
#sp = BeautifulSoup(data, 'html.parser')

#rt_msg = sp.findAll('script', type="text/javascript")[6]
#print(rt_msg)

table_buy = sp.findAll('table', attrs={'class':'table table-bordered'})
#table_buy = sp.findAll('script', attrs={'class':'majorforce-tmpl'})
print(table_buy)
#table_sell = sp.findAll('table', attrs={'class':'table table-bordered'})[3]
#print(table_sell)












"""
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
"""