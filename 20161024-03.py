import sqlite3
import datetime
import re 
import os.path
from dateutil import parser
from dateutil.parser import parse

sear_yyy = "105"
yyyy = int(sear_yyy) + 1911
print("yyyy=" + str(yyyy))

sear_qq = "04"
sear_qq2= int(sear_qq)
print("sear_qq2=" + str(sear_qq2))


conn = sqlite3.connect('market_price.sqlite')
sqlstr = "select count(*) from MOPS_YQ where COMP_ID='2801' and YYYY='2015' and QQ='02'"

try:
	cursor = conn.execute(sqlstr)
	result = cursor.fetchone()
	print("result=" + str(result[0]))
except sqlite3.Error as er:
	print ('er:', er.args[0])







run_mode = "C"
dt=datetime.datetime.now()
yyyy = str(dt.year)
print("@@ yyyy=" + yyyy)




str_float = "aaa+5,766.32ms"
non_decimal = re.compile(r'[^-\d.]+')
str_float = non_decimal.sub('', str_float)
print("111var float=" + str(float(str_float)))


str_float = "aaa-aaaa5,766.32ms"
str_float = re.sub("[^-0-9^.]", "", str_float)
print("222var float=" + str(float(str_float)))




name = "GG_LOG.txt"
file = open(name, 'a', encoding = 'UTF-8')

comp_id = "6525"
comp_name = "捷敏-KY"
bvps = "5,766.32"
str_date = str(datetime.datetime.now())
yyyy = "2014"
qq = "04"
date_last_maint = parser.parse(str_date).strftime("%Y%m%d")
time_last_maint = parser.parse(str_date).strftime("%H%M%S")
prog_last_maint = "test_prog"


sqlstr = "select count(*) from MOPS_YQ "
sqlstr = sqlstr + "where "
sqlstr = sqlstr + "COMP_ID='" + comp_id + "' and "
sqlstr = sqlstr + "YYYY='2014' and "
sqlstr = sqlstr + "QQ='04' "

#print(sqlstr)
cursor = conn.execute(sqlstr)
result = cursor.fetchone()

if result[0] == 0:
	sqlstr = "insert into MOPS_YQ values ("
	sqlstr = sqlstr + "'" + comp_id + "',"
	sqlstr = sqlstr + "'" + comp_name + "',"
	sqlstr = sqlstr + "'2014',"
	sqlstr = sqlstr + "'04',"
	sqlstr = sqlstr + "0,"
	sqlstr = sqlstr + " " + bvps + ","
	sqlstr = sqlstr + "'" + date_last_maint + "',"
	sqlstr = sqlstr + "'" + time_last_maint + "',"
	sqlstr = sqlstr + "'" + prog_last_maint + "' "
	sqlstr = sqlstr + ") "

else:
	sqlstr = "update MOPS_YQ set "
	sqlstr = sqlstr + "bvps=" + bvps + ","
	sqlstr = sqlstr + "date_last_maint='" + date_last_maint + "',"
	sqlstr = sqlstr + "time_last_maint='" + time_last_maint + "',"
	sqlstr = sqlstr + "prog_last_maint='" + prog_last_maint + "' "
	sqlstr = sqlstr + "where "
	sqlstr = sqlstr + "COMP_ID='" + comp_id + "' and "
	sqlstr = sqlstr + "YYYY='2014' and "
	sqlstr = sqlstr + "QQ='04' "

try:
	cursor = conn.execute(sqlstr)
	conn.commit()
except sqlite3.Error as er:
	file.write("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
	file.write("\n資料 " + comp_id + "," + comp_name + "," + yyyy + qq + "," + bvps + "\n")
	file.write("資料庫錯誤:\n" + er.args[0] + "\n")
	file.write("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
	print ("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
	print ("\n資料 " + comp_id + "," + comp_name + "," + yyyy + qq + "," + bvps + "\n")
	print ("資料庫錯誤:\n" + er.args[0] + "\n")
	print ("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")

	# 關閉DB cursor
	cursor.close()

conn.close

# Close File
file.close()


