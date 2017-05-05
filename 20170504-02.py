import sqlite3
import datetime
from datetime import date, timedelta
from dateutil import parser
import pandas as pd
import time

def f(d1, d2):
	delta = d2 - d1
	return set([d1 + timedelta(days=i) for i in range(delta.days + 1)])

def Date_Overlap(range1, range2):
	#判斷兩日期區間，做set_itsec
	set_itsec = f(*range1[0:2]) & f(*range2[0:2])
	xr = range1[2]
	xd = range2[2]

	ls_date = []
	if set_itsec:
		dt1 = min(set_itsec).strftime('%Y%m%d')
		dt2 = max(set_itsec).strftime('%Y%m%d')
		ls_date.append([dt1, dt2, xr, xd])

		if min(set_itsec) != min(min(range1[0:2]),min(range2[0:2])):
			dt1 = min(min(range1[0:2]),min(range2[0:2])).strftime('%Y%m%d')
			dt2 = (min(set_itsec) + timedelta(days=-1)).strftime('%Y%m%d')
			if min(range1[0:2]) < min(range2[0:2]):
				ls_date.append([dt1, dt2, xr, 0])
			else:
				ls_date.append([dt1, dt2, 0, xd])


		if max(set_itsec) != max(max(range1[0:2]),max(range2[0:2])):
			dt1 = (max(set_itsec) + timedelta(days=1)).strftime('%Y%m%d')
			dt2 = max(max(range1[0:2]),max(range2[0:2])).strftime('%Y%m%d')

			if max(range1[0:2]) > max(range2[0:2]):
				ls_date.append([dt1, dt2, xr, 0])
			else:
				ls_date.append([dt1, dt2, 0, xd])

	else:
		dt1 = min(range1).strftime('%Y%m%d')
		dt2 = max(range1).strftime('%Y%m%d')
		ls_date.append([dt1, dt2, xr, 0])

		dt1 = min(range2).strftime('%Y%m%d')
		dt2 = max(range2).strftime('%Y%m%d')
		ls_date.append([dt1, dt2, xd, 0])

	return tuple(ls_date)


def Cal_Adj_Price(arg_df):
	global err_flag

	for i in range(0,len(arg_df)):
		comp_id = arg_df['COMP_ID'][i]
		comp_name = arg_df['COMP_NAME'][i]
		xd_date = arg_df['XD_DATE'][i]
		prev_xd_date = arg_df['PREV_XD_DATE'][i]
		cash = arg_df['CASH'][i]
		xr_date = arg_df['XR_DATE'][i]
		prev_xr_date = arg_df['PREV_XR_DATE'][i]
		sre = arg_df['SRE'][i]



		print(comp_id + ", " + comp_name + ", " + xd_date + ", " + prev_xd_date + ", " + xd_adj_start_date + ", " + xd_adj_end_date + " " + str(cash) + "\n")

		#考慮除息後，還原股價
		strsql  = "select QUO_DATE, OPEN, HIGH, LOW, CLOSE "
		strsql += "from STOCK_QUO "
		strsql += "where "
		strsql += "SEAR_COMP_ID ='" + comp_id + ".TW' and "
		strsql += "QUO_DATE between '" + xd_adj_start_date + "' and '" + xd_adj_end_date + "' "
		strsql += "ORDER BY QUO_DATE "

		#print(strsql)
		cursor = conn.execute(strsql)
		result = cursor.fetchall()

		for i in range(0, len(result), 1):
			quo_date = result[i][0]
			o_price = result[i][1]
			h_price = result[i][2]
			l_price = result[i][3]
			c_price = result[i][4]

			#print(str(i) + "  " + quo_date + "\n")
			#if str(quo_date) == "20160910":
			#print("ori  " + quo_date + " " + str(o_price) + " " + str(h_price) + " " + str(l_price) + " " + str(c_price) + "\n")

			adj_o = o_price - cash
			adj_h = h_price - cash
			adj_l = l_price - cash
			adj_c = c_price - cash

			#if str(quo_date) == "20160910":
			#print("adj  " + quo_date + " " + str(adj_o) + " " + str(adj_h) + " " + str(adj_l) + " " + str(adj_c) + "\n")

			# 最後維護日期時間
			str_date = str(datetime.datetime.now())
			date_last_maint = parser.parse(str_date).strftime("%Y%m%d")
			time_last_maint = parser.parse(str_date).strftime("%H%M%S")
			prog_last_maint = "QUO_ADJ"

			strsql  = "update STOCK_QUO set "
			strsql += "ADJ_OPEN = " + str(adj_o) + ", "
			strsql += "ADJ_HIGH = " + str(adj_h) + ", "
			strsql += "ADJ_LOW = " + str(adj_l) + ", "
			strsql += "ADJ_CLOSE =" + str(adj_c) + ", "
			strsql += "DATE_LAST_MAINT='" + date_last_maint + "',"
			strsql += "TIME_LAST_MAINT='" + time_last_maint + "',"
			strsql += "PROG_LAST_MAINT='" + prog_last_maint + "' "
			strsql += "where "
			strsql += "SEAR_COMP_ID = '" + comp_id + ".TW' and "
			strsql += "QUO_DATE='" + quo_date + "' "

			try:
				conn.execute(strsql)
			except sqlite3.Error as er:
				err_flag = True
				print("update STOCK_QUO er=" + er.args[0] + "\n")
				print(comp_id + " " + comp_name + " " + quo_date + "資料更新異常...Rollback!\n")
				file.write("update STOCK_QUO er=" + er.args[0] + "\n")
				file.write(strsql + "\n")
				file.write(comp_id + " " + comp_name + " " + quo_date + "資料更新異常...Rollback!\n")

		#關閉cursor
		cursor.close()

		#考慮除權，還原股價
		strsql  = "select QUO_DATE, OPEN, HIGH, LOW, CLOSE, "
		strsql += "ADJ_OPEN, ADJ_HIGH, ADJ_LOW, ADJ_CLOSE "
		strsql += "from STOCK_QUO "
		strsql += "where "
		strsql += "SEAR_COMP_ID ='" + comp_id + ".TW' and "
		strsql += "QUO_DATE between '" + xr_adj_start_date + "' and '" + xr_adj_end_date + "' "
		strsql += "ORDER BY QUO_DATE "

		#print(strsql)
		cursor = conn.execute(strsql)
		result = cursor.fetchall()

		for i in range(0, len(result), 1):
			quo_date = result[i][0]
			o_price = result[i][1]
			h_price = result[i][2]
			l_price = result[i][3]
			c_price = result[i][4]
			aj_o_price = result[i][5]
			aj_h_price = result[i][6]
			aj_l_price = result[i][7]
			aj_c_price = result[i][8]

			if c_price == 0:
				adj_o = o_price / ()
				adj_h = h_price - cash
				adj_l = l_price - cash
				adj_c = c_price - cash
			else:
				adj_o = aj_o_price - cash
				adj_h = aj_h_price - cash
				adj_l = aj_l_price - cash
				adj_c = aj_c_price - cash

		#for test
		break

	# 最後commit
	if err_flag == False:
		conn.commit()
		print(quo_date + "還原股價，報價資料寫入成功.\n")
		file.write(quo_date + "還原股價，報價資料寫入成功.\n")
	else:
		print(quo_date + "還原股價，報價資料寫入失敗，進行Rollback.\n")
		file.write(quo_date + "還原股價，報價資料寫入失敗，進行Rollback.\n")
		conn.execute("rollback")



