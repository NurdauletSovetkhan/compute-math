import numpy as np

# Jacobi Iterative Method
# Итерационный метод решения систем линейных уравнений Ax = b.
# В отличие от Гаусса-Зейделя, все новые значения x[i] вычисляются используя СТАРЫЕ значения.
# Это означает, что итерации можно легко распараллелить.
# Формула: x[i]^(k+1) = (b[i] - sum(A[i,j] * x[j]^(k), j != i)) / A[i,i]
# Сходится если матрица диагонально доминантная или положительно определённая.
# Сходится медленнее чем Гаусс-Зейдель, но проще для параллелизации.

def jacobi(A, b, x0=None, max_iter=100, tol=1e-6):
    """
    Решение системы линейных уравнений методом Якоби.
    
    Параметры:
        A: матрица коэффициентов (n x n)
        b: вектор правых частей (n,)
        x0: начальное приближение (по умолчанию нулевой вектор)
        max_iter: максимальное число итераций
        tol: допустимая погрешность
    
    Возвращает:
        x: вектор решения
        iterations_data: данные по итерациям
        converged: флаг сходимости
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    
    if x0 is None:
        x = np.zeros(n)
    else:
        x = np.array(x0, dtype=float).copy()
    
    iterations_data = []
    
    # Сохраняем начальное приближение
    iterations_data.append({
        'iteration': 0,
        'x': x.copy(),
        'error': None
    })
    
    # Проверяем диагональные элементы
    for i in range(n):
        if abs(A[i, i]) < 1e-10:
            raise ValueError(f"Нулевой диагональный элемент в позиции {i}")
    
    for k in range(max_iter):
        x_new = np.zeros(n)
        
        for i in range(n):
            # Сумма A[i,j] * x[j] для всех j != i (используем СТАРЫЕ значения x)
            sum_term = 0.0
            for j in range(n):
                if j != i:
                    sum_term += A[i, j] * x[j]
            
            # Формула Якоби
            x_new[i] = (b[i] - sum_term) / A[i, i]
        
        # Вычисляем погрешность (максимальная абсолютная разность)
        error = np.max(np.abs(x_new - x))
        
        # Обновляем x
        x = x_new.copy()
        
        # Сохраняем данные итерации
        iterations_data.append({
            'iteration': k + 1,
            'x': x.copy(),
            'error': error
        })
        
        # Проверяем сходимость
        if error < tol:
            return x, iterations_data, True
    
    # Не сошлось за max_iter итераций
    return x, iterations_data, False


def check_convergence(A):
    """
    Проверка достаточного условия сходимости (диагональное преобладание).
    
    Возвращает True, если матрица диагонально доминантная.
    """
    n = A.shape[0]
    for i in range(n):
        diagonal = abs(A[i, i])
        off_diagonal_sum = sum(abs(A[i, j]) for j in range(n) if j != i)
        if diagonal <= off_diagonal_sum:
            return False
    return True


def solve(A, b, x0=None, max_iter=100, tol=1e-6):
    """Обёртка для унификации интерфейса."""
    return jacobi(A, b, x0, max_iter, tol)
