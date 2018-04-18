import datetime
from dateutil.parser import parse
from dateutil import parser
from dateutil.relativedelta import relativedelta

date_fmt = "%Y/%m/%d %H:%M:%S"

a = datetime.datetime.strptime("2018/03/31 23:59:00", date_fmt)
b = datetime.datetime.strptime("2018/04/02 00:01:30", date_fmt)
delta = b - a
#diff_time_minu = delta.seconds / 60
print(delta.days)
print(delta.seconds)
#print(str(delta))
#print(repr(delta))

tot_diff_minu = delta.days * 1440 + delta.seconds / 60
print(tot_diff_minu)