import numpy as np
from methods.false_point import false_point


def f(x):
	return x**3 - 3*x + 1

a, b = 0.0, 1.0  # f(0)=1 >0, f(1)=-1 <0


iters = false_point(f, a, b, epsilon=0.0, max_iterations=3)

print("False Position (Regula Falsi) for f(x)=x^3-3x+1 on [0,1], 3 iterations")
print(f"{'k':<4} {'c':>12} {'f(c)':>14}")
for k, c, fc in iters:
	print(f"{k:<4} {c:>12.8f} {fc:>14.8f}")

if iters:
	approx = iters[-1][1]
	print("\nApproximation after 3 iterations (3 d.p.): x ≈ {:.3f}".format(approx))
else:
	print("No iterations performed (check interval/sign change).")

