# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 15:54:42 2016

@author: bryson0083
"""
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import sqlite3
import re 
import datetime
from dateutil import parser
import sys
from random import randint

def proc_db(df, yyyy, qq):
    #print("this is def proc_db df ==>")
    #print(df)
    
    for i in range(0,len(df)):
        #print(str(df.index[i]))
        comp_id = str(df.iloc[i][0])
        comp_name = str(df.iloc[i][1])
        eps = str(df.iloc[i][2])
        eps = re.sub("[^-0-9^.]", "", eps) # 數字做格式控制
        
        print(comp_id + "  " + comp_name + "   " + eps + "\n")
        # 最後維護日期時間
        str_date = str(datetime.datetime.now())
        date_last_maint = parser.parse(str_date).strftime("%Y%m%d")
        time_last_maint = parser.parse(str_date).strftime("%H%M%S")
        prog_last_maint = "MOPS_YQ_2"

        sqlstr = "select count(*) from MOPS_YQ "
        sqlstr = sqlstr + "where "
        sqlstr = sqlstr + "COMP_ID='" + comp_id + "' and "
        sqlstr = sqlstr + "YYYY='" + yyyy + "' and "
        sqlstr = sqlstr + "QQ='" + qq + "' "

        #print(sqlstr)
        cursor = conn.execute(sqlstr)
        result = cursor.fetchone()

        if result[0] == 0:
            sqlstr  = "insert into MOPS_YQ values ("
            sqlstr += "'" + comp_id + "',"
            sqlstr += "'" + comp_name + "',"
            sqlstr += "'" + yyyy + "',"
            sqlstr += "'" + qq + "',"
            sqlstr += " " + eps + ","
            sqlstr += "0,"
            sqlstr += "'" + date_last_maint + "',"
            sqlstr += "'" + time_last_maint + "',"
            sqlstr += "'" + prog_last_maint + "' "
            sqlstr += ") "
        else:
            sqlstr  = "update MOPS_YQ set "
            sqlstr += "eps=" + eps + ","
            sqlstr += "date_last_maint='" + date_last_maint + "',"
            sqlstr += "time_last_maint='" + time_last_maint + "',"
            sqlstr += "prog_last_maint='" + prog_last_maint + "' "
            sqlstr += "where "
            sqlstr += "COMP_ID='" + comp_id + "' and "
            sqlstr += "YYYY='" + yyyy + "' and "
            sqlstr += "QQ='" + qq + "' "

        try:
            cursor = conn.execute(sqlstr)
            conn.commit()
        except sqlite3.Error as er:
            file.write("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
            file.write("\n資料 " + comp_id + "," + comp_name + "," + yyyy + qq + "," + eps + "\n")
            file.write("資料庫錯誤:\n" + er.args[0] + "\n")
            file.write("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
            print ("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
            print ("\n資料 " + comp_id + "," + comp_name + "," + yyyy + qq + "," + eps + "\n")
            print ("資料庫錯誤:\n" + er.args[0] + "\n")
            print ("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")

        # 關閉DB cursor
        cursor.close()


        
########################################################
#  program Main                                        #
########################################################
# 寫入LOG File
dt=datetime.datetime.now()

print("##############################################")
print("##      公開觀測資訊站~資產負債表資料讀取   ##")
print("##                                          ##")
print("##                                          ##")
print("##   datetime: " + str(dt) +            "   ##")
print("##############################################")

str_date = str(dt)
str_date = parser.parse(str_date).strftime("%Y%m%d")

name = "MOPS_YQ_2_LOG_" + str_date + ".txt"
file = open(name, 'a', encoding = 'UTF-8')

tStart = time.time()#計時開始
file.write("\n\n\n*** LOG datetime  " + str(datetime.datetime.now()) + " ***\n")

# 建立資料庫連線
conn = sqlite3.connect('market_price.sqlite')

headers = {'User-Agent':'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
session = requests.session()

# 讀取查詢頁面
r = session.get("http://mops.twse.com.tw/mops/web/t163sb05", headers=headers)

# 隨機等待3~9秒的時間
random_sec = randint(3,9)

print("Going to wait!!")
print("Waiting sec=" + str(random_sec))
time.sleep(random_sec)

URL = 'http://mops.twse.com.tw/mops/web/ajax_t163sb05'

payload = {
"encodeURIComponent": "1",
"step": "1",
"firstin": "1",
"off": "1",
"TYPEK": "sii",
"year": '105',
"season": '01'
}

r = requests.post(URL, data=payload, headers=headers)
r.encoding = "utf-8"

sp = BeautifulSoup(r.text, 'html.parser')
#print(sp)

tr_hd = sp.findAll('tr', attrs={'class':'tblHead'})
tr_odd = sp.findAll('tr', attrs={'class':'odd'})  # tag-attrs
tr_even = sp.findAll('tr', attrs={'class':'even'}) 

tr_odd_cnt = len(tr_odd)
print("tr_odd_cnt=" + str(tr_odd_cnt) + "\n\n")

#print(tr[1])
#print(str(tr_odd[0]))
#sys.exit("test end...\n")

###############################################################
# tr_odd處理                                                  #
###############################################################
# 處理 2855 統一證券 ~ 6005 群益證
i=0
ls=[]
while i <= 2:
    head = [th.text for th in tr_hd[1].select('th')]
    #print(head)
    data = [td.text for td in tr_odd[i].select('td')]
    #print(data)
    ls.append(data)

    tr_odd_cnt -= 1
    i += 1

#print(ls)
df = pd.DataFrame(ls, columns = head)
#print(df)
df2 = df.loc[:,['公司代號', '公司名稱', '每股參考淨值']]
#print(df2)

# 處理 2880 華南金 ~ 5880 合庫金
i=3
ls=[]
while i <= 16:
    head = [th.text for th in tr_hd[3].select('th')]
    #print(head)
    data = [td.text for td in tr_odd[i].select('td')]
    #print(data)
    ls.append(data)
    
    tr_odd_cnt -= 1
    i += 1

#print(ls)
df = pd.DataFrame(ls, columns = head)
#print(df)
df2 = df.loc[:,['公司代號', '公司名稱', '每股參考淨值']]
#print(df2)

# 處理 1409 新纖 ~ 2905 三商
i=17
ls=[]
while i <= 20:
    head = [th.text for th in tr_hd[5].select('th')]
    #print(head)
    data = [td.text for td in tr_odd[i].select('td')]
    #print(data)
    ls.append(data)
    
    tr_odd_cnt -= 1
    i += 1

#print(ls)
df = pd.DataFrame(ls, columns = head)
#print(df)
df2 = df.loc[:,['公司代號', '公司名稱', '每股參考淨值']]
#print(df2)

print("final tr_odd_cnt=" + str(tr_odd_cnt) + "\n\n")

tEnd = time.time()#計時結束
file.write ("\n\n\n結轉耗時 %f sec\n" % (tEnd - tStart)) #會自動做進位
file.write("*** End LOG ***\n")

# 資料庫連線關閉
conn.close()

# Close File
file.close()
