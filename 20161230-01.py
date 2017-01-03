import datetime
from dateutil import parser

#str_date = str(datetime.datetime.now())
str_date = "2016-12-05 02:28:12"
print(str_date)

dt = parser.parse(str_date).strftime("%d-%b-%Y").upper()
print(dt)

dt = parser.parse(str_date).strftime('%m%d')
print(dt)

dt2 = parser.parse(str_date).strftime("%d-%b-%Y %H").upper()
if dt2[0] == "0":
	dt2 = dt2[1:]
print(dt2)

sear_str = 'SEAR BC5$LOG:BC5_A4_CMU.' + dt + ' "UT_NET_MBX_AST:  MSGTYPE =     30","' + dt2 + '" /MATCH=AND /STATISTICS\r'
print(sear_str)




