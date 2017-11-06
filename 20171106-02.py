"""
Note: 
	$ pip install schedule

Ref:
	https://pypi.python.org/pypi/schedule
	https://schedule.readthedocs.io/en/stable/index.html

"""
import schedule
import time

def job():
    print("I'm working...")

#schedule.every(5).seconds.do(job)
#schedule.every(10).minutes.do(job)
#schedule.every().hour.do(job)
schedule.every().day.at("14:44").do(job)
#schedule.every().monday.do(job)
#schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)