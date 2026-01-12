import time
import numpy as np


TINY = 1e-15


def secant_custom(f, x0, x1, tol=1e-6, max_iter=200, criterion="absolute"):
	rows = []
	xk, xk1 = complex(x0), complex(x1)
	for k in range(max_iter):
		fk = f(xk)
		fk1 = f(xk1)
		denom = (fk1 - fk)
		if denom == 0:
			break
		xk2 = xk1 - fk1 * (xk1 - xk) / denom
		Ea = abs(xk2 - xk1)
		Er = Ea / max(abs(xk2), TINY)
		rows.append((k, xk1, xk2, fk1, Ea, Er))
		if criterion == "absolute" and Ea < tol:
			break
		if criterion == "relative" and Er < tol:
			break
		xk, xk1 = xk1, xk2
	return rows


def newton_custom(f, df, x0, tol=1e-6, max_iter=200, criterion="absolute"):
	rows = []
	xk = complex(x0)
	for k in range(max_iter):
		fk = f(xk)
		dfk = df(xk)
		if dfk == 0:
			break
		xk1 = xk - fk / dfk
		Ea = abs(xk1 - xk)
		Er = Ea / max(abs(xk1), TINY)
		rows.append((k, xk, xk1, fk, Ea, Er))
		if criterion == "absolute" and Ea < tol:
			break
		if criterion == "relative" and Er < tol:
			break
		xk = xk1
	return rows


def summarize(label, rows):
	if not rows:
		print(f"{label}: no iterations")
		return
	last = rows[-1]
	k, xk, xk1, fk, Ea, Er = last
	print(f"{label}: iter={len(rows)}, approx={xk1}, Ea={Ea:.3e}, Er={Er:.3e}")


def run_examples():
	# Example 1: f(x) = e^{-x} - x, root ~ 0.567143
	f1 = lambda x: np.exp(-x) - x
	df1 = lambda x: -np.exp(-x) - 1

	print("\nExample 1: f(x) = e^{-x} - x (root ~ 0.567143)\n")
	for tol in [1e-1, 1e-3, 1e-6]:
		s_abs = secant_custom(f1, 0.0, 1.0, tol=tol, criterion="absolute")
		s_rel = secant_custom(f1, 0.0, 1.0, tol=tol, criterion="relative")
		print(f"Tol={tol:>8.1e}")
		summarize("  Secant Ea", s_abs)
		summarize("  Secant Er", s_rel)

	# Example 2: f(x) = x^3 - x - 2, root ~ 1.5213797
	f2 = lambda x: x**3 - x - 2
	df2 = lambda x: 3*x**2 - 1

	print("\nExample 2: f(x) = x^3 - x - 2 (root ~ 1.52138)\n")
	n_abs = newton_custom(f2, df2, 1.0, tol=1e-6, criterion="absolute")
	n_rel = newton_custom(f2, df2, 1.0, tol=1e-6, criterion="relative")
	summarize("  Newton Ea", n_abs)
	summarize("  Newton Er", n_rel)

	# Example 3: root near zero to highlight difference
	# f(x) = sin(x), root at x=0. Relative error can be misleading near zero.
	f3 = lambda x: np.sin(x)
	df3 = lambda x: np.cos(x)

	print("\nExample 3: f(x) = sin(x) (root at 0)\n")
	n_abs0 = newton_custom(f3, df3, 0.3, tol=1e-6, criterion="absolute")
	n_rel0 = newton_custom(f3, df3, 0.3, tol=1e-6, criterion="relative")
	summarize("  Newton Ea", n_abs0)
	summarize("  Newton Er", n_rel0)

	# Print a small table for one run to illustrate step-wise Ea and Er
	print("\nDetailed iteration table (Secant on e^{-x}-x, tol=1e-3, Ea criterion):")
	rows = secant_custom(f1, 0.0, 1.0, tol=1e-3, criterion="absolute")
	print(f"{'k':<4} {'x_k':>12} {'x_{k+1}':>12} {'Ea':>12} {'Er':>12}")
	for (k, xk, xk1, fk, Ea, Er) in rows:
		print(f"{k:<4} {xk:>12.8f} {xk1:>12.8f} {Ea:>12.3e} {Er:>12.3e}")


if __name__ == "__main__":
	start = time.perf_counter()
	run_examples()
	end = time.perf_counter()
	print(f"\nCompleted in {(end-start)*1e3:.2f} ms")

