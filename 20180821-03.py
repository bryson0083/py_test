# -*- coding: utf-8 -*-
"""
chrome webdriver test 檔案下載到特定目錄下

@Note:
	selenuim後續不再支援PhantomJS，測試chrome headless模式

@Ref:
	https://stackoverflow.com/questions/46937319/how-to-use-chrome-webdriver-in-selenium-to-download-files-in-python

"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": r"D:\py_test\tdcc_file",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get("https://smart.tdcc.com.tw/opendata/getOD.ashx?id=1-5")
