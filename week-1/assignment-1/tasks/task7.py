import time
import numpy as np
from methods.muller import muller
from methods.secant import secant
from methods.newton_raphson import newton

# Polynomial: f(x) = x^4 − 3x^3 + x^2 + x + 1

def f(x):
    return x**4 - 3*x**3 + x**2 + x + 1

def df(x):
    return 4*x**3 - 9*x**2 + 2*x + 1

# Utility: deduplicate roots within tolerance

def dedup(roots, tol=1e-7):
    uniq = []
    for r in roots:
        if not any(abs(r - u) < tol for u in uniq):
            uniq.append(r)
    return uniq

print("Muller's method — complex roots for x^4 − 3x^3 + x^2 + x + 1 = 0\n")

# Seeds for Muller's (triplets)
triplets = [
    (0+0j, 0.6+0.8j, 0.6-0.8j),
    (1+0j, 1+1j, 1-1j),
    (2+0j, 1.5+0.5j, 1.5-0.5j),
    (-1+0j, -0.5+0.8j, -0.5-0.8j),
]

muller_roots = []
start = time.perf_counter()
for idx, (x0, x1, x2) in enumerate(triplets):
    table = muller(f, x0, x1, x2, epsilon=1e-10, max_iterations=100)
    if table:
        root = table[-1][2]
        muller_roots.append(root)
        print(f"Muller seed {idx}: iterations={len(table):2d}, root={root}")
    else:
        print(f"Muller seed {idx}: no convergence")
end = time.perf_counter()

muller_roots = dedup(muller_roots, tol=1e-7)
print(f"\nMuller unique roots ({len(muller_roots)}):")
for r in muller_roots:
    print(f"  {r}")
print(f"Muller total time: {(end-start)*1e3:.2f} ms\n")

# Newton's method (supports complex if derivative provided)
newton_seeds = [0+0j, 1+0j, 2+0j, -1+0j, 1+1j, 1-1j]
newton_roots = []
start = time.perf_counter()
for i, x0 in enumerate(newton_seeds):
    table = newton(f, df, x0, epsilon=1e-10, max_iterations=100)
    if table:
        root = table[-1][2]
        newton_roots.append(root)
        print(f"Newton seed {i}: iterations={len(table):2d}, root={root}")
    else:
        print(f"Newton seed {i}: no convergence")
end = time.perf_counter()
newton_roots = dedup(newton_roots, tol=1e-7)
print(f"\nNewton unique roots ({len(newton_roots)}):")
for r in newton_roots:
    print(f"  {r}")
print(f"Newton total time: {(end-start)*1e3:.2f} ms\n")

# Secant method with complex pairs
secant_pairs = [
    (0.6+0.8j, 0.6-0.8j),
    (1+1j, 1-1j),
    (2+0j, 1+0j),
    (-1+0j, -0.5+0.2j),
]
secant_roots = []
start = time.perf_counter()
for i, (x0, x1) in enumerate(secant_pairs):
    table = secant(f, x0, x1, epsilon=1e-10, max_iterations=200)
    if table:
        root = table[-1][2]
        secant_roots.append(root)
        print(f"Secant pair {i}: iterations={len(table):3d}, root={root}")
    else:
        print(f"Secant pair {i}: no convergence")
end = time.perf_counter()
secant_roots = dedup(secant_roots, tol=1e-7)
print(f"\nSecant unique roots ({len(secant_roots)}):")
for r in secant_roots:
    print(f"  {r}")
print(f"Secant total time: {(end-start)*1e3:.2f} ms\n")

# Summary
print("Summary (unique roots per method):")
print(f"  Muller: {len(muller_roots)} roots")
print(f"  Newton: {len(newton_roots)} roots")
print(f"  Secant: {len(secant_roots)} roots")

