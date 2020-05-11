import numpy as np

f = np.array([1,2,4,7,11,16])

grad = np.gradient(f)
print(grad)

G = [
    lambda a,b: 2 * (a + 2 * b - 5),
    lambda a,b: 4 * (a + 2 * b - 5)
]

grad_1 = np.array([G[0](1,1),G[1](1,1)])
print(grad_1)

f = np.array([8, 2, 8, 3, 5, 6, 5, 15])
grad = np.gradient(f, 7)
print(grad)