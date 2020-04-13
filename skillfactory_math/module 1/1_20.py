import numpy as np

A = np.array([[8, 6, 11], [7, 5, 9],[6, 10, 6]])
inv_A = np.linalg.inv(A)
print(inv_A)

v1 = np.array([9, 10, 7, 7, 9])
v2 = np.array([2, 0, 5, 1, 4])
v3 = np.array([4, 0, 0, 4, 1])
v4 = np.array([3, -4, 3, -1, -4])

V = np.array([v1,v2,v3,v4])
print(np.linalg.matrix_rank(V))
G = V@V.T
print(G)
print(np.linalg.det(G))
print(np.linalg.matrix_rank(G))
print(np.linalg.inv(G))