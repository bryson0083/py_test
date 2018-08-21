# -*- coding: utf-8 -*-
"""
chrome webdriver headless test

@Note:
	selenuim後續不再支援PhantomJS，測試chrome headless模式

@Ref:
	https://hk.saowen.com/a/c65442507ee9a5702755f87540343728898fc07ae75f7a92e540e55ae7cfd114
	https://www.bilibili.com/read/cv272427/

"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("https://www.google.com/")