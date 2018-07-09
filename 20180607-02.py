import datetime
from dateutil.parser import parse
from dateutil import parser

from dateutil.relativedelta import relativedelta

date_fmt = "%Y%m%d%H%M%S"

a = datetime.datetime.strptime("20180607110000", date_fmt)
b = datetime.datetime.strptime("20180607111000", date_fmt)

delta = b - a
print(delta.days)
print(delta.seconds)