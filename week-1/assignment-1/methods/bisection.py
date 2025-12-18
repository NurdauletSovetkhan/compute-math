import numpy as np

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