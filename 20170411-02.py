a = ['aaa', 'bbb']
print(a.index("bbb"))

a = [['aaa', 'bbb'],['ccc','ddd']]
c = [b.index("bbb") for b in a]
print(c)