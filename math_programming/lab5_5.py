import numpy as np


class TransportModel:

    def __init__(self, A, B, C) -> None:
        super().__init__()
        self.A = A
        self.B = B
        self.C = C
        self.X = None
        self.U = None
        self.V = None
        self.cell = None
        self.basis = []

    def solve(self):
        self._check_balance()
        self._iter(0, 0)
        print('X:', self.X, sep='\n')
        print('Базис:',self.basis, sep='\n')
        count_comp = self.C.shape[0] + self.C.shape[1] - 1
        is_solve = self._check_solve()
        is_basis = count_comp == len(self.basis)
        is_sincerity = not len([num for num in self.basis if num > 0]) == count_comp
        print(f'Допустимое решение - {is_solve}\n'
              f'Базисное решение - {is_basis}\n'
              f'Вырожденное решение - {is_sincerity}')
        print('Значение целевой функции - ',sum(sum(self.C * self.X)))

        self._calc_potential()
        sol = self._check_optimal_sol()
        self.path[sol[0], sol[1]] = 1
        self._draw_cycle(sol[0], sol[1], -1)

    def _check_balance(self):
        a_sum = np.sum(self.A)
        b_sum = np.sum(self.B)
        if a_sum > b_sum:
            self.B = np.append(self.B, a_sum - b_sum)
            loc_c = np.zeros((self.C.shape[0], 1))
            self.C = np.hstack((self.C, loc_c))
        elif b_sum > a_sum:
            self.A = np.append(self.A, b_sum - a_sum)
            loc_c = np.zeros((1, self.C.shape[1]))
            self.C = np.vstack((self.C, loc_c))

        self._refresh_potential()
        self.A_clone = np.array(self.A)
        self.B_clone = np.array(self.B)
        self.X = np.zeros((self.C.shape))
        self.cell = np.zeros((self.C.shape))
        self.path = np.zeros((self.C.shape))

    def _iter(self, i, j):
        if i == self.C.shape[0] or j == self.C.shape[1]:
            return
        if self.A[i] < self.B[j]:
            self.X[i][j] = A[i]
            self.cell[i][j] = 1
            self.basis.append(self.X[i][j])
            self.B[j] = self.B[j] - self.A[i]
            self.A[i] = 0
            #self.C[i, j + 1:self.C.shape[1]] = 0
            self._iter(i + 1, j)
        else:
            self.X[i][j] = self.B[j]
            self.cell[i][j] = 1
            self.basis.append(self.X[i][j])
            self.A[i] = self.A[i] - self.B[j]
            self.B[j] = 0
            #self.C[i + 1:self.C.shape[0], j] = 0
            self._iter(i, j + 1)

    def _refresh_potential(self):
        self.U = [np.inf for i in range(0, len(self.A))]
        self.V = [np.inf for i in range(0, len(self.B))]

    def _calc_potential(self):
        self.U[0] = 0
        size = self.X.shape
        for i in range(0, size[0]):
            for j in range(0, size[1]):
                if self.cell[i][j] != 0:
                    if self.U[i] != np.inf:
                        self.V[j] = self.C[i][j] - self.U[i]
                    else:
                        self.U[i] = self.C[i][j] - self.V[j]

    def _check_optimal_sol(self):
        eco_values = []
        size = self.X.shape
        for i in range(0, size[0]):
            for j in range(0, size[1]):
                if self.cell[i][j] == 0:
                    val = self.U[i] + self.V[j]
                    if val > self.X[i][j]:
                        val -= self.C[i][j]
                        eco_values.append((i,j,val,self.U[i]))
        if len(eco_values) == 0:
            return -1
        else:
            eco_values = sorted(eco_values, key=lambda x: (x[2], -x[3]), reverse=True)
            return eco_values[0]


    def _draw_cycle(self, start_i, start_j, sign):
        size = self.cell.shape

        # можно ли налево и направо
        if np.count_nonzero(self.path[start_i] == 0) == size[1] - 1:
            # налево
            for j in range(start_j - 1, -1, -1):
                if self.cell[start_i][j] == 1 and np.count_nonzero(self.path[:, j] == 0) != size[0] - 2:
                    self.path[start_i][j] = sign
                    self._draw_cycle(start_i, j, sign * -1)
            # направо
            for j in range(start_j + 1, size[1]):
                if self.cell[start_i][j] == 1 and np.count_nonzero(self.path[:, j] == 0) != size[0] - 2:
                    self.path[start_i][j] = sign
                    self._draw_cycle(start_i, j, sign * -1)

        # можно ли вверх и вниз
        if np.count_nonzero(self.path[:, start_j] == 0) == size[0] - 1:
            # вниз
            for i in range(start_i + 1, size[0]):
                if self.cell[i][start_j] == 1 and np.count_nonzero(self.path[i] == 0) != size[1] - 2:
                    self.path[i][start_j] = sign
                    self._draw_cycle(i, start_j, sign * -1)
            # вверх
            for i in range(start_i - 1, -1, -1):
                if self.cell[i][start_j] == 1 and np.count_nonzero(self.path[i] == 0) != size[1] - 2:
                    self.path[i][start_j] = sign
                    self._draw_cycle(i, start_j, sign * -1)


    def _check_solve(self):
        for i in range(0, self.C.shape[0]):
            if self.A_clone[i] != np.sum(self.X[i,:]):
                return False
        for i in range(0, self.C.shape[1]):
            if self.B_clone[i] != np.sum(self.X[:,i]):
                return False
        return True


A = np.array([100, 250, 200, 300])
B = np.array([200, 200, 100, 100, 250])
C = np.array([
    [10, 7, 4, 1, 4],
    [2, 7, 10, 6, 11],
    [8, 5, 3, 2, 2],
    [11, 8, 12, 16, 13]
])
# A = np.array([350,330,270])
# B = np.array([210,170,220,150,200])
# C = np.array([
#     [3,12,9,1,7],
#     [2,4,11,2,10],
#     [7,14,12,5,8]
# ])
# print('Введите в строку через пробел значения поставщиков')
# A = np.array(list(map(int,input().split(" "))))
# print('Введите в строку значения потребителей')
# B = np.array(list(map(int,input().split(" "))))
# shape = (len(A), len(B))
# print('Введите ',shape[0],'строк(-и) стоимости',shape[1],'перевозок товаров(-а)')
# C = []
# for i in range(0, shape[0]):
#     C.append(list(map(int,input().split(" "))))
# C = np.array(C)
model = TransportModel(A, B, C)
model.solve()
