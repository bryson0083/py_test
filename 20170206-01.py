import talib
from talib import MA_Type
import sqlite3
import numpy as np
import pandas as pd
import xlsxwriter
import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta

#檢查list數值是否呈現遞增，回傳Y/N
def CHK_IS_CONTINUE_UP(df):
	i = 0
	flag = "Y"
	for elem in df:
		if i == 0:
			prev_elem = elem
			i += 1
			continue
		else:
			if elem <= prev_elem:
				flag = "N"
				break
			else:
				prev_elem = elem

		i += 1

	return flag


#
def READ_HIST_QUO(sear_comp_id, str_prev_date, str_today):

	strsql  = "select close, quo_date from STOCK_QUO "
	strsql += "where "
	strsql += "SEAR_COMP_ID='" + sear_comp_id + "' and "
	strsql += "QUO_DATE between '" + str_prev_date + "' and '" + str_today + "' "
	strsql += "order by QUO_DATE "

	cursor = conn.execute(strsql)
	result = cursor.fetchall()
	re_len = len(result)

	if re_len > 0:
		close = []
		dt = []
		data = []
		for row in result:
			close.append(row[0])
			dt.append(row[1])
			data.append([row[1], row[0]])

	#print(close)
	#print(dt)
	#print(data)

	df = pd.DataFrame(data, columns = ['日期','收盤價'])

	#LIST轉換為Numpy Array
	close = np.array(close)

	#計算移動平均(ma20)
	ma20 = talib.MA(close, timeperiod=20, matype=0)

	#計算移動平均(ma60)
	ma60 = talib.MA(close, timeperiod=60, matype=0)

	#print(close)
	#print(ma20)
	#print(ma60)

	#均線 20 ma 值導到dataframe
	df['ma20'] = ma20

	#計算均線值與前一天的差(作為變動方向)
	df['ma20_diff_yesterday'] = df['ma20'] - df['ma20'].shift(1)

	#均線 60 ma 值導到dataframe
	df['ma60'] = ma60

	#計算均線值與前一天的差(作為變動方向)
	df['ma60_diff_yesterday'] = df['ma60'] - df['ma60'].shift(1)

	#計算均線間的距離(以百分比表示)
	df['dist_ma_pct'] = abs((df['ma60'] - df['ma20']) / df['ma20'] * 100)

	#檢查最新的三天ma20資料是否連三漲
	ma20_cnt_tot = len(df['ma20_diff_yesterday'])
	df_a = df['ma20_diff_yesterday'][ma20_cnt_tot-3:ma20_cnt_tot]
	#df_a = [-3.1,-2.5,0,4,6,7,8]
	#print(df_a)
	ma20_increment_yn = CHK_IS_CONTINUE_UP(df_a)
	#print("ma20_increment_yn=" + ma20_increment_yn)

	#檢查最新的三天ma60資料是否連三漲
	ma60_cnt_tot = len(df['ma60_diff_yesterday'])
	df_a = df['ma60_diff_yesterday'][ma60_cnt_tot-3:ma60_cnt_tot]
	#print(df_a)
	ma60_increment_yn = CHK_IS_CONTINUE_UP(df_a)
	#print("ma60_increment_yn=" + ma60_increment_yn)

	#最新一筆ma20大於ma60
	ma20_last = float(df['ma20'].tail(1))
	ma60_last = float(df['ma60'].tail(1))
	
	ma20bt60_yn = "N"
	if ma20_last > ma60_last:
		ma20bt60_yn = "Y"

	"""
	# for test 運算結果寫入EXCEL檔
	if sear_comp_id == "0050.TW":
		file_name = 'ma_sel_' + sear_comp_id + '.xlsx'
		writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
		df.to_excel(writer, sheet_name='stock', index=False)
		writer.save()
	"""

	#最後總評
	if ma20_increment_yn == "Y" and ma60_increment_yn == "Y" and ma20bt60_yn == "Y":
		READ_HIST_QUO = "Y"
	else:
		READ_HIST_QUO = "N"

	return READ_HIST_QUO

	#關閉cursor
	cursor.close()

############################################################################
# Main                                                                     #
############################################################################
#取得當天日期
dt = datetime.datetime.now()
str_today = parser.parse(str(dt)).strftime("%Y%m%d")
print(str_today)

#取得當天往前推180天日期
dt = datetime.datetime.now() + relativedelta(days=-180)
str_prev_date = str(dt)[0:10]
str_prev_date = parser.parse(str_prev_date).strftime("%Y%m%d")
print(str_prev_date)

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
		#print(row[0])
		select_yn = READ_HIST_QUO(row[0], str_prev_date, str_today)

		if select_yn == "Y":
			print("選出股票=" + row[0])

print("共選出" + str(i) + "檔股票...\n")

#關閉cursor
cursor.close()

#關閉資料庫連線
conn.close()

print("End of prog...")