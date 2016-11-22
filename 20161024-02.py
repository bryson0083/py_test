# 綜合損益表資料讀取
#
# 讀取公開觀測資訊站
# => 財務報表 => 採IFRSs後 => 合併/個別報表 => 合併/個別報表 => 綜合損益表
#
# last_modify: 2016/10/24
#

#import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sys
import sqlite3
import datetime
from dateutil import parser

#sys.exit("For testing abort ......")

# 建立資料庫連線
conn = sqlite3.connect('market_price.sqlite')

# 建立網頁讀取
driver = webdriver.Firefox()
driver.get("http://mops.twse.com.tw/mops/web/t163sb04")

# 查詢網頁條件參數
sear_yyy = "102"
qq = "01"

sear_qq= str(int(qq))
yyyy = str(int(sear_yyy) + 1911)

#網頁查詢條件輸入，並提交表單
elem = driver.find_element_by_name("year")
elem.send_keys(sear_yyy)

elem = driver.find_element_by_name("season")
elem.find_element_by_xpath("//select[@name='season']/option[text()='" + sear_qq + "']").click()
driver.find_element_by_xpath("//input[@type='button'][@value=' 查詢 ']").click()

cnt = 0
delay = 10 # seconds

while True:
	try:
	    element_present = EC.presence_of_element_located((By.NAME, 'fm2'))
	    WebDriverWait(driver, delay).until(element_present)
	    print ("Page is ready!")
	    break
	except TimeoutException:
	    cnt += 1
	    print ("Load cnt=" + str(cnt))
	    if cnt >= 3:
	    	# 讀取時間太久，直接結束程式
	    	sys.exit("Err01: Too much time! errors!")

#計算有多少個符合條件特徵的表格個數
tables = driver.find_elements_by_xpath("//table[@class='hasBorder']")
tb_cnt = len(tables)
print("符合條件特徵的table個數=" + str(tb_cnt))

#網頁中符合條件的table資料都掃過一遍
i = 1
#tb_cnt = 1
while i <= tb_cnt:
	print("i=" + str(i))

	#組合搜尋條件參數
	arg_str = "//table[@class='hasBorder'][" + str(i) + "]/tbody"

	#讀取表格資料內容
	table = elem.find_element_by_xpath(arg_str)
	for row in table.find_elements_by_xpath(".//tr"):
		# 把tr下，所有td的欄位資料讀取到一個list中
		a_list = [td.text for td in row.find_elements_by_xpath(".//td[text()]")]

		# a_list從td tag讀進資料，第一筆資料都是empty list，因此要過濾掉
		if a_list:
			a_list = a_list
			last_elem_idx = len(a_list)
			#print(a_list[0] + "," + a_list[1] + "," + a_list[last_elem_idx-1])

			comp_id = a_list[0]		# 公司股票號碼
			comp_name = a_list[1]	# 公司股票名稱
			eps = a_list[last_elem_idx-1] # 基本每股盈餘（元）
			print(comp_id + "," + comp_name + "," + eps)

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
				sqlstr = "insert into MOPS_YQ values ("
				sqlstr = sqlstr + "'" + comp_id + "',"
				sqlstr = sqlstr + "'" + comp_name + "',"
				sqlstr = sqlstr + "'" + yyyy + "',"
				sqlstr = sqlstr + "'" + qq + "',"
				sqlstr = sqlstr + " " + eps + ","
				sqlstr = sqlstr + "0,"
				sqlstr = sqlstr + "'" + date_last_maint + "',"
				sqlstr = sqlstr + "'" + time_last_maint + "',"
				sqlstr = sqlstr + "'" + prog_last_maint + "' "
				sqlstr = sqlstr + ") "

			else:
				sqlstr = "update MOPS_YQ set "
				sqlstr = sqlstr + "eps=" + eps + ","
				sqlstr = sqlstr + "date_last_maint='" + date_last_maint + "',"
				sqlstr = sqlstr + "time_last_maint='" + time_last_maint + "',"
				sqlstr = sqlstr + "prog_last_maint='" + prog_last_maint + "' "
				sqlstr = sqlstr + "where "
				sqlstr = sqlstr + "COMP_ID='" + comp_id + "' and "
				sqlstr = sqlstr + "YYYY='" + yyyy + "' and "
				sqlstr = sqlstr + "QQ='" + qq + "' "

			try:
				cursor = conn.execute(sqlstr)
				conn.commit()
			except sqlite3.Error as er:
				print ('er:', er.message)

			# 關閉DB cursor
			cursor.close()
	i += 1

# 資料庫連線關閉
conn.close()

# 關閉瀏覽器視窗
driver.quit();

print ("End of MOPS_YQ_1...")