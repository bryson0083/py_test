# -*- coding: utf-8 -*-
"""
openpyxl lib test

@author: Bryson Xue

@Note: 
    1. 測試讀取xlsx file
    3. pip install openpyxl
    4. Ref => https://openpyxl.readthedocs.io/en/default/
    		  http://liyangliang.me/posts/2013/02/using-openpyxl-to-read-and-write-xlsx-files/
"""
import openpyxl as px

W = px.load_workbook('test_data.xlsx')
p = W.get_sheet_by_name(name = '工作表1')

rows = p.rows
columns = p.columns

content = []
for row in rows:
    line = [col.value for col in row]
    content.append(line)

print(content)