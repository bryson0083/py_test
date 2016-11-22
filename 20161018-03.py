a_list=["1","2","3","4","5","6"]
print(a_list[0])
print([a for a in a_list])

b=[a for a in a_list]
print(b[0])

# check list is empty or not.
list3=[]
if not list3:
	print("aaa")
else:
	print("bbb")