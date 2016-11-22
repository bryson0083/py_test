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

driver = webdriver.Firefox()
driver.get("http://mops.twse.com.tw/mops/web/t163sb04")

#網頁查詢條件輸入，並提交表單
elem = driver.find_element_by_name("year")
elem.send_keys("103")
elem = driver.find_element_by_name("season")
elem.find_element_by_xpath("//select[@name='season']/option[text()='2']").click()
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
tb_cnt = 1
while i <= tb_cnt:
	print("i=" + str(i))

	#組合搜尋條件參數
	arg_str = "//table[@class='hasBorder'][" + str(i) + "]/tbody"

	#讀取表格資料內容
	table = elem.find_element_by_xpath(arg_str)
	for row in table.find_elements_by_xpath(".//tr"):
		# way 1: 把tr下，所有td的欄位資料讀取到一個list中，並print出來
		#print([td.text for td in row.find_elements_by_xpath(".//td[text()]")])

		# way 2: 同上作用，但是把資料倒到一個有指定名稱的list，以便後續取用
		#a_list = [td.text for td in row.find_elements_by_xpath(".//td[text()]")]
		#print(a_list)

		# way 3
		a_list = [td.text for td in row.find_elements_by_xpath(".//td[text()]")]
		# a_list從td tag讀進資料，第一筆資料都是empty list，因此要過濾掉
		if a_list:
			a_list = a_list
			last_elem_idx = len(a_list)
			print(a_list[0] + "," + a_list[1] + "," + a_list[last_elem_idx-1])

	i += 1

	

print ("end of prog...")
