import talib
from talib import MA_Type
import sqlite3
import numpy as np
import pandas as pd
import xlsxwriter

#建立資料庫連線
conn = sqlite3.connect("market_price.sqlite")

strsql  = "select close, quo_date from STOCK_QUO "
strsql += "where "
strsql += "SEAR_COMP_ID='2014.TW' and "
strsql += "QUO_DATE between '20160601' and '20170203' "
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
ma20 = talib.MA(close, timeperiod=10, matype=0)

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

# for test 運算結果寫入EXCEL檔
file_name = 'ma.xlsx'
writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
df.to_excel(writer, sheet_name='stock', index=False)
writer.save()

#關閉cursor
cursor.close()

#關閉資料庫連線
conn.close()