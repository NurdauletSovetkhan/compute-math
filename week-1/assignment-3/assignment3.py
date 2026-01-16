import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

x = np.array([1, 2, 3, 4])
y = np.array([2.5, 6.9, 18.3, 50.1])

def linear_func(x, a, b):
    return a * x + b

def poly2_func(x, a, b, c):
    return a * x**2 + b * x + c

def exp_func(x, a, b):
    return a * np.exp(b * x)

def power_func(x, a, b):
    return a * x**b

def log_func(x, a, b):
    return a + b * np.log(x)

models = [
    ("Linear", "y = a*x + b", linear_func),
    ("Quadratic", "y = ax^2 + bx + c", poly2_func),
    ("Exponential", "y = a * e^(bx)", exp_func),
    ("Power", "y = a * x^b", power_func),
    ("Logarithmic", "y = a + b*ln(x)", log_func)
]

best_s = 10**10
best_name = ""
best_params = []
best_func = None

header = f"{'Model Type':<15} | {'Equation':<18} | {'Parameters':<25} | {'S (Error)':<10}"
print(header)
print("-" * len(header))

for name, eq, func in models:
    try:
        popt, _ = curve_fit(func, x, y)
        y_pred = func(x, *popt)
        s_value = np.sum((y - y_pred)**2)
        
        if len(popt) == 2:
            params_text = f"a={popt[0]:.3f}, b={popt[1]:.3f}"
        else:
            params_text = f"a={popt[0]:.3f}, b={popt[1]:.3f}, c={popt[2]:.3f}"
            
        print(f"{name:<15} | {eq:<18} | {params_text:<25} | {s_value:.4f}")
        
        if s_value < best_s:
            best_s = s_value
            best_name = name
            best_params = popt
            best_func = func
    except:
        continue

print("-" * len(header))
print(f"BEST MODEL: {best_name}")

plt.figure(figsize=(8, 5))
plt.plot(x, y, 'bo', label='Experimental Data') 

x_smooth = np.linspace(min(x), max(x), 100)
y_final = best_func(x_smooth, *best_params)
plt.plot(x_smooth, y_final, 'r-', label=f'Best fit: {best_name}')

plt.title('Least Squares Approximation Analysis')
plt.xlabel('X axis')
plt.ylabel('Y axis')
plt.legend()
plt.grid(True)
plt.show()