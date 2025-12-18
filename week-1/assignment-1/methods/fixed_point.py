import numpy as np

def fixed_point(g, x0, eps, max_iter):
    table = []
    x = x0

    for k in range(max_iter):
        x_next = g(x)
        diff = abs(x_next - x)
        table.append((k, x, x_next, diff))

        if not np.isfinite(x_next):
            print(f"Divergence at iteration {k}: non-finite value")
            break

        if diff < eps:
            break

        x = x_next

    return table