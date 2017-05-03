from datetime import date, timedelta

def f(d1, d2):
	delta = d2 - d1
	return set([d1 + timedelta(days=i) for i in range(delta.days + 1)])

range_xr = [date(2017, 7, 30), date(2017, 8, 15)]
range_xd = [date(2017, 8, 1), date(2017, 8, 10)]

intersection = f(*range_xr) & f(*range_xd)
#intersection = sorted(intersection)

if intersection:
	print("intersection\n")
	print(intersection)
	print(str(min(intersection)) + "~" + str(max(intersection)) + "\n\n")
print("\n\n")



set_a = f(*range_xr) - f(*range_xd)
#et_a = sorted(set_a)

if set_a:
	print("set_a\n")
	a = sorted(set_a)
	print(str(a))
	print(str(min(set_a)) + "~" + str(max(set_a)) + "\n\n")

	tmp = set_a - intersection
	tmp = sorted(tmp)
	print(str(tmp) + "\n\n")

print("\n\n")



set_c = f(*range_xd) - f(*range_xr)
set_c = sorted(set_c)

if set_c:
	print("set_c\n")
	print(set_c)
	print(str(min(set_c)) + "~" + str(max(set_c)) + "\n\n")
print("\n\n")
