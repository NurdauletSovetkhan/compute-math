from table import print_table
from graph import make_plot
from tabulate import tabulate
from methods.bisection import bisection
from methods.fixed_point import fixed_point
from methods.newton_raphson import newton
from methods.secant import secant
from methods.false_point import false_point
import math


func = lambda x: math.exp(x) - x**2
gx = lambda x: -math.exp(x/2)  # -e^(x/2) -> e^x = x^2 => x = -sqrt(e^x) = -e^(x/2) 
dfunc = lambda x: math.exp(x) - 2*x

a, b = -2, 0.0     # Now f(a) and f(b) have different signs


# Tolerances
tolerance = 1e-3
max_iter = 50

b_table = bisection(func, a, b, tolerance, max_iter)
fp_table = fixed_point(gx, a, tolerance, max_iter)
newton_table = newton(func, dfunc, b, tolerance, max_iter)
secant_table = secant(func, a, b, tolerance, max_iter)
false_table = false_point(func, a, b, tolerance, max_iter)

max_len = max(len(b_table), len(fp_table), len(newton_table), len(secant_table), len(false_table))

print_table(b_table, fp_table, newton_table, secant_table, false_table, max_len)

# Find the root value from the last iterations
x_star = newton_table[-1][2] if newton_table else b_table[-1][1]

# Prepare data for plots
results = {
    "Bisection": [row[1] for row in b_table],
    "False Position": [row[1] for row in false_table],
    "Fixed-Point": [row[1] for row in fp_table],
    "Newton-Raphson": [row[2] for row in newton_table],  # Newton uses row[2] for x1
    "Secant": [row[2] for row in secant_table],  # Secant uses row[2] for x1
}


# Build the plots
make_plot(results, x_star, func_name="$f(x) = e^x - x^2$")