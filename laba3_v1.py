import math
import pylab
import numpy
E = 1e-2
f = lambda x: x + math.exp(x)
a = -5
b = 5

def DrawGraphic(n):
    plots = numpy.linspace(a, b, n)
    values = [f(x) for x in plots]
    pylab.plot(plots, values)
    pylab.grid(linewidth=2, linestyle='-')
    pylab.show()

DrawGraphic(100)

a = - 2
b = 0

print(f'Отрезок локализации по методу графической локализации = [{a}; {b}]')
middle = b
while b - a > 2*E:
    middle = (a + b) / 2
    print(f'Интервал = [{a:.2f}; {b:.2f}], middle = {middle:.2f}, f(middle) = {f(middle):.2f}, f(a) = {f(a):.2f}, f(b) = {f(b):.2f}')
    if f(a) * f(middle) < 0:
        b = middle
    else:
        a = middle
print(f'Ответ: x = {middle:.2f}')
