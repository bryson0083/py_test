# 上市公司清單讀取(STOCK_COMP_LIST)
#   Target: http://isin.twse.com.tw/isin/C_public.jsp?strMode=2
#   Version: 0.1
#   Date: 2016-11-15
#   Author: Bryson Xue
#   To-Do List: 

import requests as rs
from bs4 import BeautifulSoup
import pandas as pd
from dateutil import parser
import datetime
import time
import sys

# 寫入LOG File
dt=datetime.datetime.now()

str_date = str(dt)
str_date = parser.parse(str_date).strftime("%Y%m%d")

# 設定瀏覽器header
headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
} 

# 目標網址
url = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=2'

res = rs.get(url, headers = headers)
res.encoding = 'big5' # 'utf-8'  #  http://sh3ll.me/2014/06/18/python-requests-encoding/
#print(res.text)

sp = BeautifulSoup(res.text, 'html.parser')
#print(sp)

tStart = time.time()#計時開始
file.write("\n\n\n*** LOG datetime  " + str(datetime.datetime.now()) + " ***\n")

try:
    table = sp.find('table', attrs={'class':'h4'})  # tag-attrs
    #print(table)
except:
    file.write("@@@ 網頁讀取異常或該網頁無資料. @@@\n")
    file.close()
    sys.exit("@@@ 網頁讀取異常或該網頁無資料. @@@")
    
data = [[td.text for td in row.select('td')]  # http://stackoverflow.com/questions/14487526/turning-beautifulsoup-output-into-matrix
         for row in table.select('tr')]
print(data)   # list

#df = pd.DataFrame(data=data[1:len(data)], columns = data[0])
#print(df)

print ("end of prog...")