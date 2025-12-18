import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0.5, 1.5, 500)

# Define the functions
y1 = np.tan(x)
y2 = x**2
f = y1 - y2

plt.figure(figsize=(10, 6))
plt.plot(x, y1, label=r'$y = \tan(x)$', linewidth=2)
plt.plot(x, y2, label=r'$y = x^2$', linewidth=2)

plt.xlabel('x')
plt.ylabel('y')
plt.title(r'Graphical analysis of $\tan(x) = x^2$ on $[0.5, 1.5]$')
plt.legend()
plt.grid(True, alpha=0.3)

plt.xlim(0.5, 1.5)
plt.ylim(0, 5)

plt.tight_layout()
plt.savefig("task1_plot.png")

# Numerical check
print("\nChecking the difference f(x) = tan(x) - x^2 on [0.5, 1.5]:")
print(f"Minimum value of f(x): {np.min(f):.6f}")
print(f"Maximum value of f(x): {np.max(f):.6f}")

if np.min(f) > 0:
    print("\nConclusion:")
    print("tan(x) > x^2 for all x in [0.5, 1.5].")
    print("Therefore, NO intersection exists in this interval.")
else:
    print("\nConclusion:")
    print("An intersection exists in the interval.")
