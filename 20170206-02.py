import talib
from talib import MA_Type
import sqlite3
import numpy as np
import pandas as pd
import xlsxwriter
import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta


############################################################################
# Main                                                                     #
############################################################################
#取得當天日期
dt = datetime.datetime.now()
now_date = parser.parse(str(dt)).strftime("%Y/%m/%d")
print(now_date)

#dt_wday = datetime.datetime.today().isoweekday()
#print(dt_wday)

#設定結轉起始日期
start_date = '2000/01/01'

#計算區間的天數，作為迴圈終止條件
date_fmt = "%Y/%m/%d"
a = datetime.datetime.strptime(start_date, date_fmt)
b = datetime.datetime.strptime(now_date, date_fmt)
delta = b - a
int_diff_date = delta.days + 1
#print("days=" + str(int_diff_date) + "\n")

#for test
int_diff_date = 33

i = 1
dt = ""
duration_st = ""
duration_ed = ""
while i <= int_diff_date:
	#print(str(i) + "\n")
	if i==1:
		str_date = start_date
	else:
		str_date = parser.parse(str(dt)).strftime("%Y/%m/%d")
	
	#判斷該日期是星期幾(1~7表示周一到周日)
	dt_wday = datetime.datetime.strptime(str_date, '%Y/%m/%d').date().isoweekday()
	#print(str_date + "   " + str(dt_wday) + "\n")

	cal_yn = "N"
	if dt_wday == 1:
		duration_st = parser.parse(str(str_date)).strftime("%Y%m%d")
	elif duration_st > "" and dt_wday == 7:
		duration_ed = parser.parse(str(str_date)).strftime("%Y%m%d")
		cal_yn = "Y"
	else:
		duration_ed = parser.parse(str(str_date)).strftime("%Y%m%d")

	if i == int_diff_date:
		cal_yn = "Y"

	#若cal_yn為Y，結算一次周K
	if cal_yn == "Y":
		print("區間開始於" + duration_st + "~" + duration_ed + "\n")

	#日期往後推一天
	dt = datetime.datetime.strptime(str_date, date_fmt).date()
	dt = dt + relativedelta(days=1)
	i += 1










"""
#取得當天往前推180天日期
dt = datetime.datetime.now() + relativedelta(days=-180)
str_prev_date = str(dt)[0:10]
str_prev_date = parser.parse(str_prev_date).strftime("%Y%m%d")
#print(str_prev_date)

#建立資料庫連線
conn = sqlite3.connect("market_price.sqlite")

strsql  = "select distinct SEAR_COMP_ID from STOCK_QUO "
strsql += "where "
strsql += "QUO_DATE between '" + str_prev_date + "' and '" + str_today + "' "
strsql += "order by SEAR_COMP_ID "
#strsql += "limit 1 "

cursor = conn.execute(strsql)
result = cursor.fetchall()
re_len = len(result)

if re_len > 0:
	i = 0
	for row in result:
		i += 1
		print(row[0])

		if select_yn == "Y":
			print("選出股票=" + row[0])

print("共選出" + str(i) + "檔股票...\n")

#關閉cursor
cursor.close()

#關閉資料庫連線
conn.close()
"""

print("End of prog...")