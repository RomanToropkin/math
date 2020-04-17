import numpy as np
import pandas as pd


class DefaultSymplex:

    def __init__(self, A_u=None, b_u=None, c=None, sign=None, table=None,
                 index_arr=None, columns_arr = None, x_solution = None,
                 sol_index = None):
        super().__init__()
        self.table = table
        self.A_u = A_u
        self.b_u = b_u
        self.c = c
        self.sign = sign
        self._index_arr = index_arr
        self._columns_arr = columns_arr
        self._xSolution = x_solution
        self._solIndex = sol_index

    def solve(self):
        if self.table is None:
            self.table = self._buildTable()

        iter_count = 0
        last_index = np.shape(self.table)[0] - 1

        # Проверка текущего допустимого базисного решения на оптимальность.
        # Сразу же определяем разрешающий столбец
        permitting_column = self._find_permitting_column(self.table.values[last_index])

        # Определение разрешающей строки
        permitting_row = self._find_permitting_row(permitting_column)
        print(f'{iter_count} итерация ')
        print(self.table)
        print(f'Резрешающая строка: {permitting_row + 1}, Резрешающий столбец {permitting_column + 1}')

        # Проверка признака неогранниченности Z
        isSolution = self._check_solution(permitting_column)
        print(f'Существует решение - {isSolution}', '', sep='\n')
        self._index_arr[permitting_row] = self._columns_arr[permitting_column]

        # Переход к новому базису
        while permitting_column != -1 and isSolution:
            iter_count += 1
            print(f'{iter_count} итерация ')
            self._calculate(permitting_column, permitting_row)
            self.table = pd.DataFrame(data=self.table.values, index=self._index_arr, columns=self._columns_arr)
            print(self.table)
            permitting_column = self._find_permitting_column(self.table.values[last_index])
            permitting_row = self._find_permitting_row(permitting_column)
            print(f'Резрешающая строка: {permitting_row + 1}, Резрешающий столбец {permitting_column + 1}')
            isSolution = self._check_solution(permitting_column)
            print(f'Существует решение - {isSolution}', '', sep='\n')
            self._index_arr[permitting_row] = self._columns_arr[permitting_column]

        for i in range(0, len(self.table['b'])):
            col = 'x' + str(i + 1)
            if col in self.table.index.values:
                self._xSolution[i] = self.table['b'][col]
        self._xSolution.append(self.table['b']['Z'])
        self.result = pd.DataFrame(data=[self._xSolution], columns=self._solIndex)
        return self.result

    def _buildTable(self):
        sol_index = []
        index_arr = []
        columns_arr = []
        sign_map_minus = {'>=', '>'}
        for i in range(0, len(self.b_u) + len(self.c)):
            columns_arr.append('x' + str(i + 1))
            if i < len(self.c):
                sol_index.append('x' + str(i + 1))
        for i in range(len(self.b_u) + 1, len(self.b_u) * 2 + 1):
            index_arr.append('x' + str(i + 1))
        index_arr.append('Z')

        columns_arr.append('b')
        sol_index.append('Z')

        basis = np.eye(len(self.b_u), dtype='float64')
        for i in range(0, len(self.b_u)):
            if self.sign[i] in sign_map_minus:
                basis[i][i] = -1

        b_u_T = []
        for b in self.b_u:
            b_u_T.append([b])
        b_u_T = np.array(b_u_T)
        simplex_table = np.hstack([self.A_u, basis])
        simplex_table = np.hstack([simplex_table, b_u_T])
        Z_row = np.append(-self.c, np.zeros((1, len(self.b_u) + 1)))
        simplex_table = np.vstack([simplex_table, Z_row])
        self._index_arr = index_arr
        self._columns_arr = columns_arr
        self._xSolution = [0 for i in range(0, len(self.c))]
        self._solIndex = sol_index

        return pd.DataFrame(data=simplex_table, index=index_arr, columns=columns_arr)

    def _find_permitting_column(self, row):
        mini = 0
        min_index = -1
        for i in range(0, len(row)):
            if row[i] < mini:
                min_index = i
                mini = row[i]
        return min_index

    def _find_permitting_row(self, p):
        mini = np.inf
        min_index = -1
        size = np.shape(self.table)
        for i in range(0, size[0] - 1):
            if self.table.values[i][p] > 0:
                s = self.table.values[i][size[1] - 1] / self.table.values[i][p]
                if s < mini:
                    mini = s
                    min_index = i
        return min_index

    def _calculate(self, p, q):
        size = np.shape(self.table)
        qp = self.table.values[q][p]
        for j in range(0, size[1] - 1):
            self.table.values[q][j] = self.table.values[q][j] / qp
        self.table.values[q][size[1] - 1] = self.table.values[q][size[1] - 1] / qp
        for i in range(0, size[0]):
            if i != q:
                ip = -self.table.values[i][p]
                for j in range(0, size[1] - 2):
                    self.table.values[i][j] = self.table.values[i][j] + self.table.values[q][j] * ip
                self.table.values[i][size[1] - 1] = self.table.values[i][size[1] - 1] + self.table.values[q][
                    size[1] - 1] * ip

    def _check_solution(self, p):
        count = 0
        size = np.shape(self.table)
        for i in range(0, size[0]):
            if self.table.values[i][p] <= 0:
                count += 1
        if count == size[0]:
            return False
        else:
            return True

# A_u = np.array([[2,-1,1],
#                 [-4,2,-1],
#                 [3,0,1]])
# b_u = np.array([1,2,5])
# sign = ['<=', '<=', '<=']
# c = np.array([-1,1,3])
#
# s = Symplex(A_u, b_u, c, sign)
# res = s.solve()
# print(res)