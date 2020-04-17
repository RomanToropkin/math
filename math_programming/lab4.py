import numpy as np
import pandas as pd

# Полноценный класс методов мат. программирования, включающий в себя симплекс метод, двойственный метод и метод Гомори
class Gomori:

    def __init__(self, A, b, c, sign, isMin):
        self.A = A
        self.b = b
        self.c = c
        self.sign = sign
        self.isMin = isMin
        self.table = None
        self._index_arr = []
        self._column_arr = []
        self.res = None
        self._build_table()

    # Построение симплекс таблицы
    def _build_table(self):
        size = np.shape(self.A)
        dop_basis_length = 0
        for s in self.sign:
            if s != '=':
                dop_basis_length += 1

        if dop_basis_length != 0:
            new_A = np.concatenate((self.A, np.eye(dop_basis_length)), axis=1)
            for i in range(0, len(self.sign)):
                if self.sign[i] == '>=':
                    new_A[i] = np.dot(new_A[i], -1)
                    new_A[i][len(new_A[i]) - size[0] + i] = 1
                    self.b[i] = -self.b[i]
            new_C = np.concatenate((-self.c, np.zeros((1, dop_basis_length))[0]))
        else:
            new_A = self.A
            new_C = - self.c

        b_u = np.concatenate((self.b, [0])).reshape((len(self.b) + 1, 1))
        for i in range(0, size[0]):
            self._index_arr.append(f'x{len(new_A[0]) - size[0] + i + 1}')
        self._index_arr.append('Z')
        for i in range(0, len(new_A[0])):
            self._column_arr.append(f'x{i + 1}')
        self._column_arr.append('b')
        table = np.vstack((new_A, new_C))
        table = np.hstack((table, b_u))
        self.table = pd.DataFrame(data=table, index=self._index_arr, columns=self._column_arr)
        self.res = [0 for i in range(0, len(self._column_arr) - 1)]

    # Выбор метода
    # Истина - обычный симплекс метод
    # Ложь - двойственный
    def _check_method(self):
        last_сolumn = self.table.shape[1] - 1
        if min(self.table.values[:-1, last_сolumn]) >= 0:
            return True
        else:
            return False

    # Проверка на разрешимость двойственного метода
    # Истина - есть решения
    # Ложь - нет решения
    def _check_double_sol(self):
        lastColumn = self.table.shape[1] - 1
        b = self.table.values[:, lastColumn]
        for i in range(0, len(b)):
            if b[i] < 0:
                neg_count = len(list(filter(lambda x: (x < 0), self.table.values[i, :lastColumn])))
                if neg_count == 0:
                    return False
        return True

    # Проверка на разрешимость обычного симплекс метода
    # Истина - есть решения
    # Ложь - нет решения
    def _check_symplex_sol(self, p):
        count = 0
        size = self.table.values.shape
        for i in range(0, size[0]):
            if self.isMin:
                if self.table.values[i][p] >= 0:
                    count += 1
            else:
                if self.table.values[i][p] <= 0:
                    count += 1
        if count == size[0]:
            return False
        else:
            return True

    # Определение разрешающего стоблца для симплекс метода
    def _get_symplex_col(self, row):
        if self.isMin:
            value = -np.inf
        else:
            value = 0
        index = -1
        for i in range(0, len(row)):
            if self.isMin:
                if row[i] > value:
                    index = i
                    value = row[i]
            else:
                if row[i] < value:
                    index = i
                    value = row[i]
        return index

    # Определение разрешающей строки для симплекс метода
    def _get_symplex_row(self, p):
        mini = np.inf
        min_index = -1
        size = self.table.values.shape
        for i in range(0, size[0] - 1):
            if self.table.values[i][p] > 0:
                s = self.table.values[i][size[1] - 1] / self.table.values[i][p]
                if s < mini:
                    mini = s
                    min_index = i
        return min_index

    # Определение разрешающей строки для двойственного метода
    def _get_double_row(self):
        lastColumn = self.table.shape[1] - 1
        b = self.table.values[:, lastColumn]
        index = 0
        val = 0
        for i in range(0, len(b)):
            if b[i] < 0:
                if abs(b[i]) > val:
                    val = abs(b[i])
                    index = i
        return index

    # Определенеи разрещаюшего столбца для двойственного метода
    def _get_double_col(self, q):
        z_index = self.table.shape[0] - 1
        length = self.table.shape[1] - 1
        d = [np.inf for i in range(0, length)]
        for j in range(0, length):
            if self.table.values[q, j] < 0:
                d[j] = abs(self.table.values[z_index, j] / self.table.values[q, j])
        return np.flatnonzero(d == np.min(d))[0]

    # Пересчет таблицы по правилам симплекс метода
    def _calculate(self, q, p):
        qp = self.table.values[q][p]
        size = self.table.values.shape
        for j in range(0, size[1] - 1):
            self.table.values[q][j] = np.around(self.table.values[q][j] / qp, decimals=5)
        self.table.values[q][size[1] - 1] = np.around(self.table.values[q][size[1] - 1] / qp, decimals=5)
        for i in range(0, size[0]):
            if i != q:
                ip = -self.table.values[i][p]
                for j in range(0, size[1] - 1):
                    self.table.values[i][j] = np.around(self.table.values[i][j] + self.table.values[q][j] * ip,
                                                        decimals=5)
                self.table.values[i][size[1] - 1] = np.around(self.table.values[i][size[1] - 1] + self.table.values[q][
                    size[1] - 1] * ip, decimals=5)

    # Решения задачи ЛП симплекс методом
    def _symplex_solve(self):
        size = self.table.shape
        row = self.table.values[size[0] - 1]
        p = self._get_symplex_col(row)
        if p == -1:
            return 0
        if self._check_symplex_sol(p):
            q = self._get_symplex_row(p)
            self._calculate(q, p)
        else:
            return -1
        self._new_basis(p, q)
        return 1

    # Решения задачи ЛП двойственным методом
    def _double_solve(self):
        if self._check_double_sol():
            q = self._get_double_row()
            p = self._get_double_col(q)
            self._calculate(q, p)
            self._new_basis(p, q)
            return 1
        else:
            return -1

    # Проверка целочисленности оптимального решения
    # Возвращает индекс строки с наибольшой дробной частью или -1, если решение уже целочисленное
    def _check_int(self):
        lastColumn = self.table.shape[1] - 1
        b = self.table.values[:-1, lastColumn]
        self._dop = [0 for i in range(len(b))]
        for i in range(0, len(b)):
            self._dop[i] = b[i] - np.floor(b[i])
        index = np.flatnonzero(self._dop == np.max(self._dop))[0]
        if self._dop[index] == 0.0:
            return -1
        else:
            return index

    # Построение нового базиса
    def _new_basis(self, p, q):
        self._index_arr[q] = self._column_arr[p]
        self.table = pd.DataFrame(data=self.table.values, index=self._index_arr, columns=self._column_arr)

    # Поиск оптимального решения
    def _find_optimal_solve(self):
        while True:
            if self._check_method():
                flag = self._symplex_solve()
            else:
                flag = self._double_solve()
            if flag == -1:
                print('Решения нет')
                return False
            elif flag == 0:
                print('Решение найдено')
                break
            print(self.table)

        for i in range(0, len(self.res)):
            col = 'x' + str(i + 1)
            if col in self.table.index.values:
                self.res[i] = self.table['b'][col]
        print(self.res)

        return True

    # Поиск целочисленного решения
    def _int_solve(self):
        size = self.table.shape
        q = self._check_int()
        if q == -1:
            return 0

        row = self.table.values[q, :]
        row = list(map(lambda x: (x - np.floor(x)) * -1, row))
        row.append(1)
        row[-1], row[-2] = row[-2], row[-1]

        new_x_col = np.zeros((size[0], 1))
        new_x = 'x' + str(size[1])
        self.table[new_x] = new_x_col
        cols = list(self.table.columns)
        a, b = cols.index(new_x), cols.index('b')
        cols[b], cols[a] = cols[a], cols[b]
        self.table = self.table[cols]
        self.table.loc[new_x] = row
        self.table.loc[new_x], self.table.loc['Z'] = self.table.loc['Z'], row

        self._index_arr.append(new_x)
        self._index_arr[-1], self._index_arr[-2] = self._index_arr[-2], self._index_arr[-1]
        self.table.set_axis(self._index_arr, axis=0, inplace=True)

        self._column_arr = self.table.columns.values
        self.res = [0 for i in range(0, len(self._column_arr) - 1)]

        print(self.table)
        return 1

    # Поиск решения
    def solve(self):
        print('Исходная таблица')
        print(self.table)

        flag = self._find_optimal_solve()
        while True:
            if flag:
                flag_2 = self._int_solve()
                if flag_2 == 1:
                    flag = self._find_optimal_solve()
                elif flag_2 == 0:
                    print('Найдено целочисленное решение')
                    self.res.append(self.table['b']['Z'])
                    self._column_arr[-1] = 'Z'
                    print(pd.DataFrame(data=[self.res], columns=self._column_arr))
                    break
                else:
                    print('Решения нет')
                    break
            else:
                print('Решения нет')
                break


A = np.array([[3,2,1],
              [1,4,1],
              [3,3,1]])
b = np.array([10,11,13])
c = np.array([4,5,1])
sign = ['<=','<=','<=']

gomori = Gomori(A, b, c, sign, False)
gomori.solve()