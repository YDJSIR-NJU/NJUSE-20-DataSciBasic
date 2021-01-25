
x = [[5, 1], [4, 2], [3,3], [2,4], [1,5]]
x = sorted(x, key=lambda x:x[0])
y = [i[1] for i in x]
print(x)
print(y)