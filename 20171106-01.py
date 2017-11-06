"""

Thread 有五種狀態
1. New Thread
2. Runnable
3. Running
4. Not-Running
5. Dead

"""
import threading
import time

def task_1():
	print("Execute task_1...")

def schd_1():
	print("Execute schd_1...")
	threading.Timer(5,schd_1).start()
	task_1()

def task_2():
	print("Execute task_2...")

def schd_2():
	print("Execute schd_2...")
	threading.Timer(10,schd_2).start()
	task_2()

schd_1()
time.sleep(10)
schd_2()
