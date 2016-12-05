# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 13:26:03 2016

@author: yu63158
@target_rul: http://mops.twse.com.tw/mops/web/t163sb04
"""
import requests
from bs4 import BeautifulSoup
import time
import sys
import pandas as pd
import re 
import datetime
from dateutil import parser
from dateutil.parser import parse
import sqlite3

def proc_db(df):
    print("this is def proc_db df ==>")
    #print(df)
    yyyy = "2016"
    qq = "01"
    
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
        prog_last_maint = "MOPS_YQ_1"

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
        
        
def MOPS_YQ_1():
    headers = {'User-Agent':'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'}
    session = requests.session()

    # 讀取查詢頁面
    r = session.get("http://mops.twse.com.tw/mops/web/t163sb04", headers=headers)

    print("Going to wait!!")
    time.sleep(5)

    # 拋送查詢條件到頁面，並取回查詢結果內容
    URL = 'http://mops.twse.com.tw/mops/web/ajax_t163sb04'
    payload = {
           "encodeURIComponent": "1",
           "step": "1",
           "firstin": "1",
           "off": "1",
           "TYPEK": "sii",
           "year": "105",
           "season": "01"
           }

    r = requests.post(URL, data=payload, headers=headers)
    r.encoding = "utf-8"
    sp = BeautifulSoup(r.text, 'html.parser')
    #print(sp)

    try:
        table = sp.findAll('table', attrs={'class':'hasBorder'})  # tag-attrs
        #print(table)
        #print(type(table))
        #print(type(table[0]))
        #print(str(len(table)))
        #print(str(len(table[5].find_all('tr'))))
    except:
        sys.exit("@@@ 網頁讀取異常或該網頁無資料. @@@")
        
    tb_cnt = len(table)
    i = 0
    while i <= 1:
    #while i <= tb_cnt:
        # 讀取表格抬頭
        head = [[th.text for th in row.select('th')]
                for row in table[i].select('tr')]
        #print(head)
    
        # 讀取表格資料
        data = [[td.text for td in row.select('td')]  # http://stackoverflow.com/questions/14487526/turning-beautifulsoup-output-into-matrix
                for row in table[i].select('tr')]
        #print(data)   # list
    
        df = pd.DataFrame(data=data[1:len(data)], columns = head[0])
        #print(df)
        #print(df.loc[:,['公司代號', '公司名稱', '基本每股盈餘（元）']])
    
        df2 = df.loc[:,['公司代號', '公司名稱', '基本每股盈餘（元）']]
        #print("this is df2 ==>")
        #print(df2)
    
        proc_db(df2)
        i += 1    

        
        
        
        

# 寫入LOG File
dt=datetime.datetime.now()

print("##############################################")
print("##      公開觀測資訊站~綜合損益表資料讀取     ##")
print("##                                          ##")
print("##                                          ##")
print("##   datetime: " + str(dt) +            "   ##")
print("##############################################")

str_date = str(dt)
str_date = parser.parse(str_date).strftime("%Y%m%d")

name = "MOPS_YQ_1_LOG_" + str_date + ".txt"
file = open(name, 'a', encoding = 'UTF-8')

tStart = time.time()#計時開始
file.write("\n\n\n*** LOG datetime  " + str(datetime.datetime.now()) + " ***\n")


# 建立資料庫連線
conn = sqlite3.connect('market_price.sqlite')
    
# 讀取網頁資料
MOPS_YQ_1()

tEnd = time.time()#計時結束
file.write ("\n\n\n結轉耗時 %f sec\n" % (tEnd - tStart)) #會自動做進位
file.write("*** End LOG ***\n")

# 資料庫連線關閉
conn.close()

# Close File
file.close()