import numpy as np

A = np.array([[1,2],[2,1]])
A_inv = np.linalg.inv(A)
print(A_inv)

A = np.array([[2,0,0],[0,1,0],[0,0,4]])
det_A = np.linalg.det(A)
det_inv_A = np.linalg.det(np.linalg.inv(A))
print(det_inv_A)