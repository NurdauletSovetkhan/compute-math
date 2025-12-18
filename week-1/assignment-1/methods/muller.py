import numpy as np

def muller(func, x0, x1, x2, epsilon=1e-6, max_iterations=1000):
    """
    Muller's method for root finding using a quadratic through (x0,f0), (x1,f1), (x2,f2).
    Supports complex arithmetic and returns a table of tuples:
      (iteration, x_k, x_{k+1}, f(x_k))
    where x_k is the current point (x2) before the update.
    """
    # Ensure complex dtype for robust complex support
    x0 = complex(x0)
    x1 = complex(x1)
    x2 = complex(x2)

    table = []
    tiny = 1e-15

    for k in range(max_iterations):
        f0 = func(x0)
        f1 = func(x1)
        f2 = func(x2)

        h0 = x1 - x0
        h1 = x2 - x1
        if abs(h0) < tiny or abs(h1) < tiny:
            # Degenerate spacing; attempt a small perturbation step (secant-like)
            b = (f2 - f1) / (h1 if abs(h1) > tiny else (h0 if abs(h0) > tiny else 1.0))
            if abs(b) < tiny:
                # Cannot progress
                break
            x3 = x2 - f2 / b
        else:
            delta0 = (f1 - f0) / h0
            delta1 = (f2 - f1) / h1
            denom_h = (h1 + h0)
            if abs(denom_h) < tiny:
                # Near linear; do a secant-like step from (x1,x2)
                b = delta1
                if abs(b) < tiny:
                    break
                x3 = x2 - f2 / b
            else:
                a = (delta1 - delta0) / denom_h
                b = a * h1 + delta1
                c = f2

                # Use complex-safe sqrt
                disc = b*b - 4*a*c
                sqrt_disc = np.lib.scimath.sqrt(disc)

                # Choose denominator to avoid catastrophic cancellation
                denom1 = b + sqrt_disc
                denom2 = b - sqrt_disc
                denom = denom1 if abs(denom1) > abs(denom2) else denom2
                if abs(denom) < tiny:
                    # Fall back to secant-like step
                    if abs(b) < tiny:
                        break
                    x3 = x2 - c / b
                else:
                    x3 = x2 + (-2*c) / denom

        # Record row BEFORE updating triplet
        table.append((k, x2, x3, f2))

        # Convergence by step size (complex magnitude)
        if abs(x3 - x2) < epsilon:
            break

        # Validate finite values (real and imag parts finite)
        if not np.isfinite(x3.real) or not np.isfinite(x3.imag):
            print(f"Muller diverged at iter {k}: x3 not finite.")
            break

        # Shift points: keep the most recent three
        x0, x1, x2 = x1, x2, x3

    return table
