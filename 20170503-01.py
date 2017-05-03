from datetime import date, timedelta

def f(d1, d2):
	delta = d2 - d1
	return set([d1 + timedelta(days=i) for i in range(delta.days + 1)])

range1 = [date(2016, 6, 1), date(2016, 6, 20)]
range2 = [date(2016, 6, 1), date(2016, 6, 20)]
set_a = f(*range1) & f(*range2) #arbitrary argument list  http://stackoverflow.com/questions/919680/can-a-variable-number-of-arguments-be-passed-to-a-function

#print(f(*range1) & f(*range2))
print(set_a)
