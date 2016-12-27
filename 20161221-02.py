############################
#      連線PN300範例       #
############################
import telnetlib
import time

USER_ID = "account"
PASSWORD = "password"

tn = telnetlib.Telnet('127.0.0.1') 

tn.read_until(b"Username: ")
tn.write(USER_ID.encode('ascii') + b"\r")

tn.read_until(b"Password: ")
tn.write(PASSWORD.encode('ascii') + b"\r")

while True:
    line = tn.read_until(b"\r")  # Check for new line and CR
    print(line)
    if (b"DONE ! PROCESS NAME") in line:   # If last read line is the prompt, end loop
        break

# 等待直到命令提示符號出現
p = tn.read_until(b"[MIS.CPS]")
print(p)
tn.write(b"ren aaa.txt bbb.txt\r")

tn.read_until(b"[MIS.CPS]")
tn.write(b"ren ccc.txt ddd.txt\r")

tn.read_until(b"[MIS.CPS]")
tn.write(b"ren fff.txt eee.txt\r")

tn.read_until(b"[MIS.CPS]")
tn.write(b"del ggg.txt;* /nocon\r")

tn.read_until(b"[MIS.CPS]")
tn.write(b"logout\r")
time.sleep(1)

tn.close()
print("prog done..")