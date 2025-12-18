import numpy as np
from methods.secant import secant

def f(x):
    return np.exp(-x) - x

x0 = 0.0
x1 = 1.0

tol = 1e-4  # stop when |x_{n+1} - x_n| < tol
max_iter = 100

# Run secant
iterations = secant(f, x0, x1, epsilon=tol, max_iterations=max_iter)

# Print iteration table
print("Secant Method for e^{-x} = x (f(x) = e^{-x} - x) with x0=0, x1=1, tol=1e-4")
print(f"{'k':<4} {'x_k':>12} {'x_{k+1}':>12} {'f(x_k)':>12} {'|Δx|':>12}")
prev = None
for (k, xk, xk1, fxk) in iterations:
    dx = abs(xk1 - xk)
    print(f"{k:<4} {xk:>12.8f} {xk1:>12.8f} {fxk:>12.8f} {dx:>12.8f}")
    prev = (k, xk, xk1)

# Final result
if iterations:
    final_x = iterations[-1][2]
    print("\nFinal approximation (4 d.p.): x ≈ {:.4f}".format(final_x))
    print("Iterations performed: {}".format(len(iterations)))
else:
    print("No iterations recorded; method failed to start.")
