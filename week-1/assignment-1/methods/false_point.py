import numpy as np

def false_point(func, a, b, epsilon=1e-6, max_iterations=1000):
    fa = func(a)
    fb = func(b)

    if fa * fb > 0:
        print("False-Position: No sign change in [a,b].")
        return []

    table = []

    for k in range(max_iterations):
        fa = func(a)
        fb = func(b)

        denom = (fb - fa)
        if denom == 0:
            print(f"False-Position failed at iter {k}: division by zero.")
            break

        c = b - fb * (b - a) / denom
        fc = func(c)

        if not (np.isfinite(c) and np.isfinite(fc)):
            print(f"False-Position diverged at iter {k}: non-finite value.")
            break

        table.append((k, c, fc))

        if abs(fc) < epsilon or abs(b - a) < epsilon:
            break

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    return table
