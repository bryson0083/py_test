from subprocess import Popen

p = Popen("a.bat")
stdout, stderr = p.communicate()