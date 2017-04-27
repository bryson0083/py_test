import sqlite3
import datetime
from dateutil import parser
import pandas as pd

def Cal_Adj_Price(arg_df):
	file_name = "aaa.txt"
	file = open(file_name, 'w', encoding="UTF-8")

	for i in range(0,len(arg_df)):
		comp_id = arg_df['COMP_ID'][i]
		comp_name = arg_df['COMP_NAME'][i]
		xd_date = arg_df['XD_DATE'][i]
		prev_xd_date = arg_df['PREV_XD_DATE'][i]
		cash = arg_df['CASH'][i]
		xr_date = arg_df['XR_DATE'][i]
		prev_xr_date = arg_df['PREV_XR_DATE'][i]
		sre = arg_df['SRE'][i]

		"""
		ls = []
		if (len(xd_date) > 0 and len(prev_xd_date)==0) or (len(xr_date) > 0 and len(prev_xr_date)==0):
			ls = str([str(row).strip() for row in arg_df.iloc[i]])
			print(ls)
			file.write(ls + "\n")
		"""

		#除息日期處理，若本年度有除息，但去年沒有，則給予預設的去年除息日期為，
		#本年度除息日期，往前推一年時間
		if len(xd_date.strip()) > 0 and len(prev_xd_date.strip())==0:
			#print(xd_date)
			tmp_dt = datetime.datetime.strptime(xd_date, "%Y%m%d")
			prev_date = tmp_dt + datetime.timedelta(days=-365)
			prev_date = str(prev_date)[0:10]
			prev_date = parser.parse(prev_date).strftime("%Y%m%d")
			prev_xd_date = prev_date

			#print(comp_id + " " + comp_name + " " + xd_date + " " + prev_xd_date + " " + str(cash) + "\n")

		#調整除息，起始日期(使用前一年度除息日期作為調整起始日期)
		if len(prev_xd_date.strip()) > 0:
			xd_adj_start_date = prev_xd_date
		else:
			xd_adj_start_date = ""

		#調整除息，結束日期(使用本年度除息日期往前推一天，作為調整結束日期)
		if len(xd_date.strip()) > 0:
			tmp_dt = datetime.datetime.strptime(xd_date, "%Y%m%d")
			prev_date = tmp_dt + datetime.timedelta(days=-1)
			prev_date = str(prev_date)[0:10]
			prev_date = parser.parse(prev_date).strftime("%Y%m%d")
			xd_adj_end_date = prev_date
		else:
			xd_adj_end_date = ""

		#除權日期處理，若本年度有除權，但去年沒有，則給予預設的去年除權日期為，
		#本年度除權日期，往前推一年時間
		if len(xr_date.strip()) > 0 and len(prev_xr_date.strip())==0:
			#print(xd_date)
			tmp_dt = datetime.datetime.strptime(xr_date, "%Y%m%d")
			prev_date = tmp_dt + datetime.timedelta(days=-365)
			prev_date = str(prev_date)[0:10]
			prev_date = parser.parse(prev_date).strftime("%Y%m%d")
			prev_xr_date = prev_date

		#	print(comp_id + " " + comp_name + " " + xr_date + " " + prev_xr_date + " " + str(sre) + "\n")

		#調整除權，起始日期(使用前一年度除權日期作為調整起始日期)
		if len(prev_xr_date.strip()) > 0:
			xr_adj_start_date = prev_xr_date
		else:
			xr_adj_start_date = ""

		#調整除權，結束日期(使用本年度除權日期往前推一天，作為調整結束日期)
		if len(xr_date.strip()) > 0:
			tmp_dt = datetime.datetime.strptime(xr_date, "%Y%m%d")
			prev_date = tmp_dt + datetime.timedelta(days=-1)
			prev_date = str(prev_date)[0:10]
			prev_date = parser.parse(prev_date).strftime("%Y%m%d")
			xr_adj_end_date = prev_date
		else:
			xr_adj_end_date = ""

		#print(comp_id + ", " + comp_name + ", " + xd_date + ", " + prev_xd_date + ", " + xd_adj_start_date + ", " + xd_adj_end_date + "\n")

		#考慮除息後，還原股價
		strsql  = "select QUO_DATE, OPEN, HIGH, LOW, CLOSE "
		strsql += "from STOCK_QUO "
		strsql += "where "
		strsql += "SEAR_COMP_ID ='" + comp_id + ".TW' and "
		strsql += "QUO_DATE between '" + xd_adj_start_date + "' and '" + xd_adj_start_date + "' "
		strsql += "ORDER BY QUO_DATE "

		print(strsql)
		cursor = conn.execute(strsql)
		result = cursor.fetchall()

		if len(result) > 0:
			for i in range(0, len(result), 1):
				quo_date = result[i][0]
				o_price = result[i][1]
				h_price = result[i][2]
				l_price = result[i][3]
				c_price = result[i][4]

				print(quo_date + " " + str(o_price) + " " + str(h_price) + " " + str(l_price) + " " + str(c_price) + "\n")

		#關閉cursor
		cursor.close()


	file.close()



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
	strsql += "limit 1 "

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
