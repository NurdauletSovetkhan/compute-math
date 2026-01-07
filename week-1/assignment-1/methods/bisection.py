import numpy as np

# Bisection Method
# The idea is pretty simple: if f(a) and f(b) have opposite signs, there must be a root somewhere between them.
# We just keep cutting the interval in half, checking which half contains the root, and repeat.
# Its slow but super reliable - it always converges if there is a root in [a, b].

def bisection(func, a, b, epsilon, max_iterations):
    if func(a) * func(b) > 0:
        print("No root in the interval")
        return []

    table = []
    counter = 0

    while abs(b - a) > epsilon and counter < max_iterations:
        c = (a + b) / 2
        fc = func(c)
        table.append((counter, c, fc))
        counter += 1

        if func(a) * fc < 0:
            b = c
        else:
            a = c

    return table

if __name__ == "__main__":
    func = lambda x: np.tan(x) - x**2
    epsilon = 1e-3
    a = float(input("a: "))
    b = float(input("b: "))
    print("The answer is:", bisection(func, a, b, epsilon))