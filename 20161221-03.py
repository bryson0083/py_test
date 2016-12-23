# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 20:46:36 2016

@author: bryson0083
"""


import subprocess, sys, shlex
import time

"""
cmd = "C:\Program Files (x86)\PCMan\PCMan.exe"
process = subprocess.run([cmd,'ptt.cc\n','bryson0083\n'], stdout=subprocess.PIPE, shell=True)
proc_stdout = process.communicate()[0].strip()
print(proc_stdout)
"""

"""
import subprocess  
import os
  

p = subprocess.Popen("C:\Program Files (x86)\PCMan\PCMan.exe", stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)  
  
p.stdin.write(bytes('bryson0083\n'))  
p.stdin.flush()
#p.stdin.write(b'boisgood')  
#print(p.stdout.read())  
"""


p = subprocess.Popen('cmd', stdin=subprocess.PIPE, universal_newlines=True)
time.sleep(2)
p.stdin.write('dir\n')
#out, err = p.communicate()
#print(err)


#p.stdin.write(b'cps111036a\r')
#time.sleep(1)
#p.stdin.write(b'dir\r')
#time.sleep(1)
#p.communicate()[0]
p.stdin.close()

#grep_stdout = p.communicate(input=b'yucps00\ncps111036a\ndir\n')[0]
#print(grep_stdout)

#os.popen(cmd, 'w', bufsize)