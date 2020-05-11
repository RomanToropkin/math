from sympy import *
import math

x,y,w = symbols('x y w')
Z = pow((2 * x + y - 1) / sqrt(5),2)
print(Z)
q = x + y - 1
print(q)
f = Z + w * q
print(f)
fx = f.diff(x)
print(fx)
fy = f.diff(y)
print(fy)
fw = f.diff(w)
print(fw)

sols = solve([fx,fy,fw],x,y,w)
print(sols)
print()
