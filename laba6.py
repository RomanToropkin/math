from math import cos, pi, log1p, exp
from scipy.integrate import odeint
import numpy as np

t0 = 0
T = pi
y0 = 0.5
Eps = 1e-4
func = lambda y, t: -y + cos(t)
#func = lambda  y,t: 2*t-3*y

#Встроенное решение
def Internal():
    print('Встроенное решение')
    n = 100
    t = np.linspace(t0, T, n)
    Q = np.float64(odeint(func, y0, t)[n - 1])
    print(Q)
    return Q

#Метод Эйлера
def Eiler():
    print('Метод Эйлера')
    n = 2
    yLast = np.linspace(t0, T, n)
    while True:
        h = (T - t0) / n
        y = [0.0 for i in range(n)]
        y[0] = y0
        t = np.linspace(t0, T, n)
        for i in range(n - 1):
            y[i + 1] = y[i] + h * func(y[i], t[i])
        maxPogr = 0
        for i in range(1, int(n / 2)):
            maxPogr = max(maxPogr, abs(y[2 * i - 1] - yLast[i]))
        if maxPogr < Eps and maxPogr != 0:
            break
        n *= 2
        yLast = y
    print(f'Число узлов: {n}')
    print(f'Шаг между узлами {h}')
    print(f'{y[(len(y) - 1)]}')
    return y[len(y) - 1]

#Метод хойна
def Hoin():
    print('Метод Хойна')
    n = 2
    yLast = np.linspace(t0, T, n)
    while True:
        h = (T - t0) / n
        y = [0.0 for i in range(n)]
        y[0] = y0
        t = np.linspace(t0, T, n)
        for i in range(n - 1):
            y[i + 1] = y[i] + h * func(y[i], t[i])
            y[i + 1] = y[i] + h * func(y[i], t[i])
            y[i + 1] = y[i] + h / 2 * (func(y[i], t[i]) + func(y[i + 1], t[i + 1]))
        maxPogr = 0
        for i in range(1, int(n / 2)):
            maxPogr = max(maxPogr, abs(y[2 * i - 1] - yLast[i]))
        if 1 / 3 * maxPogr < Eps and maxPogr != 0:
            break
        n *= 2
        yLast = y
    print(f'Число узлов: {n}')
    print(f'Шаг между узлами {h}')
    print(f'{y[(len(y) - 1)]}')
    return y[len(y) - 1]

#Уточненный метод Эйлера
def Eiver_v2():
    print('Уточненный метод Эйлера')
    n = 2
    yLast = np.linspace(t0, T, n)
    while True:
        h = (T - t0) / n
        y = [0.0 for i in range(n)]
        t = np.linspace(t0, T, n)
        y[0] = y0
        y[1] = y[0] + h / 2 * func(y[0], t[0])
        y[1] = y[0] + h * func(y[1], t[0] + h / 2)
        for i in range(1, n - 1):
            y[i + 1] = y[i - 1] + 2 * h * func(y[i], t[i])
        maxPogr = 0
        for i in range(1, int(n / 2)):
            maxPogr = max(maxPogr, abs(y[2 * i - 1] - yLast[i]))
        if 1 / 3 * maxPogr < Eps and maxPogr != 0:
            break
        n *= 2
        yLast = y
    print(f'Число узлов: {n}')
    print(f'Шаг между узлами {h}')
    print(f'{y[(len(y) - 1)]}')
    return y[len(y) - 1]

#Метод Рунге-Кутта 4-ого порядка
def Runge_Kut():
    print('Метод Рунге-Кутта 4-ого порядка')
    n = 2
    yLast = np.linspace(t0, T, n)
    while True:
        h = (T - t0) / n
        y = [0.0 for i in range(n)]
        t = np.linspace(t0, T, n)
        y[0] = y0
        for i in range(n - 1):
            k1 = func(y[i], t[i])
            k2 = func(y[i] + h / 2 * k1, t[i] + h / 2)
            k3 = func(y[i] + h / 2 * k2, t[i] + h / 2)
            k4 = func(y[i] + h * k3, t[i] + h)
            y[i + 1] = y[i] + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        maxPogr = 0
        for i in range(1, int(n / 2)):
            maxPogr = max(maxPogr, abs(y[2 * i - 1] - yLast[i]))
        if 1 / 15 * maxPogr < Eps and maxPogr != 0:
            break
        n *= 2
        yLast = y
    print(f'Число узлов: {n}')
    print(f'Шаг между узлами {h}')
    print(f'{y[(len(y) - 1)]}')
    return y[len(y) - 1]

