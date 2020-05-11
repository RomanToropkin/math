from sympy import *
import math

x, y = symbols('x y')

f = diff(ln(x))

f1 = diff(x  ** 0.25)
print(0.25 * 1 ** (-0.75))

print(diff(3 * x + 5))

print(diff((5 + 2 * x) ** 2))

print(1 / (1 + math.e ** -4))

func = lambda x1,x2,x3: 1 / (1 + math.e ** (-2 * (x1 + x2 + x3)))
print(func(0.1,0.3,0.6))
