import more_itertools as mit

def find_ranges(iterable):
    """Yield range of consecutive numbers."""
    for group in mit.consecutive_groups(iterable):
        group = list(group)
        if len(group) == 1:
            yield group[0]
        else:
            yield group[0], group[-1]


iterable = [96, 97, 98, 99, 100, 2, 3, 4, 5, 12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 26]
a = list(find_ranges(iterable))

print(a)