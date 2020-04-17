import numpy as np

A = np.array([[1,2],
              [-3,1],
              [1,2],
              [1,-1]])
b = np.array([1,4,5,0])

g = np.linalg.inv(A.T.dot(A))
Ab = A.T.dot(b)
print(g)
print(Ab)

w = g@Ab
print(w)