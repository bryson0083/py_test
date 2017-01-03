import datetime
from dateutil.parser import parse
from dateutil import parser

from dateutil.relativedelta import relativedelta

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

# other date format
str_date = str(datetime.datetime.now())
#str_date = "2016-02-01 09:28:12"
print(str_date)

dt = parser.parse(str_date).strftime("%d-%b-%Y").upper()
print(dt)

dt = parser.parse(str_date).strftime("%d-%b-%Y %H").upper()
print(dt)

dt = parser.parse(str_date).strftime("%Y%m%d")
print(dt)

dt = parser.parse(str_date).strftime('%m%d')
print(dt)

dt = parser.parse(str_date).strftime('%m')
print(dt)


# test date add
#str_date = str(datetime.datetime.now())
str_date = "2016-02-01 09:28:12"
print(str_date)

date_fmt = "%Y/%m/%d"
start_date = parser.parse(str_date).strftime("%Y%m%d")
print("str_start_date=" + start_date)

start_date = parser.parse(start_date).strftime(date_fmt)
date_1 = datetime.datetime.strptime(start_date, date_fmt)

end_date = date_1 + datetime.timedelta(days=1)
end_date = str(end_date)[0:10]
end_date = parser.parse(end_date).strftime(date_fmt)
print("str_end_date=" + end_date)

# test date add 2
dt = datetime.datetime.now() + relativedelta(years=1)
print(dt)

dt = datetime.datetime.now() + relativedelta(months=1)
print(dt)

dt = datetime.datetime.now() + relativedelta(days=6)
print(dt)

#print(parse(end_date).strftime("%m"))

# Date diff
date_fmt = "%Y/%m/%d"
start_date = "20160229"
start_date = parser.parse(start_date).strftime(date_fmt)
date_1 = datetime.datetime.strptime(start_date, date_fmt)

end_date = date_1 + datetime.timedelta(days=1)
end_date = str(end_date)[0:10]
end_date = parser.parse(end_date).strftime(date_fmt)

print(str(start_date) + "~" + str(end_date))

#a = datetime.datetime.strptime(start_date, date_fmt)
#b = datetime.datetime.strptime(end_date, date_fmt)
a = datetime.datetime.strptime("2016/01/01", date_fmt)
b = datetime.datetime.strptime("2016/01/10", date_fmt)

delta = b - a
print(delta.days)