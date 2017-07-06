import requests
from bs4 import BeautifulSoup
import json
import re

import sys
import codecs

from lxml import etree
import pandas as pd
#import xml.etree.cElementTree as etree
#import xml.etree.ElementTree as etree

def Login_nvesto(s):
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

	return True





err_flag = False
s = requests.session()
headers = {'User-Agent':'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}

#登入網站
#Login_nvesto = Login_nvesto(s)
#print(Login_nvesto)

#URL = 'https://www.nvesto.com/'
#URL = 'https://www.nvesto.com/tpe/2034/majorForce#!/fromdate/2017-07-04/todate/2017-07-04/view/summary'
#r = s.get(URL, headers=headers)
#r.encoding = "utf-8"
#sp = BeautifulSoup(r.text, 'html.parser')
#print(sp)
#rt_msg = str(sp.findAll('script', type="text/javascript"))
#print(rt_msg)
#msg_posi = str(rt_msg).find("MajorForce_JS_VARS")
#print(str(rt_msg)[msg_posi:])
#print(msg_posi)

f=codecs.open("C:/Users/bryson0083/Desktop/Nvesto.html", 'r',encoding = 'utf8')
#print(f.read())

data = f.read()
#data.encoding = "utf-8"
sp = BeautifulSoup(data, 'html.parser')
rt_msg = sp.findAll('script', type="text/javascript")[6]
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
print(df_sell)