import datetime
from dateutil.parser import parse
from dateutil import parser

# print current datetime
dt=datetime.datetime.now()
print("output 1:" + str(dt))
print("output 2:" + str(dt.year) + str(dt.month) + str(dt.day))

# convert str to datetime
dt = datetime.datetime.strptime('24052010', '%d%m%Y').date()
print("output 3:" + str(dt))

dt = datetime.datetime.strptime('20161024', '%Y%m%d').date()
print("output 4:" + str(dt))

dt = datetime.datetime.strptime('20160901', '%Y%m%d').date()
print("output 5:" + str(dt))

# format date
#str_date = '30th November 2009'
str_date = "2016-09-01"
#str_date = "2016/01/02"

dt = parser.parse(str_date).strftime("%Y%m%d")
print("output 5:" + str(dt))

# get current c8 date and c6 time
str_date = str(datetime.datetime.now())
dt_c8 = parser.parse(str_date).strftime("%Y%m%d")
print("output 6:" + str(dt_c8))

dt_c6 = parser.parse(str_date).strftime("%H%M%S")
print("output 7:" + str(dt_c6))