cnt = 0
while True:
	try:
		age = int(input("what is your age?"))
		break
	except:
		print("pls enter a num!")
		cnt = cnt + 1
		if cnt < 3:
			print("Err cnt=" + str(cnt))
		else:
			age = 0
			break

if age < 15:
	print("you are too young!")	