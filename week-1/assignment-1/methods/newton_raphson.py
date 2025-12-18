import numpy as np

# Based on tangent line approximation of the function
# Iteration formula:
# x_{n+1} = x_n - f(x_n) / f'(x_n)

def newton(func, dfunc, x0, epsilon=1e-6, max_iterations=1000):
    """
    Newton-Raphson Method
    Returns table: (iteration, x0, x1, f(x0))
    """
    table = []

    for iteration in range(max_iterations):
        f0 = func(x0)
        df0 = dfunc(x0)

        if df0 == 0:
            print(f"Newton failed at iter {iteration}: derivative is zero.")
            break

        x1 = x0 - f0 / df0

        # Save row
        table.append((iteration, x0, x1, f0))

        if not np.isfinite(x1):
            print(f"Newton diverged at iter {iteration}: x1 not finite.")
            break

        # Convergence
        if abs(x1 - x0) < epsilon:
            break

        x0 = x1

    return table
