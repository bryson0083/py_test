# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 09:26:24 2017

@author: bryson0083
"""

import csv
f = open('test.csv', 'r')
for row in csv.DictReader(f, ["證券代號","證券名稱","成交股數","成交筆數","成交金額","開盤價","最高價","最低價","收盤價","漲跌(+/-)","漲跌價差","最後揭示買價","最後揭示買量","最後揭示賣價","最後揭示賣量","本益比"]):
	print(row["證券代號"])
	print(row["證券代號"], row["證券名稱"])