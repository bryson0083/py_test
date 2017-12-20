import pyodbc 

"""
#連SQL SERVER
cnxn = pyodbc.connect("Driver={SQL Server Native Client 10.0};"
					  "Server=ntsr12;"
					  "Database=per;"
					  "uid=XXXX;pwd=XXXX")
"""

#連RDB
cnxn = pyodbc.connect(r'DSN=RDBPCM60;UID=XXXX;PWD=XXXX')

sql_str = "select count(*) from pcmb020m"

cursor = cnxn.cursor()
cursor.execute(sql_str)

for row in cursor:
    print(row)
 