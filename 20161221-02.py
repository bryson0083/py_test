import os;
#from subprocess import Popen, PIPE
import subprocess
import sys
from subprocess import Popen, PIPE, STDOUT

#os.system("\"C:\\PN300\\AXP76A.EMU\">yucps00 ");

#subprocess.call([r'C:\PN300\bin\Pn3Tel.exe', 'C:\PN300\AXP76A.EMU'])




import telnetlib

USER_ID = "yucps00"
PASSWORD = "cps111036a"
timeout = 30
tn = telnetlib.Telnet('100.1.1.6') 
print("111")
tn.read_until(b"Username: ")
print("222")
tn.write(USER_ID.encode('ascii') + b"\n")
print("333")
tn.read_until(b"Password: ")
print("444")
tn.write(PASSWORD.encode('ascii') + b"\n")
print("555")

while True:
    line = tn.read_until(b"\n")  # Check for new line and CR
    print(line)
    if (b"DONE ! PROCESS NAME") in line:   # If last read line is the prompt, end loop
        break



tn.read_until(b"[MIS.CPS]")
print("666")
tn.write(b"show time\n")
print("777")


print("888")
tn.write(b"vt100\n")
print(tn.read_all().decode('ascii'))
print("999")
tn.close()





