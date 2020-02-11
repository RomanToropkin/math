import sympy as sym

x1, x2 = sym.symbols('x1 x2')
f = ['sin(0.5 * x1 + x2) - 1.2 * x1 - 1', 'x1 ^ 2 + x2 ^ 2 - 1']
eps = 1e-6

#Вывод графика
def DrawGraphic():
    curve1 = sym.plot_implicit(sym.Eq(sym.sin(0.5 * x1 + x2) - 1.2 * x1 - 1, 0))
    curve2 = sym.plot_implicit(sym.Eq(x1 ** 2 + x2 ** 2 - 1, 0))
    curve1.extend(curve2)
    curve1.show()

#Построение матрицы Якоби
def Jacobian(f, x1zero, x2zero):
    vars = sym.symbols('x1 x2')
    J = sym.zeros(len(f), len(vars))
    for i, fi in enumerate(f):
        for j, s in enumerate(vars):
            J[i, j] = sym.diff(fi, s)
    return J.subs({x1: x1zero, x2: x2zero})

#Метод простых итераций
def MPI():
    X = sym.Matrix([zx1, zx2])
    J = Jacobian(F, X[0], X[1]).inv()
    flag = True
    iter = 0
    while flag:
        iter += 1
        X_old = X.copy()
        X = X_old - J * F.subs({x1: X_old[0], x2: X_old[1]})
        if abs(sum(X - X_old)) <= eps:
            flag = False
    print(f'Кол-во итераций: {iter}')
    return X.evalf(6)

#Метод ньютона
def Newton():
    X = sym.Matrix([zx1, zx2])
    flag = True
    iter = 0
    while flag:
        iter += 1
        X_old = X.copy()
        X = X_old - Jacobian(F, X_old[0], X_old[1]).inv() * F.subs({x1: X_old[0], x2: X_old[1]})
        if abs(sum(X - X_old)) <= eps:
            flag = False
    print(f'Кол-во итераций: {iter}')
    return X.evalf(6)

#Метод браума
def Braum():
    X = sym.Matrix([zx1, zx2])
    f = sym.sin(0.5 * x1 +x2) - 1.2 * x1 - 1
    g = x1 ** 2 + x2 ** 2 - 1
    flag = True
    iter = 0
    while flag:
        iter += 1
        rX = X[0] - f.subs({x1: X[0], x2: X[1]}) / sym.diff(f, x1).subs({x1: X[0], x2: X[1]})
        q = g.subs({x1: rX, x2: X[1]}) * sym.diff(f, x1).subs({x1: X[0], x2: X[1]}) / (sym.diff(f, x1).subs(
            {x1: X[0], x2: X[1]}) * sym.diff(g, x2).subs({x1: rX, x2: X[1]}) - sym.diff(f, x2).subs({x1: X[0], x2: X[1]}) *
                                                                                       sym.diff(g,x1).subs({x1: rX, x2: X[1]}))
        p = (f.subs({x1: X[0], x2: X[1]}) - q * sym.diff(f, x2).subs({x1: X[0], x2: X[1]})) / sym.diff(f, x1).subs(
            {x1: X[0], x2: X[1]})
        X[0] = X[0] - p
        X[1] = X[1] - q
        if max(abs(p), abs(q)) < eps:
            flag = False
    print(f'Кол-во итераций: {iter:}')
    return X.evalf(6)

#Метод наискорейшего спуска
def Fast_Down():
    X = sym.Matrix([zx1,zx2])
    flag = True
    iter = 0
    while flag:
        iter+=1
        J = Jacobian(F,X[0],X[1])
        fK = F.subs({x1:X[0], x2:X[1]})
        l1 = fK.dot(J * J.transpose() * fK)
        l2 = (J * J.transpose() * fK).dot(J * J.transpose() * fK)
        mu = l1/l2
        X = X - mu * J.transpose() * fK
        if sum(abs(F.subs({x1:X[0], x2:X[1]}))) <= eps:
            flag = False
    print(f'Кол-во итераций: {iter}')
    return X.evalf(6)

#Встроенная функция
def Internal():
    return sym.nsolve((sym.sin(0.5 * x1 + x2) - 1.2 * x1 - 1, x1 ** 2 + x2 ** 2 - 1), (x1, x2), (zx1, zx2)).evalf(6)

#Начальное приближение
DrawGraphic()
zx1 = -0.4
zx2 = 1
F = sym.Matrix(sym.sympify(f))
print(f'Встроенная: {Internal()}')
print(f'МПИ: {MPI()}')
print(f'Ньютон: {Newton()}')
print(f'Браум: {Braum()}')
print(f'МНС: {Fast_Down()}')