#Метод Адамса
def Adams():
    print('Метод Адамса')
    n = 4
    yLast = []
    while True:
        h = (T - t0) / n
        y = [0.0 for i in range(n)]
        t = np.linspace(t0, T, n)
        y[0] = y0
        for i in range(0, 3):
            k1 = func(y[i], t[i])
            k2 = func(y[i] + h / 2 * k1, t[i] + h / 2)
            k3 = func(y[i] + h / 2 * k2, t[i] + h / 2)
            k4 = func(y[i] + h * k3, t[i] + h)
            y[i + 1] = y[i] + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        maxPogr = 0
        for i in range(3, n - 1):
            f0 = func(y[i], t[i])
            f1 = func(y[i - 1], t[i - 1])
            f2 = func(y[i - 2], t[i - 2])
            f3 = func(y[i - 3], t[i - 3])
            df0 = f0
            df1 = f0 - f1
            df2 = f0 - 2 * f1 + f2
            df3 = f0 - 3 * f1 + 3 * f2 - f3
            y[i + 1] = y[i] + h * (df0 + 1 / 2 * df1 + 5 / 12 * df2 + 3 / 8 * df3)
        if n == 4:
            yLast = y
            n *= 2
            continue
        for i in range(1, int(n / 2)):
            maxPogr = max(maxPogr, abs(y[2 * i - 1] - yLast[i]))
        if 1 / 15 * maxPogr < Eps and maxPogr != 0:
            break
        n *= 2
        yLast = y
    print(f'Число узлов: {n}')
    print(f'Шаг между узлами {h}')
    print(f'{y[(len(y) - 1)]}')
    return y[len(y) - 1]

#Метод прогноза и коррекции
def PK(n):
    print('Метод прогноза и коррекции')
    yLast = [0.0 for i in range(n)]
    iter = 0
    while True:
        iter += 1
        h = (T - t0) / n
        y = [0.0 for i in range(n)]
        t = np.linspace(t0, T, n)
        y[0] = y0
        for i in range(0, 3):
            k1 = func(y[i], t[i])
            k2 = func(y[i] + h / 2 * k1, t[i] + h / 2)
            k3 = func(y[i] + h / 2 * k2, t[i] + h / 2)
            k4 = func(y[i] + h * k3, t[i] + h)
            y[i + 1] = y[i] + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        maxPogr = 0
        for i in range(3, n - 1):
            f0 = func(y[i], t[i])
            f1 = func(y[i - 1], t[i - 1])
            f2 = func(y[i - 2], t[i - 2])
            f3 = func(y[i - 3], t[i - 3])
            y[i + 1] = y[i] + h / 24 * (55 * f0 - 59 * f1 + 37 * f2 - 9 * f3)
            y[i + 1] = y[i] + h / 24 * (9 * func(y[i + 1], t[i + 1]) + 19 * f0 - 5 * f1 + f2)
        if n <= 4:
            yLast = y
            n *= 2
            continue
        for i in range(1, int(n / 2)):
            maxPogr = max(maxPogr, abs(y[2 * i - 1] - yLast[i]))
        if 1 / 15 * maxPogr < Eps and maxPogr != 0:
            break
        n *= 2
        yLast = y
    print(f'Число узлов: {n}')
    print(f'Шаг между узлами {h}')
    print(f'Кол-во итераций {iter}')
    print(f'{y[(len(y) - 1)]}')
    return y[len(y) - 1]


I = Internal()
E = Eiler()
print(f'Глобальная погрешность: {abs(I - E)}')
H = Hoin()
print(f'Глобальная погрешность: {abs(I - H)}')
E2 = Eiver_v2()
print(f'Глобальная погрешность: {abs(I - E2)}')
R = Runge_Kut()
print(f'Глобальная погрешность: {abs(I - R)}')
A = Adams()
print(f'Глобальная погрешность: {abs(I - A)}')
PK = PK(4)
print(f'Глобальная погрешность: {abs(I - PK)}')