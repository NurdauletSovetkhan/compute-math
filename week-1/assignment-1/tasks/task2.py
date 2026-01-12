# equation is e**x = x**2
import math
import matplotlib.pyplot as plt
import numpy as np
from methods.bisection import bisection
def func(x):
    return math.exp(x) - x**2


def f1(x):
    return np.tan(x) - x**2

def f2(x):
    return x**3 - 2*x - 5

max_iters = 20
root1 = bisection(f1, 0.5, 1.5, 1e-3, max_iterations=max_iters)
root2 = bisection(f2, 2, 3, 1e-3, max_iterations=max_iters)
max_len = max(len(root1), len(root2))

print("Iter  Root of f1   Root of f2")
for i in range(max_len):
    row = [
        f"{i+1}   ",
        f"  {root1[i][1]:.4f}  " if i < len(root1) else " -        ",
        f" {root2[i][1]:.4f}    " if i < len(root2) else " -         ",
    ]
    print("  ".join(str(x) for x in row))


    