# 上市公司清單讀取(db not yet)
#
# 資料來源: 證券交易所
# 
#
# last_modify: 2016/11/02
#

#import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os.path

name = "COMP_LIST.txt"
file = open(name, 'a', encoding = 'UTF-8')

driver = webdriver.Firefox()
driver.get("http://isin.twse.com.tw/isin/C_public.jsp?strMode=2")

elem = driver.find_element_by_class_name("h4")

cnt = 0
delay = 10 # seconds

while True:
	try:
	    element_present = EC.presence_of_element_located((By.TAG_NAME, 'h2'))
	    WebDriverWait(driver, delay).until(element_present)
	    print ("Page is ready!")
	    break
	except TimeoutException:
	    cnt += 1
	    print ("Load cnt=" + str(cnt))
	    if cnt >= 3:
		    # 關閉瀏覽器視窗
		    driver.quit();

		    # 讀取時間太久，直接結束程式
		    file.write("@@@ 網頁讀取逾時或該網頁無資料. @@@\n")
		    file.close()
		    sys.exit("@@@ 網頁讀取逾時或該網頁無資料. @@@")

#計算有多少個符合條件特徵的表格個數
tables = driver.find_elements_by_xpath("//table[@class='h4']")
tb_cnt = len(tables)
print("符合條件特徵的table個數=" + str(tb_cnt))

#網頁中符合條件的table資料都掃過一遍
i = 1
tb_cnt = 1
while i <= tb_cnt:
	print("i=" + str(i))

	#組合搜尋條件參數
	arg_str = "//table[@class='h4'][" + str(i) + "]/tbody"

	j = 1
	#讀取表格資料內容
	table = elem.find_element_by_xpath(arg_str)
	for row in table.find_elements_by_xpath(".//tr"): 
		# 把tr下，所有td的欄位資料讀取到一個list中
		a_list = [td.text for td in row.find_elements_by_xpath(".//td[text()]")]

		# a_list從td tag讀進資料，去除empty list
		if a_list:
			if a_list[0] != "有價證券代號及名稱":  # 排除第一筆不需要的資料
				#print(a_list)
				file.write(str(a_list)+"\n")

				# 從a_list[0]拆解出代號跟公司名稱
				t = str(a_list[0]).split("\u3000") 
				comp_id = str(t[0]).strip(" ")	# 公司代號
				comp_name = str(t[1]).strip(" ")	# 公司名稱
				ipo_date = str(a_list[2]).replace("/","") # 公開上市日期
				industry = str(a_list[4])	# 產業類別

				print(comp_id+" "+comp_name+" "+ipo_date+" "+industry+"\n")
				file.write(comp_id+" "+comp_name+" "+ipo_date+" "+industry+"\n")

				cid_len = len(comp_id)
				#print("len of comp_id=" + str(len(cid_len)))

				# 非上市股票的資料就不需要了(用代碼是否為四碼來判斷)
				if cid_len > 4:
					print("break in cid="+comp_id+","+comp_name+"\n")
					break

		#j += 1
		#if j==10 :
		#	break

	i += 1

# 關閉瀏覽器視窗
driver.quit();

# Close File
file.close()
print ("end of prog...")