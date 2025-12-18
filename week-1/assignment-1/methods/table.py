import numpy as np
from tabulate import tabulate
from methods.bisection import bisection
from methods.fixed_point import fixed_point
from methods.newton_raphson import newton
from methods.secant import secant
from methods.false_point import false_point
from methods.muller import muller

func = lambda x: x**3 - x - 2
gx = lambda x: (x + 2)**(1/3)      # Fixed-Point iteration: x = (x+2)^(1/3)
dfunc = lambda x: 3*x**2 - 1        # Newton-Raphson derivative

# Initial guesses / intervals
a, b = 1, 2      # Bisection interval
x0 = 0.5         # Fixed-Point initial guess
x1 = 1.0         # Newton-Raphson initial guess
x0_sec = 0.5     # Secant first guess
x1_sec = 1.0     # Secant second guess
x0_mul = 1.0     # Muller first guess
x1_mul = 1.5     # Muller second guess
x2_mul = 2.0     # Muller third guess

# Tolerances
tolerance = 1e-3
max_iter = 50

b_table = bisection(func, a, b, tolerance)
fp_table = fixed_point(gx, x0, tolerance, max_iter)
newton_table = newton(func, dfunc, x1, tolerance, max_iter)
secant_table = secant(func, x0_sec, x1_sec, tolerance, max_iter)
false_table = false_point(func, a, b, tolerance, max_iter)
muller_table = muller(func, x0_mul, x1_mul, x2_mul, tolerance, max_iter)


max_len = max(len(b_table), len(fp_table), len(newton_table), len(secant_table), len(false_table), len(muller_table))


rows = []
for i in range(max_len):
    rows.append([
        i,
        f"{b_table[i][1]:.6f}" if i < len(b_table) else "-",
        f"{fp_table[i][1]:.6f}" if i < len(fp_table) else "-",
        f"{newton_table[i][1]:.6f}" if i < len(newton_table) else "-",
        f"{secant_table[i][1]:.6f}" if i < len(secant_table) else "-",
        f"{false_table[i][1]:.6f}" if i < len(false_table) else "-",
        f"{muller_table[i][1]:.6f}" if i < len(muller_table) else "-",
    ])

print(tabulate(
    rows,
    headers=["Iter", "Bisection", "Fixed-Point", "Newton-Raphson", "Secant", "False-Position", "Muller"],
    tablefmt="grid"
))

print("\nFinal Approximations:")
if b_table:
    print(f"Bisection: x ≈ {b_table[-1][1]:.5f}")
if fp_table:
    print(f"Fixed-Point: x ≈ {fp_table[-1][1]:.5f}")
if newton_table:
    print(f"Newton-Raphson: x ≈ {newton_table[-1][2]:.5f}")
if secant_table:
    print(f"Secant: x ≈ {secant_table[-1][2]:.5f}")
if false_table:
    print(f"False-Position: x ≈ {false_table[-1][1]:.5f}")
if muller_table:
    print(f"Muller: x ≈ {muller_table[-1][2]:.5f}")

