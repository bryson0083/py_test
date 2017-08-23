import talib
from talib import MA_Type
import sqlite3
import numpy as np
import pandas as pd
import xlsxwriter
import datetime
from datetime import date, timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta
import sys, os.path
import time
import math, statistics

#K線型態判斷
def Stock_Ana(arg_stock, str_prev_date, str_today):
	sear_comp_id = arg_stock[0]
	#日線資料讀取
	strsql  = "select quo_date, open, high, low, close, vol from STOCK_QUO "
	strsql += "where "
	strsql += "SEAR_COMP_ID='" + sear_comp_id + "' and "
	strsql += "QUO_DATE between '" + str_prev_date + "' and '" + str_today + "' "
	strsql += "order by QUO_DATE "

	cursor = conn.execute(strsql)
	result = cursor.fetchall()

	none_flag = False
	if len(result) > 0:
		df = pd.DataFrame(result, columns = ['date','open','high','low','close','vol'])
		#print(df)
	else:
		none_flag = True

	#關閉cursor
	cursor.close()

	ls_result = []
	if none_flag == False:
		#LIST轉換為Numpy Array
		npy_high = np.array(df['high'])
		npy_low = np.array(df['low'])
		npy_close = np.array(df['close'])

		stock_vol = df['vol'].tail(6)/1000	#取近六天成交量，並由股換算為張
		last_vol = df['vol'].tail(1)/1000	#取最近一天成交量，並換算為張
		last_open = df['open'].tail(1)
		last_close = df['close'].tail(1)
		prev_close = df['close'].shift(1).tail(1)
		avg_vol = stock_vol.mean()	#取平均

		#最近一天交易日，成交量漲幅
		rt = 0
		if avg_vol > 0:
			rt = (last_vol.iloc[0] - avg_vol) / avg_vol * 100

		#最近一天交易日，K棒本體漲幅
		kbody_chg = 0
		if last_open.iloc[0] > 0:
			kbody_chg = (last_close.iloc[0] - last_open.iloc[0]) / last_open.iloc[0] * 100

		#最近一天交易日當天漲幅
		rise_rt = 0
		if prev_close.iloc[0] > 0:
			rise_rt = (last_close.iloc[0] - prev_close.iloc[0]) / prev_close.iloc[0] * 100

		#計算20MA
		ma20 = talib.MA(npy_close, timeperiod=20, matype=0)
		df['ma20'] = ma20

		#最近一個交易日20MA值
		last_20ma = df['ma20'].tail(1)

		#倒數第2個交易日20MA值
		prev_20ma = df['ma20'].shift(1).tail(1)

		#print('## last_close=' + str(last_close))
		#print(prev_close.iloc[0])

		# http://www.cmoney.tw/learn/course/technicals/topic/484
		# http://pythontrader.blogspot.tw/2015/05/ta-lib-usage-stoch.html
		# http://www.bituzi.com/2011/06/kd.html

		# http://www.tadoc.org/indicator/STOCH.htm
		slowk, slowd = talib.STOCH (npy_high,
									npy_low,
									npy_close,
									fastk_period=9,
									slowk_period=70,
									slowk_matype=0,
									slowd_period=30,
									slowd_matype=0)

		print("slowk=" + str(slowk[-1]))
		print("slowd=" + str(slowd[-1]))

		# http://www.tadoc.org/indicator/STOCHF.htm
		fastk, fastd = talib.STOCHF(npy_high,
									npy_low,
									npy_close,
									fastk_period=9,
									fastd_period=9,
									fastd_matype=0)

		print("fastk=" + str(fastk[-1]))
		print("fastd=" + str(fastd[-1]))

		# http://www.tadoc.org/indicator/STOCHRSI.htm
		fastk, fastd = talib.STOCHRSI(npy_close,
									timeperiod=9,
									fastk_period=3,
									fastd_period=3,
									fastd_matype=0)

		print("fastk=" + str(fastk[-1]))
		print("fastd=" + str(fastd[-1]))

		if (prev_close.iloc[0] <= prev_20ma.iloc[0]) and \
		   (last_close.iloc[0] > last_20ma.iloc[0]):
			print("##" + arg_stock[0] + "##" + arg_stock[1]  + "##\n")


		"""
		#三條均線變異數介於0~1間、最近一天成交量相對平均量成長20%、當天上漲3%以下、
		#最近一天收盤價在8MA跟50MA之上、成交量均量需大於500張
		if (var_val > 0 and var_val < 1) and \
		   rt >= 20 and \
		   (rise_rt > 0 and rise_rt < 3) and \
		   (last_close.iloc[0] > last_8ma.iloc[0]) and \
		   (last_close.iloc[0] > last_50ma.iloc[0]) and \
		   avg_vol > 500:

			#讀取個股籌碼資料
			strsql  = "select FR_BAS_CNT, IT_BAS_CNT, DE_BAS_CNT, RANK "
			strsql += "from REPORT_CHIP_ANA "
			strsql += "where "
			strsql += "SEAR_COMP_ID='" + sear_comp_id + "' "

			cursor = conn.execute(strsql)
			result = list(cursor.fetchone())

			if len(result) > 0:
				fr_bas_cnt = str(result[0])
				it_bas_cnt = str(result[1])
				de_bas_cnt = str(result[2])
				rank = result[3]
			else:
				fr_bas_cnt = "0"
				it_bas_cnt = "0"
				de_bas_cnt = "0"
				rank = " "

			#關閉cursor
			cursor.close()

			#print("##" + arg_stock[0] + "##" + arg_stock[1] + "##" + fr_bas_cnt + "##" + it_bas_cnt + "##" + de_bas_cnt + "##" + rank + "##\n")

			ls_result = [[arg_stock[0],arg_stock[1],var_val,rt,fr_bas_cnt,it_bas_cnt,de_bas_cnt,rank]]
			df_result = pd.DataFrame(ls_result, columns=['代號', '名稱', 'var', 'burst_rt','外資買賣超天數','投信買賣超天數','自營商買賣超天數','類別'])
		"""
	if len(ls_result) == 0:
		df_result = pd.DataFrame()

	return df_result

