import numpy as np
import pandas as pd
from scipy.optimize import linprog

np.set_printoptions(precision=3, suppress=True)

def simplex(A_u, b_u, sign, c):
    x_solution = [0 for i in range(0, len(c))]
    sol_index = []
    index_arr = []
    columns_arr = []
    sign_map_minus = {'>=', '>'}
    for i in range(0, len(b_u) + len(c)):
        columns_arr.append('x' + str(i + 1))
        if i < len(c):
            sol_index.append('x' + str(i + 1))
    for i in range(len(b_u) + 1, len(b_u) * 2 + 1):
        index_arr.append('x' + str(i + 1))
    index_arr.append('Z')

    columns_arr.append('b')
    sol_index.append('Z')

    basis = np.eye(len(b_u), dtype='float64')
    for i in range(0, len(b_u)):
        if sign[i] in sign_map_minus:
            basis[i][i] = -1

    b_u_T = []
    for b in b_u:
        b_u_T.append([b])
    b_u_T = np.array(b_u_T)
    simplex_table = np.hstack([A_u, basis])
    simplex_table = np.hstack([simplex_table, b_u_T])
    Z_row = np.append(-c, np.zeros((1, len(b_u) + 1)))
    simplex_table = np.vstack([simplex_table, Z_row])
    df = pd.DataFrame(data=simplex_table, index=index_arr, columns=columns_arr)

    iter_count = 0
    last_index = np.shape(simplex_table)[0] - 1

    # Проверка текущего допустимого базисного решения на оптимальность.
    # Сразу же определяем разрешающий столбец
    permitting_column = find_permitting_column(simplex_table[last_index])

    # Определение разрешающей строки
    permitting_row = find_permitting_row(simplex_table, permitting_column)
    print(f'{iter_count} итерация ')
    print(df)
    print(f'Резрешающая строка: {permitting_row + 1}, Резрешающий столбец {permitting_column + 1}')

    # Проверка признака неогранниченности Z
    isSolution = check_solution(simplex_table, permitting_column)
    print(f'Существует решение - {isSolution}', '', sep='\n')
    index_arr[permitting_row] = columns_arr[permitting_column]

    # Переход к новому базису
    while permitting_column != -1 and isSolution:
        iter_count += 1
        print(f'{iter_count} итерация ')
        simplex_table = calculate(simplex_table, permitting_column, permitting_row)
        df = pd.DataFrame(data=simplex_table, index=index_arr, columns=columns_arr)
        print(df)
        permitting_column = find_permitting_column(simplex_table[last_index])
        permitting_row = find_permitting_row(simplex_table, permitting_column)
        print(f'Резрешающая строка: {permitting_row + 1}, Резрешающий столбец {permitting_column + 1}')
        isSolution = check_solution(simplex_table, permitting_column)
        print(f'Существует решение - {isSolution}', '', sep='\n')
        index_arr[permitting_row] = columns_arr[permitting_column]

    for i in range(0, len(c)):
        col = 'x' + str(i + 1)
        if col in df.index.values:
            x_solution[i] = df['b'][col]
    x_solution.append(df['b']['Z'])
    df = pd.DataFrame(data=[x_solution], columns=sol_index)
    print(df)

def find_permitting_column(row):
    mini = 0
    min_index = -1
    for i in range(0, len(row)):
        if row[i] < mini:
            min_index = i
            mini = row[i]
    return min_index

def find_permitting_row(table, p):
    mini = np.inf
    min_index = -1
    size = np.shape(table)
    for i in range(0, size[0] - 1):
        if table[i][p] > 0:
            s = table[i][size[1] - 1] / table[i][p]
            if s < mini:
                mini = s
                min_index = i
    return min_index


def calculate(table, p, q):
    size = np.shape(table)
    qp = table[q][p]
    for j in range(0, size[1] - 1):
        table[q][j] = table[q][j] / qp
    table[q][size[1] - 1] = table[q][size[1] - 1] / qp
    for i in range(0, size[0]):
        if i != q:
            ip = -table[i][p]
            for j in range(0, size[1] - 2):
                table[i][j] = table[i][j] + table[q][j] * ip
            table[i][size[1] - 1] = table[i][size[1] - 1] + table[q][size[1] - 1] * ip
    return table


def check_solution(table, p):
    count = 0
    size = np.shape(table)
    for i in range(0, size[0]):
        if table[i][p] <= 0:
            count += 1
    if count == size[0]:
        return False
    else:
        return True


A_u = np.array([[1, 2, 4, 0],
                [3, 5, 1, 0],
                [6, 0, 3, 0]])
b_u = np.array([24, 12, 35])
sign = ['<=', '<=', '<=', '<=']
c = np.array([4, 2, 5, 8])

# simplex(A_u, b_u, sign, c)
# inner_solution = linprog(-c, A_u, b_u, method='simplex')
# print(f'Минимальное значение x: {inner_solution.x}\nОптимальное решение: {-inner_solution.fun}')
