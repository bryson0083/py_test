import pandas as pd
import pandas_datareader.data as web
import datetime
start = datetime.datetime.strptime('11/01/2016', '%m/%d/%Y')
end = datetime.datetime.strptime('11/08/2016', '%m/%d/%Y')

# 讀取股價資料

try:
	#com_stock = web.DataReader('2002.TW','yahoo',start,end)
	#com_stock = web.DataReader("TPE:2002", 'google', start, end)
	com_stock = web.DataReader('HKG%3A0700','google',start,end)

	# 全部資料
	print("原始資料 From Yahoo\n" + str(com_stock) + "\n")
except:
	print("無法讀取股價資料，或無資料!!")

