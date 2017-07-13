from selenium import webdriver
import json
from bs4 import BeautifulSoup
import codecs

driver = webdriver.PhantomJS() # or add to your PATH
#driver.set_window_size(1024, 768) # optional
#driver.save_screenshot('screen.png') # save a screenshot to disk

#進入登入網站頁面
driver.get('https://www.nvesto.com/user/login?normal_login=1')

#讀取帳密參數檔
with open('account.json') as data_file:
	data = json.load(data_file)

acc_id = data['nvesto']['id']
acc_pwd = data['nvesto']['pwd']

#輸入帳號密碼登入網站
elem = driver.find_element_by_name("LoginForm[email]")
elem.send_keys(acc_id)

elem = driver.find_element_by_name("LoginForm[password]")
elem.send_keys(acc_pwd)

driver.find_element_by_xpath("//button[@type='submit'][@class='btn_blue_send']").click()

#開啟券商進出分點網頁，讀取執行完後的頁面source code
driver.get('https://www.nvesto.com/tpe/2034/majorforce#!/fromdate/2017-07-12/todate/2017-07-12/view/summary')
pageSource = driver.page_source
#print(pageSource)

#關閉PhantomJS
driver.close()

#For test 讀取local網頁存檔
#f=codecs.open("C:/Users/bryson0083/Desktop/Nvesto.html", 'r',encoding = 'utf8')
#pageSource = f.read()
#print(pageSource)

#讀取網頁SOURCE CODE
sp = BeautifulSoup(pageSource, 'html.parser')

#讀取券商進出分點買賣超資料
table_buy = sp.findAll('table', attrs={'class':'table table-bordered'})[1]
print(table_buy)

table_sell = sp.findAll('table', attrs={'class':'table table-bordered'})[3]
print(table_sell)