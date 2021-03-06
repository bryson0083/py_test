############################
#      連線PN300範例       #
############################
import telnetlib
import time

USER_ID = "yucps00"
PASSWORD = "cps111036a"

tn = telnetlib.Telnet('100.1.1.6') 

#for telnetlib debug
tn.set_debuglevel(1)

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
tn.write(b"DIR\r")

"""
tn.write(b"ren aaa.txt bbb.txt\r")

tn.read_until(b"[MIS.CPS]")
tn.write(b"ren ccc.txt ddd.txt\r")

tn.read_until(b"[MIS.CPS]")
tn.write(b"ren fff.txt eee.txt\r")

tn.read_until(b"[MIS.CPS]")
tn.write(b"del ggg.txt;* /nocon\r")
"""

tn.read_until(b"[MIS.CPS]")
tn.write(b"logout\r")
time.sleep(1)

tn.close()
print("prog done..")