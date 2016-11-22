import sqlite3

# 建立資料庫連線
conn = sqlite3.connect('market_price.sqlite')

# SQL Select type 1
sqlstr = "select * from prices where gdate='2016/10/03'"
cursor = conn.execute(sqlstr)

for row in cursor:
	print("Type 1:  日期：{}，92無鉛：{}，95無鉛：{}，98無鉛：{}". \
            format(row[0],row[1],row[2],row[3]))

# SQL Select type 2
sqlstr = "select * from prices where gdate='2016/10/24'"
cursor = conn.execute(sqlstr)

for row in cursor:
	print("Type 2:  日期：{}，92無鉛：{}，95無鉛：{}，98無鉛：{}". \
            format(row[0],row[1],row[2],row[3]))

# SQL Insert
sqlstr = "insert into prices values ('2016/10/24',1.11,2.22,3.33)"
cursor = conn.execute(sqlstr)

# SQL Update
sqlstr = "update prices set g92=4.44, g95=5.55, g98=6.66 where gdate='2016/10/24'"
cursor = conn.execute(sqlstr)

# SQL Delete
sqlstr = "delete from prices where gdate='2016/10/24'"
cursor = conn.execute(sqlstr)

conn.commit()