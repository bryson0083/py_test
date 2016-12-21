# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 20:46:36 2016

@author: bryson0083
"""


import subprocess, sys, shlex

cmd = "C:\Program Files (x86)\PCMan\PCMan.exe"
process = subprocess.run([cmd,'ptt.cc\n','bryson0083\n'], stdout=subprocess.PIPE, shell=True)
proc_stdout = process.communicate()[0].strip()
print(proc_stdout)


"""
import subprocess  
import os
  

p = subprocess.Popen("C:\Program Files (x86)\PCMan\PCMan.exe", stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = True)  
  
p.stdin.write(bytes('bryson0083\n'))  
p.stdin.flush()
#p.stdin.write(b'boisgood')  
#print(p.stdout.read())  
"""

"""
calcProc = subprocess.Popen(['c:\\Windows\\System32\\calc.exe'], shell=True, stdin=subprocess.PIPE)
calcProc.poll() == None

calcProc.wait()
calcProc.poll()

print("shhhhhhhh")
calcProc.communicate(b'1')
"""