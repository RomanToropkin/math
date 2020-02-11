import math
import pylab
import numpy
from scipy.misc import derivative
from sympy import *

E = 1e-4 # Сигма
a = 2  # Левая граница
b = 10  # Правая граница

f = lambda x: x**3+x**2-15*x-14 # Исходная функция


# Отображение графика
def DrawGraphic(n):
    plots = numpy.linspace(a, b, n)
    values = [f(x) for x in plots]
    pylab.plot(plots, values)
    pylab.plot([0, 1, 2], [0, 0, 0], color='k',)
    pylab.plot([0, 0, 0, 0], [2, 1, -1, -2], color='k')
    pylab.grid(linewidth=2, linestyle='-')
    pylab.show()


# Локализация корней уравнений
# dots - кол-во знаков после запятой
def Localize(dots) -> list:
    sigma = 1 * 10 ** -dots
    otresok = numpy.arange(a, b, sigma)
    L = []
    for i in range(len(otresok) - 1):
        if f(otresok[i]) * f(otresok[i + 1]) <= 0:
            L.append([round(otresok[i], dots), round(otresok[i + 1], dots)])
    return L


# Метод дихотомии
# а - левая граница, b - правая
def Half_Division(a, b):
    k = -1
    middle = b
    while b - a > 2 * E:
        middle = (a + b) / 2
        k += 1
        if (f(middle) * f(a)) < 0:
            b = middle
        else:
            a = middle
    print(f"k = {k}, x = {middle:.9f}, f(x) = {abs(f(middle)):.11f} интервал: [{a:.11f}; {b:.11f}]")


# Метод хорд
# а - левая граница, b - правая
def Hourda(a, b):
    formula = lambda a, b: a - (b - a) / (f(b) - f(a)) * f(a)
    xCurrect = a
    k = 0
    while abs(f(xCurrect)) > E:
        k += 1
        xCurrect = formula(a, b)
        if (f(a) * f(xCurrect)) < 0:
            b = xCurrect
        else:
            a = xCurrect
    print(f"k = {k}, x = {xCurrect:.9f}, f(x) = {abs(f(xCurrect)):.16f} интервал: [{a:.11f}; {b:.11f}]")


# Поиск максимума функции
def Find_Max():
    x = symbols('x')
    g = x*(x-1)*(x-3)*(x-5)
    fprime = g.diff(x)
    maxs = solve(fprime, x)
    M = maxs[0]
    for i in maxs:
        if f(i) > M:
            M = i
    return f(M)


# Метод простых итераций
# а - левая граница, b - правая
def MPI(a, b):
    M = Find_Max()
    xCurrect = a
    xLast = b
    if (derivative(f, a, dx=E) and derivative(f, b, dx=E)) < 0:
        g = lambda x: -f(x)
    else:
        g = lambda x: f(x)
    fi = lambda x: x - 1 / M * g(x)
    dK = abs(xCurrect - xLast)
    k = 0
    while dK > E:
        k += 1
        xLast = xCurrect
        xCurrect = fi(xLast)
        dK = abs(xCurrect - xLast)
    print(f"k = {k}, x = {xCurrect:.9f}, dk = {dK:.11f}")


# Метод Ньютона
# а - левая граница, b - правая
def Newton(a, b):
    if f(a) * f(b) < 0:
        if (f(a) * derivative(f, b, dx=E)) > 0:
            x0 = a
        else:
            x0 = b
        iter = lambda x: x - f(x) / derivative(f, x, dx=E)
        k = 0
        xLast = 0
        while abs(x0 - xLast) > E:
            k += 1
            xLast = x0
            x0 = iter(xLast)
        print(f'k = {k}, x = {x0:.9f}, dK = {(x0 - xLast):.15f}')
    else:
        print('Не выполняется условие монотонности!')


# Метод Чебышева 3-го порядка
# а - левая граница, b - правая
def Chebyshev(a, b):
    x0 = a
    iter = lambda x: x - f(x) / derivative(f, x,dx=E) - derivative(f, x,n=2) * f(x) ** 2 / derivative(f, x,dx=E) ** 3 * 2
    k = 0
    dk = 1
    while abs(dk) > E:
        k += 1
        xLast = x0
        x0 = iter(xLast)
        dk = abs(x0 - xLast)
    print(f'k = {k}, x = {x0:.9f}, dK = {dk:.16f}')


# Встроенная реализация поиска корней
def InternalSolve():
    x = symbols('x', real=True)
    f = 4*x**3 - 27 * x**2 + 46*x - 15
    ans = solve(f, x)
    print(f'Встроенные корни уравнений: {ans}')


DrawGraphic(100)
L = Localize(1)
print("Метод дихотомии")
for o in L:
    print(f'Отрезок: [{o[0]}; {o[1]}]')
    Half_Division(o[0], o[1])
print("Метод хорд")
for o in L:
    print(f'Отрезок: [{o[0]}; {o[1]}]')
    Hourda(o[0], o[1])
# print("Метод простых итераций")
# for o in L:
#     print(f'Отрезок: [{o[0]}; {o[1]}]')
#     MPI(o[0], o[1])
# print("Метод касательных")
# for o in L:
#     print(f'Отрезок: [{o[0]}; {o[1]}]')
#     Newton(o[0], o[1])
# print("Метод Чебышева")
# for o in L:
#     print(f'Отрезок: [{o[0]}; {o[1]}]')
#     Chebyshev(o[0], o[1])
#InternalSolve()
