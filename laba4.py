import numpy as np


# Прямой ход метода Гаусса
def FirstStep(A, B):
    m = lambda k, i: A[i][k] / A[k][k]
    a = lambda i, j, k: A[i][j] - m(k, i) * A[k][j]
    b = lambda i, j: B[i][0] - m(j, i) * B[j][0]
    n = len(A)
    for k in range(0, n - 1):
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = a(i, j, k)
            B[i][0] = b(i, k)
        for i in range(k + 1, n):
            A[i][k] = 0


# Обратный ход метода Гаусса
def LastStep(A, B):
    n = len(A)
    R = np.zeros((n, 1), dtype=float)
    R[n - 1] = B[n - 1][0] / A[n - 1][n - 1]
    for i in range(1, n):
        k = n - i - 1
        left = 1 / A[k][k]
        right = B[k]
        for j in range(1, i + 1):
            right -= A[k][k + j] * R[k + j]
        R[k] = left * right
    print(f'Число операций: {round(2 / 3 * n ** 3 + n ** 2)}')
    return R


# Метода Гаусса
def Gauss(A, B):
    FirstStep(A, B)
    R = LastStep(A, B)
    return R


# Метод Зейделя
def Zeidel(A, B, eps):
    n = len(A)
    q = np.random.uniform(-1e-6, 1e-6, (n, n))
    np.fill_diagonal(q, 1)
    q = A.transpose().dot(q)
    A = q.dot(A)
    B = q.dot(B)
    x = np.zeros((n, 1))
    converge = False
    k = 0
    count = 0
    while not converge:
        x_new = np.copy(x)
        for i in range(n):
            s1 = sum(A[i][j] * x_new[j][0] for j in range(i))
            count += i
            s2 = sum(A[i][j] * x[j][0] for j in range(i + 1, n))
            count += n - i - 1
            x_new[i][0] = (B[i] - s1 - s2) / A[i][i]
            count += 3
        k += 1
        converge = abs(sum((x_new[i][0] - x[i][0]) for i in range(n))) <= eps
        x = x_new
    print(f'Число итераций: {k}')
    print(f'Число операций: {count}')
    return x


np.set_printoptions(precision=30)
A = np.array([[0,0,0,0,0,0],
              [0,0,0,0,0,0],
              [0,0,0,0,0,0],
              [0,0,0,0,0,0],
              [0,0,0,0,0,0],
              [0,0,0,0,0,0]],
             dtype=float)
B = np.array([[12], [-12-36],[],[],[],[]], dtype=float)
eps = 1e-10
print(f'Исходная матрица A:\n{A}')
print(f'Исходная матрца b:\n{B}')
print('Метод Гауса')
x1 = Gauss(A.copy(), B.copy())
print(f'Результат:\n{x1}')
print('Зейдель')
x3 = Zeidel(A, B, eps)
print(f'Результат:\n{x3}')
print('Встроенная функция:')
x2 = np.linalg.solve(A, B)
print(f'Результат:\n{x2}')
print(f'Погрешность Гаусса:{max(abs(x2 - x1))}')
print(f'Погрешность Зейделя:{max(abs(x2 - x3))}')
