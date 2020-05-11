from sympy import *
import math

S_tr = 0.433
alpha = 0.8660254038

x1,x2,x3,x4,x5,w = symbols('x1 x2 x3 x4 x5 w')
Z = - x1 * x2 * alpha
q = x1 * x2 * alpha - 0.433 + x3 ** 2
f = Z + w * q
print(f)
fx1 = f.diff(x1)
fx2 = f.diff(x2)
fx3 = f.diff(x3)
fw = f.diff(w)
print(fx1, fx2,fx3, fw, sep='\n')
sols = solve([fx1, fx2, fx3, fw], x1,x2,x3, w)
print(sols)