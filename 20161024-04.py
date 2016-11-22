import sys
import datetime
from dateutil import parser
from dateutil.parser import parse

def mode_c():
	#str_date = "2016-04-05"
	str_date = str(datetime.datetime.now())
	
	# 轉換日期為C8格式字串
	dt_c8 = parser.parse(str_date).strftime("%Y%m%d")
	yyyy = dt_c8[0:4]
	print(yyyy)

	# 轉西元年為民國年
	yyy = str(int(yyyy) - 1911)
	#print(yyy)

	# 取出月日的部分
	mmdd = dt_c8[4:]
	#print(mmdd)

	# 註：依證券交易法第36條及證券期貨局相關函令規定，財務報告申報期限如下：
	# 1.一般行業申報期限：第一季為5月15日，第二季為8月14日，第三季為11月14日，年度為3月31日。
	# 2.金控業申報期限：第一季為5月30日，第二季為8月31日，第三季為11月29日，年度為3月31日。
	# 3.銀行及票券業申報期限：第一季為5月15日，第二季為8月31日，第三季為11月14日，年度為3月31日。
	# 4.保險業申報期限：第一季為5月15日，第二季為8月31日，第三季為11月14日，年度為3月31日。
	# 5.證券業申報期限：第一季為5月15日，第二季為8月31日，第三季為11月14日，年度為3月31日。

	# 只在以下特定幾天結轉季報資料
	if mmdd == "0405":
		yyy = str(int(yyy) - 1)
		qq = "04"
	elif mmdd == "0605":
		qq = "01"
	elif mmdd == "0905":
		qq = "02"
	elif mmdd == "1205":
		qq = "03"
	else:
		sys.exit(mmdd + " No need to get data.")

	print("結轉yyyqq=" + yyy + qq)


def mode_h():
	yyyy = str(input("輸入抓取資料年分(YYYY):"))
	qq = str(input("輸入抓取資料季別(QQ):"))

	# 轉西元年為民國年
	yyy = str(int(yyyy) - 1911)

	print("結轉yyyqq=" + yyy + qq)


def mode_a():

	for y in range(2013,2017,1):
		print("y=" + str(y))
		yyy = str(y - 1911)
		q = 1
		while q <= 4:
			if q == 1:
				qq = "01"
			elif q == 2:
				qq = "02"
			elif q == 3:
				qq = "03"
			else:
				qq = "04"

			print("結轉yyyqq=" + yyy + qq)
			q += 1


try:
	run_mode = sys.argv[1]
	run_mode = run_mode.upper()
except Exception as e:
	run_mode = "C"

print("you choose mode " + run_mode)

if run_mode == "C":
	mode_c()
elif run_mode == "H":
	mode_h()
elif run_mode == "A":
	mode_a()
else:
	sys.exit("No such input arg.")