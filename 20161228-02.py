############################
#      連線PN300範例       #
############################
import telnetlib
import time

USER_ID = "yucps00"
PASSWORD = "cps111076a"
timeout = 20

tn = telnetlib.Telnet('100.1.1.2') 

#for debug
#tn.set_debuglevel(1)

tn.read_until(b"Username: ",timeout)
tn.write(USER_ID.encode('ascii') + b"\r")

tn.read_until(b"Password: ",timeout)
tn.write(PASSWORD.encode('ascii') + b"\r")

#waiting for prompt
p = tn.read_until(b"[MIS.CPS]",timeout)
#print(p)
tn.write(b'SEAR BC5$LOG:BC5_A4_CMU.1205 "UT_NET_MBX_AST:  MSGTYPE =     30" /OUTPUT=TMP.TXT\r')

tn.read_until(b"[MIS.CPS]",timeout)
tn.write(b"COPY END_OF_FILE.TXT TMPEOF.TXT\r")

tn.read_until(b"[MIS.CPS]",timeout)
tn.write(b"APPEND TMPEOF.TXT TMP.TXT\r")

tn.read_until(b"[MIS.CPS]",timeout)
tn.write(b"type TMP.TXT\r")

while True:
    line = tn.read_until(b"\r",timeout)  # Check for new line and CR
    line_str = line.decode("ASCII").replace("\n","").replace("[7m"," ").replace("[0m","")
    print(line_str)

    if (b"END OF FILE") in line.upper():   # If last read line is the prompt, end loop
        break

tn.read_until(b"[MIS.CPS]",timeout)
tn.write(b"DELETE TMP.TXT;* /NOCON\r")

tn.read_until(b"[MIS.CPS]",timeout)
tn.write(b"DELETE TMPEOF.TXT;* /NOCON\r")

tn.read_until(b"[MIS.CPS]",timeout)
tn.write(b"logout\r")
time.sleep(1)

#close connection
tn.close()
print("prog done..")