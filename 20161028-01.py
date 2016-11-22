import pandas as pd
import pandas_datareader.data as web
import datetime
start = datetime.datetime.strptime('10/27/2016', '%m/%d/%Y')
end = datetime.datetime.strptime('10/27/2016', '%m/%d/%Y')

# 讀取股價資料
com_stock = web.DataReader('2002.TW','yahoo',start,end)

# 全部資料
print("原始資料 From Yahoo\n" + str(com_stock) + "\n")

# 只取Adj Close欄位
print(str(com_stock['Adj Close']) + "\n")

# 資料丟到DataFrame
df = pd.DataFrame(com_stock)

# 直接print DataFrame內容
print("直接print DataFrame內容\n" + str(df) + "\n")

# 抓取日期的部分
print(df.index[0])

# 抓取Open(開盤價)
print(df.iloc[0][0])

# 抓取High(最高價)
print(df.iloc[0][1])

# 抓取Low(最低價)
print(df.iloc[0][2])

# 抓取Close(收盤價)
print(df.iloc[0][3])

# 抓取Volume(成交量)
print(df.iloc[0][4])

# 抓取Adj Close(調整後收盤價)
print(df.iloc[0][5])

# 其他使用範例
f = web.DataReader(['GOOG','AAPL'], 'yahoo', start, end)
print ('Adjusted Closing Prices')
print (f['Adj Close'].describe())
