import multiprocessing
import time

def f():
    print("In f")
    while True:
    	for 
    	pass

def g():
    print("In g")

if __name__ == '__main__':
	functions = {'f': f, 'g': g}
	func_name = 'f'
	multiprocessing.Process(target=functions.get(func_name), args=()).start()