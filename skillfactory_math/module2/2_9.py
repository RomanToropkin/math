import numpy as np
from sklearn import preprocessing

x = np.array([11,8])
x_c = np.mean(x)
x = x - x_c
print(x)
d = np.linalg.norm(x)
x = x / d
print(x)

x = np.array([120,9,6,45,89])
X_scale = preprocessing.scale(x)
print(X_scale)
