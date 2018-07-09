import more_itertools as mit
from operator import itemgetter


def find_ranges(iterable):
    """Yield range of consecutive numbers."""
    for group in mit.consecutive_groups(iterable):
        group = list(group)
        if len(group) == 1:
            yield group[0]
        else:
            yield group[0], group[-1]


iterable = [96, 97, 98, 99, 100, 2, 3, 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24, 26]
a = list(find_ranges(iterable))
print(a)

filtered_ls = list(filter(lambda i:type(i) is tuple, a))
print(filtered_ls)

i = 0
max_diff = 0
for item in filtered_ls:
	val_diff = item[1] - item[0] + 1
	if (i==0) or (val_diff > max_diff): 
		major_tuple = item
		max_diff = val_diff

	i += 1


print(major_tuple)