####################################################
# main                                             #
####################################################
global err_flag
err_flag = False

dt = str(datetime.datetime.now())
str_date = parser.parse(dt).strftime("%Y%m%d")
now_yyyy = int(parser.parse(dt).strftime("%Y"))

#print(str_date)
#print(now_yyyy)

#建立資料庫連線
conn = sqlite3.connect("market_price.sqlite")

# 寫入LOG File
dt=datetime.datetime.now()
str_date = str(dt)
str_date = parser.parse(str_date).strftime("%Y%m%d")

name = "QUO_ADJ_" + str_date + ".txt"
file = open(name, 'a', encoding = 'UTF-8')

tStart = time.time()#計時開始
file.write("\n\n\n*** LOG datetime  " + str(datetime.datetime.now()) + " ***\n")

#for y in range(2004,now_yyyy,1):
for y in range(2015,2016,1):
	print("結轉還原股價，年度:" + str(y) + "\n")
	file.write("結轉還原股價，盈餘結算年度:" + str(y) + "\n")

	pre_yyyy = str(y - 1)
	strsql  = "select a.COMP_ID, a.COMP_NAME, a.XD_DATE,"
	strsql += "(select XD_DATE from stock_dividend where comp_id = a.comp_id and setm_year < '" + str(y) + "' order by setm_year desc limit 1) as PRE_XD_DATE,"
	strsql += "a.CASH,a.XR_DATE,"
	strsql += "(select XR_DATE from stock_dividend where comp_id = a.comp_id and setm_year < '" + str(y) + "' order by setm_year desc limit 1) as PRE_XR_DATE,"
	strsql += "SRE "
	strsql += "from stock_dividend a "
	strsql += "where a.setm_year='" + str(y) + "' and "
	strsql += "(XD_DATE > '' or XR_DATE > '') "
	#strsql += "and a.COMP_ID='1101' "
	strsql += "order by a.COMP_ID "
	#strsql += "limit 10"

	print(strsql)
	cursor = conn.execute(strsql)
	result = cursor.fetchall()

	df = pd.DataFrame(result, columns=['COMP_ID','COMP_NAME','XD_DATE','PREV_XD_DATE','CASH','XR_DATE','PREV_XR_DATE','SRE'])
	df = df.fillna('')
	#print(df)


	"""
	for i in range(0, len(df)):
		print(df.loc[i]['COMP_ID'])
		xd_date = df.loc[i]['XD_DATE']
		prev_xd_date = df.loc[i]['PREV_XD_DATE']

		xr_date = df.loc[i]['XR_DATE']
		prev_xr_date = df.loc[i]['PREV_XR_DATE']
	"""





	#計算還原股價
	#Cal_Adj_Price(df)

	#關閉cursor
	cursor.close()
	#print(df)

#關閉資料庫連線
conn.close()

tEnd = time.time()#計時結束
file.write ("\n\n\n結轉耗時 %f sec\n" % (tEnd - tStart)) #會自動做進位
file.write("*** End LOG ***\n")

# Close File
file.close()
