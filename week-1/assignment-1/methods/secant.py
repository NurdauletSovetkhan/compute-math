import numpy as np

# Secant Method
# Think of this as Newton-Raphson but without needing the actual derivative.
# Instead of the true derivative, we approximate it using the slope between two previous points.
# Formula: x_new = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
# Its almost as fast as Newton and you dont need to compute derivatives, which is nice.
# You do need two starting points though, not just one.

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
