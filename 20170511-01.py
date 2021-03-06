import multiprocessing
import time

# Your foo function
def foo(n):
	for i in range(10000 * n):
		print("Tick")
		time.sleep(1)

if __name__ == '__main__':
	# Start foo as a process
	p = multiprocessing.Process(target=foo, name="Foo", args=(10,))
	p.start()

	# Wait a maximum of 10 seconds for foo
	# Usage: join([timeout in seconds])
	p.join(10)

	# If thread is active
	if p.is_alive():
		print("foo is running... let's kill it...")

		# Terminate foo
		p.terminate()
		p.join()