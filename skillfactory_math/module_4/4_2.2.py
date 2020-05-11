from sympy import *

a, b, c, w = symbols('a b c w')

Z = 2 * (a * b + b * c + a * c)
print(Z)
q = a * b * c - 1
print(q)
f = Z + w * q
print(f)
fa = f.diff(a)
print(fa)
fb = f.diff(b)
print(fb)
fc = f.diff(c)
print(fc)
fw = f.diff(w)
print(fc)

sols = solve([fa, fb, fc, fw], a, b, c, w)
print(sols)
print(2 * (sols[0][0] * sols[0][1] + sols[0][1] * sols[0][2] + sols[0][0] * sols[0][2]))