############################################################################
# Main                                                                     #
############################################################################
global err_flag
err_flag = False

#產生日期區間(當天日期，往前推90天)
today = datetime.datetime.now()
prev_date = today + timedelta(days=-90)

str_today = today.strftime("%Y%m%d")
str_prev_date = prev_date.strftime("%Y%m%d")

# 寫入LOG File
dt=datetime.datetime.now()
str_date = parser.parse(str(dt)).strftime("%Y%m%d")

name = "STOCK_SELECT_TYPE11_" + str_date + ".txt"
file = open(name, 'a', encoding = 'UTF-8')
tStart = time.time()#計時開始
file.write("\n\n\n*** LOG datetime  " + str(datetime.datetime.now()) + " ***\n")
file.write("偵測日期區間:" + str_prev_date + "~" + str_today + "\n")

#建立資料庫連線
conn = sqlite3.connect("market_price.sqlite")

strsql  = "select SEAR_COMP_ID,COMP_NAME, STOCK_TYPE from STOCK_COMP_LIST "
#strsql += "where SEAR_COMP_ID='0050.TW' "
strsql += "order by STOCK_TYPE, SEAR_COMP_ID "
strsql += "limit 1 "

cursor = conn.execute(strsql)
result = cursor.fetchall()

df_result = pd.DataFrame()
if len(result) > 0:
	for stock in result:
		print(stock)
		Stock_Ana(stock, str_prev_date, str_today)


#		try:
#			df = Stock_Ana(stock, str_prev_date, str_today)
#
#			if len(df)>0:
#				df_result = pd.concat([df_result, df], ignore_index=True)
#		except Exception as e:
#			err_flag = True
#			print("Function Stock_Ana raise exception:\n" + str(e) + "\n")

#關閉cursor
cursor.close()

#關閉資料庫連線
conn.close()

"""
#資料進行排序
if len(df_result)>0:
	df_result = df_result.sort_values(by=['類別', 'var', 'burst_rt'], ascending=[True, True, False])

#結果寫入EXCEL檔
file_name = 'STOCK_SELECT_TYPE11_' + str_date + '.xlsx'
writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
df_result.to_excel(writer, sheet_name='stock', index=False)
writer.save()

tEnd = time.time()#計時結束
file.write ("\n\n\n結轉耗時 %f sec\n" % (tEnd - tStart)) #會自動做進位
file.write("*** End LOG ***\n")

# Close File
file.close()

#若執行過程無錯誤，執行結束後刪除log檔案
if err_flag == False:
	os.remove(name)
"""
print("End of prog.")