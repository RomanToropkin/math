import numpy as np
import pandas as pd

Hut_Paradise_DF = pd.DataFrame({'1.Rent': [65, 70, 120, 35, 40, 50, 100, 90, 85],
                                '2.Area': [50, 52, 80, 33, 33, 44, 80, 65, 65],
                                '3.Rooms':[3, 2, 1, 1, 1, 2, 4, 3, 2],
                                '4.Floor':[5, 12, 10, 3, 6, 13, 8, 21, 5],
                                '5.Demo two weeks':[8, 4, 5, 10, 20, 12, 5, 1, 10],
                                '6.Liv.Area': [37, 40, 65, 20, 16, 35, 60, 50, 40]})

x = Hut_Paradise_DF.values
print(x[4])
print(x[2,3])
print(len(x))
print(x[:,1] - x[:,5])

K = 0.4
print(x[:,0] * K)

time = np.array([10,20,30,15,5,40,20,8,20])
print(sum(time * x[:,4]))

u=np.array([3,0,1,1,1])
v=np.array([0,1,0,2,-2])
w=np.array([1,-4,-1,0,-2])

print('u-v',u@v)
print('u-w',u@w)
print('v-w',v@w)

comp = v*2 + w * -3
print(comp)
print(comp@u)

norm_u = u / np.linalg.norm(u)
norm_v = v / np.linalg.norm(v)
norm_w = w / np.linalg.norm(w)
print(norm_u, norm_v, norm_w)
