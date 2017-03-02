import ftplib

#Open ftp connection
ftp = ftplib.FTP('100.1.1.6')
ftp.login('yucps00','cps111036a')

#List the files in the current directory
#print ("File List:")
#files = ftp.dir()
#print (files)

files = []

try:
	files = ftp.nlst()
except ftplib.error_perm:
	print("error!!!")
	#if str(resp) == "550 No files found":
	#	print("No files in this directory")
	#else:
	#	raise

for f in files:
	print(f)


"""
#Get the readme file
ftp.cwd("$1$DGA2:[MIS.CRM.BC5.LOG]")
gFile = open("BC5_A4_CMU.1228", "wb")
ftp.retrbinary('RETR Readme', gFile.write)
gFile.close()
ftp.quit()

#Print the readme file contents
print ("\nReadme File Output:")
gFile = open("BC5_A4_CMU.1228", "r")
buff = gFile.read()
print (buff)
gFile.close()
"""