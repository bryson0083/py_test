# -*- coding: utf-8 -*-
"""
技術分析選股 TYPE 09 上傳Firebase

@author: Bryson Xue

@target_rul: 

@Note: 
	選股結果上傳Firebase

"""
import pandas as pd
import xlrd
import sys, os
from firebase import firebase

def MAIN_STOCK_SELECT_09_FB():
	print("Executing " + os.path.basename(__file__) + "...")

	try:
		wb = xlrd.open_workbook('aaa.xlsx', on_demand = True)
	except Exception as e:
		print('Err: 讀取選股excel檔異常.')
		print(e.args)
		return

	sh = wb.sheet_by_index(0)
	row_cnt = sh.nrows

	row_ls = []
	for i in range(1,row_cnt):
		d = {}
		#print(i)
		d['股票代號'] = sh.cell(i,0).value.replace('.TW','')
		d['名稱'] = sh.cell(i,1).value
		d['外資買賣超天數'] = sh.cell(i,4).value
		d['投信買賣超天數'] = sh.cell(i,5).value
		d['自營商買賣超天數'] = sh.cell(i,6).value
		d['類別'] = sh.cell(i,7).value
		#print(d)
		row_ls.append(d)

	#關閉excel檔案
	wb.release_resources()
	del wb

	#print(row_ls)
	try:
		#建立firebase資料連線
		db_url = 'https://brysonxue-bfca6.firebaseio.com/'
		fdb = firebase.FirebaseApplication(db_url, None)

		#轉存firebase前，清空線上的資料
		fdb.delete('/STOCK_S09', None)

		#資料轉存firebase
		for row in row_ls:
			fdb.post('/STOCK_S09', row)

		print('上傳STOCK_S09成功.')
	except Exception as e:
		print('Err: 資料上傳Firebase table => STOCK_S09異常.')
		print(e.args)
		return

	print("End of prog.")

if __name__ == '__main__':
	MAIN_STOCK_SELECT_09_FB()	