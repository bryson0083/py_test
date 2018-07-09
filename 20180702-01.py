# -*- coding: utf-8 -*-
"""


"""

def some_code_that_may_raise_our_value_error():
	#raise ValueError('Represents a hidden bug, do not catch this')
	raise Exception('This is the exception you expect to handle')

def call_func():
	i = 1
	while True:
		try:
			some_code_that_may_raise_our_value_error()

		except ValueError as err:
			print("ValueError is occurred")
			print(err.args)
		except Exception as err:
			print("Internal Exception is occurred")
			print(err.args)
			if i == 3:
				print("End the loop.")
				raise Exception('Before end of the loop throw the exception.')
				#break
			else:
				print("Err cnt =>" + str(i))
				i += 1

try:
	call_func()
except Exception as err:
	print("Outer Exception is occurred")
	print(err.args)