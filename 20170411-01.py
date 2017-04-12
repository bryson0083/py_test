"""
先將目標網頁另存檔案，再用程式讀取表格內容，直到正確
之後可以改成直接抓來源網頁，避免測試開發期間太多次讀取來源網頁
被視為攻擊行為
"""
import codecs
from bs4 import BeautifulSoup
import pandas as pd

f=codecs.open("C:/Users/bryson0083/Desktop/stock105.html", 'r')
#print(f.read())

data = f.read()
#data.encoding = "utf-8"
sp = BeautifulSoup(data, 'html.parser')
#print(sp)

table = sp.findAll('table', attrs={'class':'hasBorder'})
tb_cnt = len(table) # 網頁上的表格總數

#print(table[0])
i=0
#while i < tb_cnt:
while i < 2:
	ign = str(table[i]).find("面額新台幣10元之公司")

	if ign == -1:
		# 讀取表格資料
		rdata = [[td.text for td in row.select('td')]
				for row in table[i].select('tr')]
		rdata = [x for x in rdata if x != []]
		#print(rdata)
	
	i += 1		

head = ['公司代號名稱','資料來源','期別','董事會決議通過股利分派日', \
		'股東會日期','期初未分配盈餘/待彌補虧損(元)','本期淨利(淨損)(元)', \
		'可分配盈餘(元)','分配後期末未分配盈餘(元)','盈餘分配之現金股利(元/股)', \
		'法定盈餘公積、資本公積發放之現金(元/股)','股東配發之現金(股利)總金額(元)',\
		'盈餘轉增資配股(元/股)','法定盈餘公積、資本公積轉增資配股(元/股)', \
		'股東配股總股數(股)','摘錄公司章程-股利分派部分','備註','普通股每股面額']

df = pd.DataFrame(rdata, columns = head)
#print(df)

df = df.loc[:,['公司代號名稱', '資料來源', '股東會日期','盈餘分配之現金股利(元/股)','盈餘轉增資配股(元/股)']]
print(df)