# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 10:03:29 2017

@author: bryson0083
"""

import requests
from bs4 import BeautifulSoup
import json

name = "ggg.txt"
file = open(name, 'w', encoding = 'UTF-8')


#讀取帳密參數檔
with open('account.json') as data_file:
	data = json.load(data_file)

acc_id = data['lme']['id']
acc_pwd = data['lme']['pwd']

#print('acc=' + acc_id)
#print('pwd=' + acc_pwd)

# 登入網站
headers = {'User-Agent':'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
URL = 'https://www.metalprices.com/a/Login'

s = requests.session()
s.headers.update(headers)

payload = {
		"IsMobile": "False",
		"Username": acc_id,
		"Password": acc_pwd,
		"remember": "false"
		}

r = s.post(URL, data=payload, headers=headers)
r.encoding = "utf-8"
sp = BeautifulSoup(r.text, 'html.parser')
#print(sp)

rt_msg = str(sp.find('p'))
#print(rt_msg)

flag = rt_msg.find('Your account is currently logged into the website')
#print('\n\nflag=' + str(flag))

if flag > 0:
	print('有已登入的連線...')
	URL2 = 'https://www.metalprices.com/a/switchdevice?returnUrl=%2F'
	payload = {
		"mobile": "no"
	}
	r2 = s.post(URL2, data=payload, headers=headers)
	r2.encoding = "utf-8"
	
	file.write(r2.text)
	#print(r.text)
	
	sp2 = BeautifulSoup(r2.text, 'html.parser')
	#print(sp2)
	rt_msg2 = str(sp2.find('h4'))
	print(rt_msg2)
	
else:
	rt_msg = str(sp.find('title'))
	print(rt_msg)
	flag2 = rt_msg.find('Custom Dashboard')
	print("flag2=" + str(flag2))
	print('登入失敗')

#讀取網頁資料
URL = 'https://www.metalprices.com/dailyexchangedata/LMESummary/LME/LNI'

payload = {
		"Unit": "MT",
		"Currency": "usd"
		}

r = s.post(URL, data=payload, headers=headers)
r.encoding = "utf-8"

sp = BeautifulSoup(r.text, 'html.parser')
#print(sp)

table = sp.findAll('table', attrs={'class':'high_low'})
#print(table)

tb_cnt = len(table)
print("tb_cnt=" + str(tb_cnt))

i = 0
while i < tb_cnt:
	print("i=" + str(i) + "\n\n")
	data = [[td.text for td in row.select('td')]
					for row in table[i].select('tr')]
	print(data)
	i += 1 


# Close File
file.close()