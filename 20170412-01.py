"""
先將目標網頁另存檔案，再用程式讀取表格內容，直到正確
之後可以改成直接抓來源網頁，避免測試開發期間太多次讀取來源網頁
被視為攻擊行為
"""
import codecs
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import datetime
from dateutil import parser

f=codecs.open("C:/Users/bryson0083/Desktop/stock105.html", 'r')
#print(f.read())

data = f.read()
#data.encoding = "utf-8"
sp = BeautifulSoup(data, 'html.parser')
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

yyyy = "2015"

#建立資料庫連線
conn = sqlite3.connect("market_price.sqlite")

#有錯誤出現時，設定err_flag=True作為識別
global err_flag
err_flag = False

for i in range(0, len(all_df)):
	data_source = str(all_df.loc[i]['資料來源'])
	tmp_str = str(all_df.loc[i]['公司代號名稱'])
	tmp_ls = tmp_str.split(" - ")
	comp_id = tmp_ls[0]
	comp_name = tmp_ls[1]
	shd_date = str(all_df.loc[i]['股東會日期'])

	if len(shd_date) > 2:
		tmp_date = shd_date.split("/")
		tmp_year = int(tmp_date[0]) + 1911
		shd_date = str(tmp_year) + tmp_date[1] + tmp_date[2]

	cash = all_df.loc[i]['盈餘分配之現金股利(元/股)']	#現金股利
	sre = all_df.loc[i]['盈餘轉增資配股(元/股)']		#股票股利

	# 最後維護日期時間
	str_date = str(datetime.datetime.now())
	date_last_maint = parser.parse(str_date).strftime("%Y%m%d")
	time_last_maint = parser.parse(str_date).strftime("%H%M%S")
	prog_last_maint = "STOCK_DIVIDEND"

	if data_source == "股東會確認":
		print(comp_id + " " + comp_name + " " + shd_date + " " + cash + " " + sre)

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
			#file.write(sqlstr + "\n")
			#file.write("DB Err:\n" + er.args[0] + "\n")
			print (sqlstr + "\n")
			print ("DB Err:\n" + er.args[0] + "\n")		

		# 關閉DB cursor
		cursor.close()

#過程中有任何錯誤，進行rollback
if err_flag == False:
	conn.commit()
else:
	conn.execute("rollback")

#關閉資料庫連線
conn.close()