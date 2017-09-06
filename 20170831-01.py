"""
抓取YAHOO FINANCE股價資料

NOTE:
安裝fix_yahoo_finance
$ pip install fix_yahoo_finance --upgrade --no-cache-dir

如果現有的pandas版本比較新，編譯會有錯誤，需要降版本
$ pip install -U pandas==0.19.2

"""
from pandas_datareader import data as pdr

import fix_yahoo_finance as yf
yf.pdr_override() # <== that's all it takes :-)

# download dataframe
data = pdr.get_data_yahoo("SPY", start="2017-08-01", end="2017-08-30")
print(data)

# download Panel
#data = pdr.get_data_yahoo(["SPY", "IWM"], start="2017-01-01", end="2017-04-30")
#print(data)
