import telnetlib
import time
import datetime
from dateutil import parser

USER_ID = "yucps00"
PASSWORD = "cps111076a"
timeout = 20

tn = telnetlib.Telnet('100.1.1.2') 

#for telnetlib debug
#tn.set_debuglevel(1)

tn.read_until(b"Username: ",timeout)
tn.write(USER_ID.encode('ascii') + b"\r")

tn.read_until(b"Password: ",timeout)
tn.write(PASSWORD.encode('ascii') + b"\r")

#Date format convert
str_date = str(datetime.datetime.now())
#str_date = "2016-12-05 02:28:12"

dt  = parser.parse(str_date).strftime('%m%d')
dt2 = parser.parse(str_date).strftime("%d-%b-%Y %H").upper()
if dt2[0] == "0":
	dt2 = dt2[1:]

dt3 = parser.parse(str_date).strftime("%Y%m%d")

#紀錄執行LOG
name = "AP4_AGENT_" + dt3 + ".txt"
file = open(name, 'a', encoding = 'UTF-8')

file.write("\n\n\n*** LOG datetime  " + str(datetime.datetime.now()) + " ***\n")
file.write("執行AP4檢查...\n\n")

#Generate searching string
sear_str = 'SEAR BC5$LOG:BC5_A4_CMU.' + dt + ' "UT_NET_MBX_AST:  MSGTYPE =     30","' + dt2 + '" /MATCH=AND /STATISTICS\r'
print(sear_str)
file.write(sear_str + "\n")

#waiting for prompt
tn.read_until(b"[MIS.CPS]",timeout)
tn.write(sear_str.encode())	# string convert to bytes format

while True:
	line = tn.read_until(b"\r",timeout)  # Check for new line and CR
	line_str = line.decode("ASCII").replace("\n","").replace("[7m"," ").replace("[0m","")
	#print(line_str)

	if (b"Records matched:") in line:
		cnt = int(line_str[17:34].strip())
		print("Abnormal Records matched:" + str(cnt))
		file.write("Abnormal Records matched:" + str(cnt) + "\n\n")

	if (b"Elapsed CPU time:") in line:   # If last read line is the prompt, end loop
		break

#檢視LOG同一小時內，異常次數達三次以上，進行斷線重啟一次
if cnt > 2:
	file.write("$$$ AP4出現異常，執行重啟程序. $$$\n\n")
	tn.read_until(b"[MIS.CPS]",timeout)
	tn.write(b"dir\r")

	i = 0
	while True:
		line = tn.read_until(b"\r",timeout)
		line_str = line.decode("ASCII").replace("\n","").replace("[7m"," ").replace("[0m","")
		print(line_str)

		i += 1
		if i == 10:
			break

	tn.read_until(b"[MIS.CPS]",timeout)
	tn.write(b"dir\r")

	i = 0
	while True:
		line = tn.read_until(b"\r",timeout)
		line_str = line.decode("ASCII").replace("\n","").replace("[7m"," ").replace("[0m","")
		print(line_str)

		i += 1
		if i == 10:
			break

	tn.read_until(b"[MIS.CPS]",timeout)
	tn.write(b"dir\r")

	i = 0
	while True:
		line = tn.read_until(b"\r",timeout)
		line_str = line.decode("ASCII").replace("\n","").replace("[7m"," ").replace("[0m","")
		print(line_str)

		i += 1
		if i == 10:
			break

tn.read_until(b"[MIS.CPS]",timeout)
tn.write(b"logout\r")
time.sleep(1)

file.write("*** End LOG ***\n")

#close connection
tn.close()

# Close File
file.close()

print("prog done..")