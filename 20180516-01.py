import requests
from selenium import webdriver
import time
from selenium.webdriver.support.select import Select

#driver = webdriver.Chrome()	# 需要看到執行過程可以用Chrome
driver = webdriver.PhantomJS()

driver.get("http://www.tdcc.com.tw/smWeb/QryStock.jsp")

time.sleep(1)

#html_source = driver.page_source
#print(html_source)

dt_obj = driver.find_element_by_id("scaDates")
#print(opt_list.text)

opt_list = []
for element in dt_obj.find_elements_by_tag_name('option'):
	#print(element.text)
	opt_list.append(element.text)

print(opt_list)
driver.quit()