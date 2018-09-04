import pandas as pd
import sqlite3

conn = sqlite3.connect('market_price.sqlite')
data_dt = '20180817'
strsql = "select count(*) as cnt from STOCK_DISPERSION where QUO_DATE='" + data_dt + "' "
df2 = pd.read_sql_query(strsql, conn)
select_cnt = df2['cnt'].iloc[0]
print(select_cnt)

df.to_sql("daily_flights", conn, if_exists="replace")
