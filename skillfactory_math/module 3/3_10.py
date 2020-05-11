import numpy as np

def hessian(x):
    """
     Вычисление матрицы Гессе
     Параметры:
        - x: ndarray
     Возвращает:
        массив вида (x.dim, x.ndim) + x.shape
        где массив [i, j, ...] соответствует второй производной x_ij
    """
    x_grad = np.gradient(x)
    hessian = np.empty((x.ndim, x.ndim) + x.shape, dtype=x.dtype)
    for k, grad_k in enumerate(x_grad):
        # перебираем измерения
        # применяем градиент снова к каждому компоненту первой производной
        tmp_grad = np.gradient(grad_k)
        for l, grad_kl in enumerate(tmp_grad):
            hessian[k, l, :, :] = grad_kl
    return hessian

x = np.random.randn(100, 100, 100)
hessian(x)