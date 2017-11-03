import multiprocessing
import time
import test_func

# Your foo function
def foo(n):
	print('Starting:', multiprocessing.current_process().name)
	for i in range(10000 * n):
		print("Tick")
		time.sleep(1)

	print('Exiting :', multiprocessing.current_process().name)


if __name__ == '__main__':
	# Start foo as a process
	p = multiprocessing.Process(target=foo, name="Foo", args=(1,))
	#p = multiprocessing.Process(target=test_func.test_a, name="TEST_A")
	p.start()
	#test_func.test_a()
	print(p.is_alive())
	p.join(5)
	p.terminate()
	p.join()
	print(p.is_alive())

	"""
	# Wait a maximum of 10 seconds for foo
	# Usage: join([timeout in seconds])
	p.join(10)

	# If thread is active
	if p.is_alive():
		print("foo is running... let's kill it...")

		# Terminate foo
		p.terminate()
		p.join()
	"""		