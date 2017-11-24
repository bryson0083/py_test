from subprocess import Popen

p = Popen("a.bat")
stdout, stderr = p.communicate()

p = Popen("a2.bat")
stdout, stderr = p.communicate()