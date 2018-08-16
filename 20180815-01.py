import datetime
from dateutil import parser

#current datetime to vms date
str_date = str(datetime.datetime.now())
#str_date = "2016-02-01 09:28:12"
dt = parser.parse(str_date).strftime("%d-%b-%Y").upper()
print(dt)
dt = parser.parse(str_date).strftime("%d-%b-%Y %H:%M:%S.%f").upper()[:-4]
print(dt)

#input vms datetime convert to char(8) date and char(6) time 
str_date = "15-AUG-2018 09:28:12.11"
c8_date = parser.parse(str_date).strftime("%Y%m%d")
c6_time = parser.parse(str_date).strftime("%H%M%S")
print(c8_date)
print(c6_time)
