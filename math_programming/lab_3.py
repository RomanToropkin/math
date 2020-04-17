import numpy as np
import pandas as pd


class Solve:

    def __init__(self, A, b, c, sign, isMin):
        self.A = A
        self.b = b
        self.c = c
        self.sign = sign
        self.isMin = isMin
        self._build_table()

    def _build_table(self):
        size = np.shape(self.A)
        c_length = len(self.c)
        self.sol_index = []
        self.index_arr = []
        self.columns_arr = []
        self.x_solution = [0 for i in range(0, c_length)]

        new_A = np.concatenate((self.A, np.eye((size[0]))), axis=1)
        for i in range(0, len(self.sign)):
            if self.sign[i] == '>=':
                new_A[i] = np.dot(new_A[i], -1)
                new_A[i][len(new_A[i]) - size[0] + i] = 1
                self.b[i] = -self.b[i]
        c = np.concatenate((-self.c, np.zeros((1, size[0]))[0]))
        b_u = np.concatenate((self.b, [0])).reshape((len(self.b) + 1, 1))

        for i in range(0, size[0]):
            self.index_arr.append(f'x{len(new_A[0]) - size[0] + i + 1}')
        self.index_arr.append('Z')
        for i in range(0, len(new_A[0])):
            self.columns_arr.append(f'x{i + 1}')
            if i < c_length:
                self.sol_index.append(f'x{i + 1}')
        self.columns_arr.append('b')

        table = np.vstack((new_A, c))
        table = np.hstack((table, b_u))
        self.table = pd.DataFrame(data=table, index=self.index_arr, columns=self.columns_arr)
        self.sol_index.append('Z')


A_u = np.array([[1, 1, -1], # Система ограничений
                [1, -5, 1]])
b_u = np.array([4,5]) # Свободные члены
sign = ['<=', '>='] # Знаки неравенства ограничений
c = np.array([2, -1, -5]) # Коэффициенты целевой функции
isMin = False
s = Solve(A_u, b_u, c, sign, isMin)
print(s.table)