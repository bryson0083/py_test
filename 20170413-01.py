import time
import pandas as pd
import sqlite3
import datetime
import sys
import os
import requests
from bs4 import BeautifulSoup
from dateutil import parser
from random import randint

# 自動結轉資料
def mode_c():
	#有錯誤出現時，設定err_flag=True作為識別
	global err_flag

	#str_date = "2016-04-05"
	str_date = str(datetime.datetime.now())

	# 轉換日期為C8格式字串
	dt_c8 = parser.parse(str_date).strftime("%Y%m%d")
	yyyy = dt_c8[0:4]
	#print(yyyy)

	# 轉西元年為民國年
	yyy = str(int(yyyy) - 1911)
	#print(yyy)

	# 取出月日的部分
	mmdd = dt_c8[4:]
	#print(mmdd)

	#mmdd = "1206"
	# 只在以下特定幾天結轉季報資料
	if mmdd >= "0501" and mmdd <= "0731":
		#yyy = str(int(yyy) - 1)
		file.write("mode_c: 自動抓取當年度股東會資料 yyy=" + yyy + "\n")
		print("mode_c: 自動抓取當年度股東會資料 yyy=" + yyy)

		# 開始抓取資料(上市)
		print("結轉上市公司除權息資料...")
		GET_STOCK_DIVIDEND(yyy, 'sii')

		# 隨機等待60~120秒的時間
		random_sec = randint(60,120)
		print("隨機等待秒數=" + str(random_sec) + "...")
		time.sleep(random_sec)

		# 開始抓取資料(上櫃)
		print("結轉上櫃公司除權息資料...")
		GET_STOCK_DIVIDEND(yyy, 'otc')

	else:
		file.write("mode_c: 未到批次結轉時間，執行結束...\n")
		print("mode_c: date=" + mmdd + " 未到批次結轉時間，執行結束...")
		err_flag = False


# 手動輸入條件結轉資料
def mode_h():
	yyyy = str(input("輸入抓取資料年分(YYYY):"))

	# 轉西元年為民國年
	yyy = str(int(yyyy) - 1911)

	# 寫入LOG File
	file.write("mode_h: 手動結轉年度 yyy=" + yyy + "\n")
	print("mode_h: 手動結轉年度 yyy=" + yyy)

	# 開始抓取資料(上市)
	print("結轉上市公司除權息資料...")
	GET_STOCK_DIVIDEND(yyy, 'sii')

	# 隨機等待60~120秒的時間
	random_sec = randint(60,120)
	print("隨機等待秒數=" + str(random_sec) + "...")
	time.sleep(random_sec)

	# 開始抓取資料(上櫃)
	print("結轉上櫃公司除權息資料...")
	GET_STOCK_DIVIDEND(yyy, 'otc')


# 跑特定區間，結轉資料(自行修改參數條件)
def mode_a():
	for y in range(2016,2017,1):
		#print("y=" + str(y))
		yyy = str(y - 1911)
		file.write("mode_a: 特定區間，結轉yyyqq=" + yyy + qq + "\n")
		print("mode_a: 特定區間，結轉yyyqq=" + yyy + qq)

		# 開始抓取資料(上市)
		print("結轉上市公司除權息資料...")
		GET_STOCK_DIVIDEND(yyy, 'sii')

		# 隨機等待60~120秒的時間
		random_sec = randint(60,120)
		print("隨機等待秒數=" + str(random_sec) + "...")
		time.sleep(random_sec)

		# 開始抓取資料(上櫃)
		print("結轉上櫃公司除權息資料...")
		GET_STOCK_DIVIDEND(yyy, 'otc')

		# 隨機等待60~120秒的時間
		random_sec = randint(60,120)
		print("隨機等待秒數=" + str(random_sec) + "...")
		time.sleep(random_sec)

		q += 1

