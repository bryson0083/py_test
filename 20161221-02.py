import os;
#from subprocess import Popen, PIPE
import subprocess
import sys
from subprocess import Popen, PIPE, STDOUT

#os.system("\"C:\\PN300\\AXP76A.EMU\">yucps00 ");

#subprocess.call([r'C:\PN300\bin\Pn3Tel.exe', 'C:\PN300\AXP76A.EMU'])



p = Popen([r'C:\PN300\bin\Pn3Tel.exe', 'C:\PN300\AXP76A.EMU'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
#stdout_data = p.communicate(input="yucps00")
p.stdin.write(str('yourPassword\n'))
p.stdin.flush()