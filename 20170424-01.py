import sqlite3
import datetime
from dateutil import parser
import pandas as pd

def Cal_Adj_Price(arg_df):
	for i in range(0,len(arg_df)):
		comp_id = arg_df['COMP_ID'][i]
		comp_name = arg_df['COMP_NAME'][i]
		xd_date = arg_df['XD_DATE'][i]
		prev_xd_date = arg_df['PREV_XD_DATE'][i]
		cash = arg_df['CASH'][i]
		xr_date = arg_df['XR_DATE'][i]
		prev_xr_date = arg_df['PREV_XR_DATE'][i]
		sre = arg_df['SRE'][i]

		ls = []
		if (len(xd_date) > 0 and len(prev_xd_date)==0) or (len(xr_date) > 0 and len(prev_xr_date)==0):
			ls = [row for row in arg_df.iloc[i]]
			print(ls)



####################################################
# main                                             #
####################################################
dt = str(datetime.datetime.now())
str_date = parser.parse(dt).strftime("%Y%m%d")
now_yyyy = int(parser.parse(dt).strftime("%Y"))

#print(str_date)
#print(now_yyyy)

#建立資料庫連線
conn = sqlite3.connect("market_price.sqlite")

#for y in range(2004,now_yyyy,1):
for y in range(2015,2016,1):
	print(y)
	pre_yyyy = str(y - 1)
	strsql  = "select a.COMP_ID, a.COMP_NAME, a.XD_DATE,"
	strsql += "(select XD_DATE from stock_dividend where comp_id = a.comp_id and setm_year='" + pre_yyyy + "') as PRE_XD_DATE,"
	strsql += "a.CASH,a.XR_DATE,"
	strsql += "(select XR_DATE from stock_dividend where comp_id = a.comp_id and setm_year='" + pre_yyyy + "') as PRE_XR_DATE,"
	strsql += "SRE "
	strsql += "from stock_dividend a "
	strsql += "where a.setm_year='" + str(y) + "' "
	strsql += "order by a.COMP_ID "
	#strsql += "limit 1 "

	#print(strsql)
	cursor = conn.execute(strsql)
	result = cursor.fetchall()

	df = pd.DataFrame(result, columns=['COMP_ID','COMP_NAME','XD_DATE','PREV_XD_DATE','CASH','XR_DATE','PREV_XR_DATE','SRE'])
	df = df.fillna('')

	#計算還原股價
	Cal_Adj_Price(df)

	#關閉cursor
	cursor.close()
	#print(df)
	
#關閉資料庫連線
conn.close()
