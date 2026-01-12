import numpy as np
from tabulate import tabulate
from methods.newton_raphson import newton
f = lambda x: 5*x - np.cos(x) - 3
f_prime = lambda x: 5 + np.sin(x)

x0 = 0.5
tol = 0.0001 

# Run Newton-Raphson
table = newton(f, f_prime, x0, epsilon=tol)

rows = []
for k, xk, xk1, fxk in table:
    rows.append([
        k,
        f"{xk:.6f}",
        f"{fxk:.6f}",
        f"{f_prime(xk):.6f}",
        f"{xk1:.6f}",
        f"{abs(xk1 - xk):.6f}"
    ])

print("\nNewton-Raphson Iteration Table")
print(tabulate(
    rows,
    headers=["k", "x_k", "f(x_k)", "f'(x_k)", "x_{k+1}", "|Δx|"],
    tablefmt="grid"
))

if table:
    final_x = table[-1][2]
    f_val = f(final_x)
    
    print(f"\nFinal Result:")
    print(f"Root x ≈ {final_x:.4f}")
    print(f"Verification:")
    print(f"  5x = {5*final_x:.4f}")
    print(f"  cos(x) + 3 = {np.cos(final_x) + 3:.4f}")
    print(f"  f(x) = {f_val:.6f}")
    print(f"Converged in {len(table)} iterations.")