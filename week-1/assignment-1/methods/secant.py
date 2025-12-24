import numpy as np

# Derivative is replaced by finite difference
# Uses two previous points:
# x_{n+1} = x_n - f(x_n)*(x_n - x_{n-1}) / (f(x_n) - f(x_{n-1}))

def secant(func, x0, x1, epsilon=1e-6, max_iterations=1000):
    table = []

    for iteration in range(max_iterations):
        f0 = func(x0)
        f1 = func(x1)

        # Write row BEFORE update
        table.append((iteration, x0, x1, f0))

        # Check denominator
        if (f1 - f0) == 0:
            print(f"Secant failed at iter {iteration}: division by zero.")
            break

        # New approximation
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)

        # Check invalid values (NaN/Inf)
        if not np.isfinite(x2):
            print(f"Secant diverged at iter {iteration}: x2 not finite.")
            break

        # Convergence
        if abs(x2 - x1) < epsilon:
            table.append((iteration + 1, x1, x2, f1))
            break

        # Shift values
        x0, x1 = x1, x2

    return table
