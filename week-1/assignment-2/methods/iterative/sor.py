import numpy as np

# SOR (Successive Over-Relaxation) Method
# Улучшенная версия метода Гаусса-Зейделя с параметром релаксации ω (omega).
# При ω = 1 метод совпадает с Гауссом-Зейделем.
# При 0 < ω < 1 - недорелаксация (under-relaxation), стабилизирует сходимость.
# При 1 < ω < 2 - сверхрелаксация (over-relaxation), ускоряет сходимость.
# Оптимальное ω зависит от матрицы и обычно находится эмпирически.
# Формула: x[i]^(k+1) = (1-ω)*x[i]^(k) + ω*(b[i] - sum1 - sum2) / A[i,i]
# Сходится быстрее Гаусса-Зейделя при правильном выборе ω.

def sor(A, b, omega=1.25, x0=None, max_iter=100, tol=1e-6):
    """
    Решение системы линейных уравнений методом SOR.
    
    Параметры:
        A: матрица коэффициентов (n x n)
        b: вектор правых частей (n,)
        omega: параметр релаксации (0 < omega < 2 для сходимости)
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
    
    # Проверка параметра релаксации
    if omega <= 0 or omega >= 2:
        raise ValueError("Параметр omega должен быть в диапазоне (0, 2) для гарантии сходимости")
    
    if x0 is None:
        x = np.zeros(n)
    else:
        x = np.array(x0, dtype=float).copy()
    
    iterations_data = []
    
    # Сохраняем начальное приближение
    iterations_data.append({
        'iteration': 0,
        'x': x.copy(),
        'omega': omega,
        'error': None
    })
    
    # Проверяем диагональные элементы
    for i in range(n):
        if abs(A[i, i]) < 1e-10:
            raise ValueError(f"Нулевой диагональный элемент в позиции {i}")
    
    for k in range(max_iter):
        x_old = x.copy()
        
        for i in range(n):
            # sum1: использует уже обновлённые значения (как в Гаусс-Зейделе)
            sum1 = np.dot(A[i, :i], x[:i])
            # sum2: использует старые значения
            sum2 = np.dot(A[i, i+1:], x_old[i+1:])
            
            # Гаусс-Зейдельовское обновление
            x_gs = (b[i] - sum1 - sum2) / A[i, i]
            
            # SOR: взвешенное среднее между старым и новым значением
            x[i] = (1 - omega) * x_old[i] + omega * x_gs
        
        # Вычисляем погрешность
        error = np.max(np.abs(x - x_old))
        
        # Сохраняем данные итерации
        iterations_data.append({
            'iteration': k + 1,
            'x': x.copy(),
            'omega': omega,
            'error': error
        })
        
        # Проверяем сходимость
        if error < tol:
            return x, iterations_data, True
    
    # Не сошлось за max_iter итераций
    return x, iterations_data, False


def optimal_omega(A):
    """
    Оценка оптимального параметра ω для симметричных положительно определённых матриц.
    
    Для трёхдиагональных матриц с постоянными коэффициентами:
    ω_opt = 2 / (1 + sqrt(1 - ρ²))
    где ρ - спектральный радиус матрицы Якоби.
    
    Для общего случая возвращает приближённое значение.
    """
    n = A.shape[0]
    # Построение матрицы Якоби
    D = np.diag(np.diag(A))
    L = np.tril(A, -1)
    U = np.triu(A, 1)
    
    try:
        D_inv = np.linalg.inv(D)
        T_jacobi = -np.dot(D_inv, L + U)
        eigenvalues = np.linalg.eigvals(T_jacobi)
        rho = np.max(np.abs(eigenvalues))  # Спектральный радиус
        
        if rho >= 1:
            return 1.0  # Метод может не сходиться
        
        omega_opt = 2 / (1 + np.sqrt(1 - rho**2))
        return omega_opt
    except:
        return 1.0  # Возвращаем значение Гаусса-Зейделя при ошибке


def solve(A, b, omega=1.25, x0=None, max_iter=100, tol=1e-6):
    """Обёртка для унификации интерфейса."""
    return sor(A, b, omega, x0, max_iter, tol)
