import numpy as np
from methods.fixed_point import fixed_point
print("=" * 70)
print("Fixed-Point Iteration for ln(x+1) + x^2 = 0 on [0,1]")
print("=" * 70)

g = lambda x: np.exp(-x**2) - 1
g_prime = lambda x: -2*x*np.exp(-x**2)

# Check convergence condition on the range where iteration stays
x_check = np.linspace(-0.5, 0.5, 100)
g_prime_vals = np.abs(g_prime(x_check))

print("\nConvergence check:")
print(f"|g'(x)| min = {g_prime_vals.min():.4f}")
print(f"|g'(x)| max = {g_prime_vals.max():.4f}")

if g_prime_vals.max() < 1:
    print("✓ |g'(x)| < 1 on [0,1]")
else:
    print("✗ |g'(x)| < 1 NOT satisfied everywhere")

# Iteration parameters - start closer to the root
x0 = 0.1
tol = 1e-3
max_iter = 50

table = fixed_point(g, x0, tol, max_iter)

print("\nIterations:")
print(f"{'k':<5}{'x_k':<15}{'x_{k+1}':<15}{'|Δx|':<15}")
for k, xk, xk1, d in table:
    print(f"{k:<5}{xk:<15.6f}{xk1:<15.6f}{d:<15.6f}")

# Final analysis
if table:
    final_x = table[-1][2]
    f_val = np.log(final_x + 1) + final_x**2

    print("\nFinal result:")
    print(f"x ≈ {final_x:.6f}")
    print(f"ln(x+1) + x^2 = {f_val:.6f}")

    if abs(f_val) < tol:
        print(f"Conclusion: Root found at x ≈ {final_x:.6f}")
    else:
        print("Conclusion: Method did not converge to required tolerance.")