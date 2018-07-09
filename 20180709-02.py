
"""
Find the maximum value in a list of tuples in Python 

Ref:
	https://stackoverflow.com/questions/13145368/find-the-maximum-value-in-a-list-of-tuples-in-python
	https://stackoverflow.com/questions/18352784/how-to-remove-all-of-certain-data-types-from-list
	https://stackoverflow.com/questions/13638898/how-to-use-filter-map-and-reduce-in-python-3
	http://www.runoob.com/python/python-func-filter.html

"""
from operator import itemgetter

lis=[(101, 153), (255, 827), (361, 961)]

#效能較使用lambda好
b = max(lis,key=itemgetter(1))
print(b)

b = max(lis,key=lambda item:item[1])
#b = min(lis,key=lambda item:item[1])
print(b)

#排除list中非tuple元素
lis = [(96, 100), (2, 8), (12, 17), (20, 24), 26]
filtered_A = list(filter(lambda i:type(i) is tuple, lis))
print(filtered_A)
