import numpy as np

x = np.array([4, 5])
y = np.array([2, 1])
u = np.array([1, 0])
k1, k2, k3 = 2, -3, 5

res = x * k1 + y * k2 + u * k3
print(res)

create = np.array([3, 4, 5, 9])
sell = np.array([1, 5, 3, 6])
x1, x2 = 200, 400
total = sell * x2 - create * x1
print(total)

