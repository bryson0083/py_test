import os.path
import datetime
import time
from dateutil.parser import parse
from dateutil import parser

tStart = time.time()#計時開始

# print current datetime
dt=datetime.datetime.now()

name = "MOPY_LOG_" + str(dt.year) + str(dt.month) + str(dt.day) + ".txt"
is_exist = os.path.exists(name)

if is_exist == True:
	file = open(name, 'a', encoding = 'UTF-8')
else:
	file = open(name, 'a', encoding = 'UTF-8')

print("##############################################")
print("##    公開觀測資訊站~綜合損益表資料讀取     ##")
print("##                                          ##")
print("##                                          ##")
print("##   datetime: " + str(dt) +            "   ##")
print("##############################################")

dt=datetime.datetime.now()
file.write("*** LOG datetime  " + str(dt) + " ***\n")

file.write("test 1\n")
file.write("test 2\n")
file.write("test 3\n")
file.write("test 4\n")
file.write("test 5\n")
file.write("test 6\n")
file.write("test 7\n")

tEnd = time.time()#計時結束
file.write ("\n\n\nIt cost %f sec\n" % (tEnd - tStart)) #會自動做近位

file.write("*** End LOG ***\n\n\n")

file.close()
