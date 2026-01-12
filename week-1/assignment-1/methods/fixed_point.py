import numpy as np

# Fixed Point Iteration Method
# The trick here is to rewrite f(x) = 0 into the form x = g(x).
# Then we just keep plugging our guess back in: x_new = g(x_old), and repeat until it stabilizes.
# The catch is that it only works if |g'(x)| < 1 near the root, otherwise it blows up.
# When it works though, its pretty elegant and easy to implement.

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