def GET_STOCK_DIVIDEND(arg_yyy, arg_typek):
	headers = {'User-Agent':'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
	session = requests.session()

	# 拋送查詢條件到頁面，並取回查詢結果內容
	URL = 'http://mops.twse.com.tw/server-java/t05st09sub'
	payload = {
	           "step": "1",
	           "TYPEK": arg_typek,
	           "YEAR": arg_yyy,
	           "first": ""
	           }

	r = requests.post(URL, data=payload, headers=headers)

	r.encoding = "big5"
	sp = BeautifulSoup(r.text, 'html.parser')
	#print(sp)

	table = sp.findAll('table', attrs={'class':'hasBorder'})
	tb_cnt = len(table) # 網頁上的表格總數
	#print(tb_cnt)

	i=0
	all_df = pd.DataFrame()
	while i <= tb_cnt-1:
		ign = str(table[i]).find("面額新台幣10元之公司")

		if ign == -1:
			head = ['公司代號名稱','資料來源','期別','董事會決議通過股利分派日', \
					'股東會日期','期初未分配盈餘/待彌補虧損(元)','本期淨利(淨損)(元)', \
					'可分配盈餘(元)','分配後期末未分配盈餘(元)','盈餘分配之現金股利(元/股)', \
					'法定盈餘公積、資本公積發放之現金(元/股)','股東配發之現金(股利)總金額(元)',\
					'盈餘轉增資配股(元/股)','法定盈餘公積、資本公積轉增資配股(元/股)', \
					'股東配股總股數(股)','摘錄公司章程-股利分派部分','備註','普通股每股面額']

			# 讀取表格資料
			rdata = [[td.text for td in row.select('td')]
					for row in table[i].select('tr')]
			rdata = [x for x in rdata if x != []]
			df = pd.DataFrame(data=rdata, columns = head)
			all_df = pd.concat([all_df,df],ignore_index=True)

		i += 1		

	all_df = all_df.loc[:,['公司代號名稱', '資料來源', '股東會日期','盈餘分配之現金股利(元/股)','盈餘轉增資配股(元/股)']]
	#print(all_df)
	yyyy = str(int(arg_yyy) + 1911 - 1)

	#資料庫處裡
	proc_db(all_df, yyyy)

def proc_db(df, yyyy):
	#print(df)

	#有錯誤出現時，設定err_flag=True作為識別
	global err_flag

	for i in range(0,len(df)):
		data_source = str(df.loc[i]['資料來源'])
		tmp_str = str(df.loc[i]['公司代號名稱'])
		tmp_ls = tmp_str.split(" - ")
		comp_id = tmp_ls[0]
		comp_name = tmp_ls[1]
		shd_date = str(df.loc[i]['股東會日期'])

		if len(shd_date) > 2:
			tmp_date = shd_date.split("/")
			tmp_year = int(tmp_date[0]) + 1911
			shd_date = str(tmp_year) + tmp_date[1] + tmp_date[2]

		cash = df.loc[i]['盈餘分配之現金股利(元/股)']	#現金股利
		sre = df.loc[i]['盈餘轉增資配股(元/股)']		#股票股利

		# 最後維護日期時間
		str_date = str(datetime.datetime.now())
		date_last_maint = parser.parse(str_date).strftime("%Y%m%d")
		time_last_maint = parser.parse(str_date).strftime("%H%M%S")
		prog_last_maint = "STOCK_DIVIDEND"

		if data_source == "股東會確認":
			#print(comp_id + " " + comp_name + " " + shd_date + " " + cash + " " + sre)

			#資料庫處理
			sqlstr  = "select count(*) from STOCK_DIVIDEND "
			sqlstr += "where "
			sqlstr += "COMP_ID='" + comp_id + "' and "
			sqlstr += "SETM_YEAR='" + yyyy + "' "

			cursor = conn.execute(sqlstr)
			result = cursor.fetchone()

			if result[0] == 0:
				sqlstr  = "insert into STOCK_DIVIDEND "
				sqlstr += "(COMP_ID,COMP_NAME,SETM_YEAR,"
				sqlstr += "SHD_DATE,CASH,SRE,"
				sqlstr += "DATE_LAST_MAINT,TIME_LAST_MAINT,PROG_LAST_MAINT"
				sqlstr += ") values ("
				sqlstr += "'" + comp_id + "',"
				sqlstr += "'" + comp_name + "',"
				sqlstr += "'" + yyyy + "',"
				sqlstr += "'" + shd_date + "',"
				sqlstr += " " + cash + ","
				sqlstr += " " + sre + ","
				sqlstr += "'" + date_last_maint + "',"
				sqlstr += "'" + time_last_maint + "',"
				sqlstr += "'" + prog_last_maint + "' "
				sqlstr += ") "
			else:
				sqlstr  = "update STOCK_DIVIDEND set "
				sqlstr += "SHD_DATE=" + shd_date + ","
				sqlstr += "CASH=" + cash + ","
				sqlstr += "SRE=" + sre + ","
				sqlstr += "date_last_maint='" + date_last_maint + "',"
				sqlstr += "time_last_maint='" + time_last_maint + "',"
				sqlstr += "prog_last_maint='" + prog_last_maint + "' "
				sqlstr += "where "
				sqlstr += "COMP_ID='" + comp_id + "' and "
				sqlstr += "SETM_YEAR='" + yyyy + "' "

			try:
				cursor = conn.execute(sqlstr)
			except sqlite3.Error as er:
				err_flag = True
				file.write(sqlstr + "\n")
				file.write("DB Err:\n" + er.args[0] + "\n")
				print (sqlstr + "\n")
				print ("DB Err:\n" + er.args[0] + "\n")		

			# 關閉DB cursor
			cursor.close()

	#過程中有任何錯誤，進行rollback
	if err_flag == False:
		conn.commit()
	else:
		conn.execute("rollback")


#############################################################################
# Main																		#
#############################################################################
print("Executing STOCK_DIVIDEND...")

# 寫入LOG File
dt = datetime.datetime.now()

print("##############################################")
print("##             公開觀測資訊站               ##")
print("##        股利分派情形彙總表資料讀取        ##")
print("##                                          ##")
print("##   datetime: " + str(dt) +            "   ##")
print("##############################################")

str_date = str(dt)
str_date = parser.parse(str_date).strftime("%Y%m%d")

name = "STOCK_DIVIDEND_LOG_" + str_date + ".txt"
file = open(name, 'a', encoding = 'UTF-8')

global err_flag
err_flag = False

tStart = time.time()#計時開始
file.write("\n\n\n*** LOG datetime  " + str(datetime.datetime.now()) + " ***\n")

# 建立資料庫連線
conn = sqlite3.connect('market_price.sqlite')

try:
	run_mode = sys.argv[1]
	run_mode = run_mode.upper()
except Exception as e:
	run_mode = "C"

print("you choose mode " + run_mode)

if run_mode == "C":
	file.write("mode_c: 自動抓取當季，結轉資料...\n")
	mode_c()
elif run_mode == "H":
	file.write("mode_h: 手動輸入區間，結轉資料...\n")
	mode_h()
elif run_mode == "A":
	print("mode_a 跑特定區間，結轉資料...\n")
	file.write("mode_a: 跑特定區間，結轉資料...\n")
	mode_a()
else:
	file.write("Err: 模式錯誤，結束程式...\n")
	sys.exit("Err: 模式錯誤，結束程式...\n")

tEnd = time.time()#計時結束
file.write ("\n\n\n結轉耗時 %f sec\n" % (tEnd - tStart)) #會自動做進位
file.write("*** End LOG ***\n")

# 資料庫連線關閉
conn.close()

# Close File
file.close()

print("err_flag=" + str(err_flag))
#若執行過程無錯誤，執行結束後刪除log檔案
if err_flag == False:
    os.remove(name)

print ("End of prog...")
