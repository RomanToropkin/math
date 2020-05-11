import numpy as np


class TransportModel:

    def __init__(self, A, B, C) -> None:
        super().__init__()
        self.A = A
        self.B = B
        self.C = C
        self.X = None
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

        self.A_clone = np.array(self.A)
        self.B_clone = np.array(self.B)
        self.X = np.zeros((self.C.shape))

    def _iter(self, i, j):
        if i == self.C.shape[0] or j == self.C.shape[1]:
            return
        if self.A[i] < self.B[j]:
            self.X[i][j] = A[i]
            self.basis.append(self.X[i][j])
            self.B[j] = self.B[j] - self.A[i]
            self.A[i] = 0
            #self.C[i, j + 1:self.C.shape[1]] = 0
            self._iter(i + 1, j)
        else:
            self.X[i][j] = self.B[j]
            self.basis.append(self.X[i][j])
            self.A[i] = self.A[i] - self.B[j]
            self.B[j] = 0
            #self.C[i + 1:self.C.shape[0], j] = 0
            self._iter(i, j + 1)


    def _check_solve(self):
        for i in range(0, self.C.shape[0]):
            if self.A_clone[i] != np.sum(self.X[i,:]):
                return False
        for i in range(0, self.C.shape[1]):
            if self.B_clone[i] != np.sum(self.X[:,i]):
                return False
        return True


print('Введите в строку через пробел значения поставщиков')
A = np.array(list(map(int,input().split(" "))))
print('Введите в строку значения потребителей')
B = np.array(list(map(int,input().split(" "))))
shape = (len(A), len(B))
print('Введите ',shape[0],'строк(-и) стоимости',shape[1],'перевозок товаров(-а)')
C = []
for i in range(0, shape[0]):
    C.append(list(map(int,input().split(" "))))
C = np.array(C)
model = TransportModel(A, B, C)
model.solve()
