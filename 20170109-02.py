# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 09:11:25 2017

@author: bryson0083
"""
import csv
import pandas as pd

with open('1050511.csv', 'r') as f:
	reader = csv.reader(f)
	quo_list = list(reader)

#print(quo_list)

#取得要讀取的資料起點位置
st_idx = 0
i = 0
for item in quo_list:
	#print("i=" + str(i) + "\n")
	for j in item:
		if j == "證券代號":
			st_idx = i
			#print("start from " + str(i) + "\n")
	i += 1

# 讀取當天個股收盤資料到list中
i = 0
idx = st_idx
all_data = []
while True:
	#for item in quo_list[idx]:
	#	print(item)
	
	# 判斷若list長度不滿16，跳出迴圈
	if len(quo_list[idx]) != 16:
		break
		
	data = [str(item) for item in quo_list[idx]]
	all_data.append(data)
	
	idx += 1
	i += 1

#all_data list拋到pandas
df = pd.DataFrame(all_data[1:], columns = all_data[0])
df2 = df.loc[:,['證券代號', '證券名稱', '開盤價', '最高價', '最低價', '收盤價', '本益比']]
print(df2)



