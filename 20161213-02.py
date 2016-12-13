# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 16:02:46 2016

@author: bryson0083
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.parse import urlencode
import httplib2

url = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX.php'
data = {'download': 'csv', 'qdate': '103/12/23', 'selectType': 'ALLBUT0999'}
agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'

httplib2.debuglevel = 1
conn = httplib2.Http('.cache')
headers = {'Content-type': 'application/x-www-form-urlencoded',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'User-Agent': agent}
resp, content = conn.request(url, 'POST', urlencode(data), headers)

#print(resp.status, resp.reason)
#print(content.decode('cp950'))

with open('aaa.csv', 'wb') as f:
	f.write(content)