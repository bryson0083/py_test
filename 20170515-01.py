import talib
from talib import MA_Type
import sqlite3
import numpy as np
import pandas as pd
import xlsxwriter
import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta
import sys
import time
import math, statistics

#檢查list數值是否呈現遞減(mode='D')或遞增(mode='U')，回傳Y/N
def trend_chk(df, mode):
	i = 0
	flag = "Y"
	for elem in df:
		if i == 0:
			prev_elem = elem
			i += 1
			continue
		else:
			if (mode == "D") and (elem >= prev_elem):
				flag = "N"
				break
			elif (mode == "U") and (elem <= prev_elem):
				flag = "N"
				break
			else:
				prev_elem = elem
		i += 1
	return flag

#K線型態判斷
def Patt_Recon(arg_stock, str_prev_date, str_today):
	sear_comp_id = arg_stock[0]
	#日線資料讀取
	strsql  = "select quo_date, open, high, low, close, vol from STOCK_QUO "
	#strsql  = "select quo_date, open, high, low, close from STOCK_QUO_WEEKLY "
	#strsql  = "select quo_date, open, high, low, close from STOCK_QUO_MONTH "
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
		npy_close = np.array(df['close'])
		stock_vol = df['vol'].tail(6)/1000	#取近六天成交量，並由股換算為張
		last_vol = df['vol'].tail(1)/1000	#取最近一天成交量，並換算為張
		last_open = df['open'].tail(1)
		last_close = df['close'].tail(1)
		avg_vol = stock_vol.mean()	#取平均

		#print(last_vol.iloc[0])
		#sys.exit("test end...")
		rt = 0
		if avg_vol > 0:
			rt = (last_vol.iloc[0] - avg_vol) / avg_vol * 100

		chg = 0
		if last_open.iloc[0] > 0:
			chg = (last_close.iloc[0] - last_open.iloc[0]) / last_open.iloc[0] * 100

		#print(stock_vol.mean())
		#sys.exit("test end...")

		#計算6MA
		ma6 = talib.MA(npy_close, timeperiod=6, matype=0)
		df['ma6'] = ma6

		#計算18MA
		ma18 = talib.MA(npy_close, timeperiod=18, matype=0)
		df['ma18'] = ma18

		#計算50MA
		ma50 = talib.MA(npy_close, timeperiod=50, matype=0)
		df['ma50'] = ma50

		last_50ma = df['ma50'].tail(1)

		#三條MA線近六天的數值，全部丟到一個list下，一起計算變異數
		ls_ma = []
		ls_ma.extend(df['ma6'].tail(6))
		ls_ma.extend(df['ma18'].tail(6))
		ls_ma.extend(df['ma50'].tail(6))
		var_val = statistics.variance(ls_ma)
		#print(var_val)
		"""
		sys.exit("test end...")


		# for test 股價原始資料寫入EXCEL檔
		file_name = 'TOU_TEST.xlsx'
		writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
		df.to_excel(writer, sheet_name='stock', index=False)
		writer.save()
		"""
		if avg_vol > 500 and rt > 0 and chg >= 3 and (last_close.iloc[0] > last_50ma.iloc[0]):
			ls_result = [[arg_stock[0],arg_stock[1],var_val,rt]]
			df_result = pd.DataFrame(ls_result, columns=['stock_id', 'stock_name', 'var', 'burst_rt'])


	if len(ls_result) == 0:
		df_result = pd.DataFrame()

	return df_result

############################################################################
# Main                                                                     #
############################################################################
#回測日期區間
str_prev_date = "20170101"
str_today = "20170515"

# 寫入LOG File
dt=datetime.datetime.now()
str_date = parser.parse(str(dt)).strftime("%Y%m%d")

name = "PATT_RECON_" + str_date + ".txt"
file = open(name, 'a', encoding = 'UTF-8')
tStart = time.time()#計時開始
file.write("\n\n\n*** LOG datetime  " + str(datetime.datetime.now()) + " ***\n")
file.write("回測日期區間:" + str_prev_date + "~" + str_today + "\n")

#建立資料庫連線
conn = sqlite3.connect("market_price.sqlite")

strsql  = "select SEAR_COMP_ID,COMP_NAME, STOCK_TYPE from STOCK_COMP_LIST "
#strsql += "where STOCK_TYPE = '上櫃' and SEAR_COMP_ID='3662.TW' "
strsql += "order by STOCK_TYPE, SEAR_COMP_ID "
#strsql += "limit 1 "

cursor = conn.execute(strsql)
result = cursor.fetchall()

df_result = pd.DataFrame()
if len(result) > 0:
	for stock in result:
		print(stock)
		df = Patt_Recon(stock, str_prev_date, str_today)

		if len(df)>0:
			df_result = pd.concat([df_result, df], ignore_index=True)

#關閉cursor
cursor.close()

#關閉資料庫連線
conn.close()

#結果寫入CSV FILE
#print(df_result)
df_result.to_csv('PATT_RECON_RESULTxxxx.csv', encoding='utf-8')

tEnd = time.time()#計時結束
file.write ("\n\n\n結轉耗時 %f sec\n" % (tEnd - tStart)) #會自動做進位
file.write("*** End LOG ***\n")

# Close File
file.close()

print("End of prog.")
