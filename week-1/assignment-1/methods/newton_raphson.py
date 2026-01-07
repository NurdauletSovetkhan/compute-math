import numpy as np

# Newton-Raphson Method
# This is one of the fastest root-finding methods out there.
# The idea is to draw a tangent line at your current guess and see where it hits the x-axis.
# That intersection becomes your next guess. Formula: x_new = x_old - f(x_old) / f'(x_old)
# It converges really fast (quadratically) when you start close to the root.
# Downside: you need to know the derivative, and it can fail if f'(x) is zero or you start too far.

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
