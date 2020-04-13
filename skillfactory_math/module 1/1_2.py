import numpy as np

np.set_printoptions(precision=5, suppress=True)

apartment = np.array([59.50, 31.40, 19, 2, 60550, 2])
# В NumPy вектор и массив - одно и то же.
# Исключение - понятие вектор-столбец и вектор-строка - фактически двумерные массивы,
# где один из атрибутов shape равен 1.

share_living_space = round(apartment[1]/apartment[0],2)
print(f'{share_living_space}')
apartment = np.delete(apartment, [0, 1])
apartment = np.append(apartment, share_living_space)

print("ndim:", apartment.ndim) # число осей (измерений) массива - n.dim: 1
print("shape:", apartment.shape) # размеры массива, для вектора определена только длина - shape: (6, )
