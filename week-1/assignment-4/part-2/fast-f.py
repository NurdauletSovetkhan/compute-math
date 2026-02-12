import numpy as np

# f = [1.0000, 1.2214, 1.4918, 1.8221, 2.2255]
f = [2,6,14,30,62,126]
h = 1  # Шаг по x (x1 - x0)
idx = 1

# --- ВАРИАНТ 1: Конечные разности (Forward Differences) ---
delta_1 = np.diff(f, n=1)  # Первая разность [f(x+h) - f(x)]
delta_2 = np.diff(f, n=2)  # Вторая разность [f(x+2h) - 2f(x+h) + f(x)]
delta_3 = np.diff(f, n=3)
delta_4 = np.diff(f, n=4)

# --- ВАРИАНТ 2: Производные (Derivatives) ---
f_prime = delta_1 / h
f_double_prime = delta_2 / (h**2)
f_triple_prime = delta_3 / (h**3)


# --- ВАРИАНТ 3: Центральные разности (Central Differences) ---

# Формула: (f[i+1] - f[i-1]) / (2*h)
if idx > 0 and idx < len(f) - 1:
    f_prime_central = (f[idx+1] - f[idx-1]) / (2 * h)
    print(f"Центральная производная f'({idx+1}): {f_prime_central}")

# --- ПРИМЕР ДЛЯ ЗАДАЧИ ---
print(f"Конечная разность Δ²f(1.1): {delta_4[idx]:.4f}")
# print(f"Вторая производная f''(1.1): {f_triple_prime[idx]:.2f}") 
# print(f"The central thing is: {f_prime_central}")

