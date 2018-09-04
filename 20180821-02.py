import io
import pandas as pd
import requests

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
url = 'https://smart.tdcc.com.tw/opendata/getOD.ashx?id=1-5'
#url = 'http://www.tse.com.tw/fund/MI_QFIIS?response=csv&date=20180820&selectType=ALLBUT0999'
#url = 'https://www.google.com'
session = requests.session()
rt = session.get(url, headers=headers)
#print(rt.text)

with open('abc.csv', 'wb') as f:
	for chunk in rt.iter_content(chunk_size=1024):
		if chunk: # filter out keep-alive new chunks
			f.write(chunk)

#data = pd.read_csv(io.StringIO(rt.text), encoding='utf-8')
#print(data.head())
