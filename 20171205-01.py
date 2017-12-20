# -*- coding: utf-8 -*-
"""
Selenium IE webdriver test

@author: Bryson Xue

@Note:
	driver for IE 11

@Ref:
	https://stackoverflow.com/questions/24925095/selenium-python-internet-explorer
	https://stackoverflow.com/questions/16682169/unable-to-launch-internet-explorer-through-selenium-webdriver-python-bindings
	https://github.com/seleniumQuery/seleniumQuery/wiki/seleniumQuery-and-IE-Driver
	https://github.com/seleniumhq/selenium-google-code-issue-archive/issues/1795
"""
from selenium import webdriver

#driver = webdriver.Ie(r"D:\\py_yusco\\IEDriverServer.exe") #deriver exe 放置絕對路徑目錄下
driver = webdriver.Ie(r"IEDriverServer.exe")	#deriver exe 放置同一層目錄下

driver.get('https://www.google.com.tw')

driver.quit()	#關閉瀏覽器