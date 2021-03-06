# 上櫃公司清單讀取(STOCK_COMP_LIST_SQ)
# Target: http://www.tpex.org.tw/web/regular_emerging/corporateInfo/regular/regular_stock.php?l=zh-tw

import requests as rs
from bs4 import BeautifulSoup
import pandas as pd
from dateutil import parser
import datetime
import os.path
import sqlite3
import time
import sys

############################################################################
# Main                                                                     #
############################################################################
print("Executing STOCK_COMP_LIST_SQ...")

err_yn = "N"

# 寫入LOG File
dt=datetime.datetime.now()
print("##############################################")
print("##      台灣櫃買中心 ~ 上櫃公司清單讀取     ##")
print("##                                          ##")
print("##                                          ##")
print("##   datetime: " + str(dt) +            "   ##")
print("##############################################")
str_date = str(dt)
str_date = parser.parse(str_date).strftime("%Y%m%d")

file_name = "STOCK_COMP_LIST_SQ_" + str_date + ".txt"
file = open(file_name, 'a', encoding = 'UTF-8')

tStart = time.time()#計時開始
file.write("\n\n\n*** LOG datetime  " + str(datetime.datetime.now()) + " ***\n")

##############
# 讀取本國企業
##############
# 設定瀏覽器header
headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
} 

# 目標網址
URL = 'http://www.tpex.org.tw/web/regular_emerging/corporateInfo/regular/regular_stock.php?l=zh-tw'

payload = {
    "choice_type": "stk_type"
}
res = rs.post(URL, data=payload, headers=headers)

res.encoding = 'utf-8'
#print(res.text)

sp = BeautifulSoup(res.text, 'html.parser')
#print(sp)

try:
    table = sp.find('table', attrs={'id':'company_list'})  # tag-attrs
    #print(table)
except:
    err_yn = "Y"
    file.write("Err. 上櫃本國，網頁讀取異常或該網頁無資料.\n")
    file.close()
    sys.exit("Err. 上櫃本國，網頁讀取異常或該網頁無資料.")
    
data = [[td.text for td in row.select('td')]  # http://stackoverflow.com/questions/14487526/turning-beautifulsoup-output-into-matrix
         for row in table.select('tr')]

#跳過第一筆空list
data = data[1:]

#list拋到dataframe
df = pd.DataFrame(data, columns = ['股票代號','公司名稱','最新一季每股淨值(元)','產業類別'])


##############
# 讀取外國企業
##############
# 設定瀏覽器header
headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
} 

# 目標網址
URL = 'http://www.tpex.org.tw/web/regular_emerging/corporateInfo/regular/regular_stock.php?l=zh-tw'

payload = {
    "choice_type": "stk_type",
    "stk_type": "RR"
}
res = rs.post(URL, data=payload, headers=headers)

res.encoding = 'utf-8' # 'utf-8'  #  http://sh3ll.me/2014/06/18/python-requests-encoding/
#print(res.text)

sp = BeautifulSoup(res.text, 'html.parser')
#print(sp)

try:
    table = sp.find('table', attrs={'id':'company_list'})  # tag-attrs
    #print(table)
except:
    err_yn = "Y"
    file.write("Err. 上櫃外國，網頁讀取異常或該網頁無資料.\n")
    file.close()
    sys.exit("Err. 上櫃外國，網頁讀取異常或該網頁無資料.")
    
data = [[td.text for td in row.select('td')]  # http://stackoverflow.com/questions/14487526/turning-beautifulsoup-output-into-matrix
         for row in table.select('tr')]

#跳過第一筆空list
data = data[1:]
df2 = pd.DataFrame(data, columns = ['股票代號','公司名稱','最新一季每股淨值(元)','產業類別'])

#合併本國與外國公司清單
df = df.append(df2, ignore_index=True)
#print(df)

#建立資料庫連線
conn = sqlite3.connect('market_price.sqlite')

#刪除現有上櫃公司資料
strsql = "delete from STOCK_COMP_LIST where STOCK_TYPE = '上櫃'"
conn.execute(strsql)

new_cnt = 0
for i in range(1,len(df)):
    #print(str(df.index[i]))

    comp_id = str(df.iloc[i][0])	# 公司代號
    comp_name = str(df.iloc[i][1])	# 公司名稱
    industry = str(df.iloc[i][3])	# 產業類別
    #print(comp_id+" "+comp_name+" "+industry+"\n")
    
    # 最後維護日期時間
    str_date = str(datetime.datetime.now())
    date_last_maint = parser.parse(str_date).strftime("%Y%m%d")
    time_last_maint = parser.parse(str_date).strftime("%H%M%S")
    prog_last_maint = "STOCK_COMP_LIST_SQ"

    sqlstr  = "insert into STOCK_COMP_LIST ("
    sqlstr += "COMP_ID,SEAR_COMP_ID,COMP_NAME,"
    sqlstr += "INDUSTRY,STOCK_TYPE,"
    sqlstr += "DATE_LAST_MAINT,TIME_LAST_MAINT,"
    sqlstr += "PROG_LAST_MAINT"
    sqlstr += ") values ("
    sqlstr += "'" + comp_id + "',"
    sqlstr += "'" + comp_id + ".TW',"
    sqlstr += "'" + comp_name + "',"
    sqlstr += "'" + industry + "',"
    sqlstr += "'上櫃',"
    sqlstr += "'" + date_last_maint + "',"
    sqlstr += "'" + time_last_maint + "',"
    sqlstr += "'" + prog_last_maint + "'"
    sqlstr += ")"

    try:
        file.write("新增上櫃股票:"+comp_id+" "+comp_name+" "+ industry+"\n")
        cursor = conn.execute(sqlstr)
        conn.commit()
        new_cnt += 1
    except sqlite3.Error as er:
        err_yn = "Y"
        file.write("insert 資料庫錯誤:\n" + er.args[0] + "\n")
        print("er:" + er.args[0])
        file.write(sqlstr + "\n")

print("本次新增筆數:" + str(new_cnt) + "筆.\n")

# 關閉資料庫連線
conn.close()    

tEnd = time.time()#計時結束
file.write ("\n\n\n結轉耗時 %f sec\n" % (tEnd - tStart)) #會自動做進位
file.write("*** End LOG ***\n")

# Close File
file.close()

# 如果執行過程無錯誤，最後刪除log file
if err_yn == "N":
    os.remove(file_name)

print ("End of prog...")