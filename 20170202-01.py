# -*- coding: utf-8 -*-
# TA-Lib僅能在python 3.4下執行
# matplotlib顯示中文碼有問題，因此先以英文為主

import talib
from talib import MA_Type
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

#建立資料庫連線
conn = sqlite3.connect("market_price.sqlite")

strsql  = "select close, quo_date from STOCK_QUO "
strsql += "where "
strsql += "SEAR_COMP_ID='2014.TW' and "
strsql += "QUO_DATE between '20150101' and '20170127' "
strsql += "order by QUO_DATE"

cursor = conn.execute(strsql)
result = cursor.fetchall()
re_len = len(result)

if re_len > 0:
	close = []
	dt = []
	for row in result:
		close.append(row[0])
		dt.append(row[1])

print(close)
print(dt)

#關閉cursor
cursor.close()

#關閉資料庫連線
conn.close()

####################################################################

#直接指定收盤價(不讀取資料庫)
#close = [1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0]

#LIST轉換為Numpy Array
price = np.array(close)

#計算移動平均(MA18)
ma18 = talib.MA(np.array(close), timeperiod=18, matype=0)

#計算移動平均(MA50)
ma50 = talib.MA(np.array(close), timeperiod=50, matype=0)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

#直接畫線
#plt.plot(price, 'b-', label="Close")
#plt.plot(ma18, 'g-', label="MA18")
#plt.plot(ma50, 'y-', label="MA50")

#畫日期與收盤價
ax.plot_date(dt,price,'-',xdate=True, ydate=False, label='Close')

#畫日期與移動均線(ma18)
ax.plot_date(dt,ma18,'-',xdate=True, ydate=False, label='ma18')

#畫日期與移動均線(ma50)
ax.plot_date(dt,ma50,'-',xdate=True, ydate=False, label='ma50')

#設定圖形的抬頭
plt.title('STOCK CLOSE PRICE and MA')
plt.xlabel('QUO_DATE (YYYYMMDD)')
plt.ylabel('Close ($)')

#設定圖形帶格線
plt.grid(True)

#X軸的日期顯示變成斜的
fig.autofmt_xdate()

#顯示不同標線的說明
plt.legend()

#顯示圖形
plt.show()