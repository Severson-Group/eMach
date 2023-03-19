import numpy as np

a = [1,7,19,21,31]
b = [2,5,8,53,77]
c = [33,55,66,77,88]

d = np.stack((a,b,c),axis=1)

print(d)

d = np.sort(d)

print(d)

e = [list(x) for x in zip(*d)]
#print(d)
print(e)