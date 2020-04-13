import numpy as np

A = np.array([[1,-1,2,4,0],
              [8,2,0,5,3],
              [0,1,2,1,2]])

B = np.array([[1,0,1,0],
              [0,0,2,-1],
              [1,0,1,1],
              [0,1,1,1],
              [1,1,0,-1]])

C = np.dot(A,B)
print(C)

X = np.array([[1,1],[2,-1],[1,2]])
print(X.dot(X.T))