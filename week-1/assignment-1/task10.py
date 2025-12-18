from __future__ import annotations

import math
from typing import List, Tuple

import numpy as np

try:
    from tabulate import tabulate
    _HAS_TABULATE = True
except Exception:  # pragma: no cover
    _HAS_TABULATE = False

from methods.bisection import bisection
from methods.false_point import false_point
from methods.fixed_point import fixed_point
from methods.newton_raphson import newton
from methods.secant import secant


def f(x: float) -> float:
    return math.log(x) + x


def df(x: float) -> float:
    return 1 / x + 1


def g(x: float) -> float:
    return math.exp(-x)


def sequence_bisection(rows: List[Tuple[int, float, float]], a: float) -> List[float]:
    # Start with the first left endpoint as x0 for display purposes
    xs = [a]
    xs.extend(r[1] for r in rows)
    return xs


def sequence_false_position(rows: List[Tuple[int, float, float]], a: float) -> List[float]:
    xs = [a]
    xs.extend(r[1] for r in rows)
    return xs


def sequence_fixed_point(rows: List[Tuple[int, float, float, float]], x0: float) -> List[float]:
    xs = [x0]
    xs.extend(r[2] for r in rows)  # x_next
    return xs


def sequence_newton(rows: List[Tuple[int, float, float, float]], x0: float) -> List[float]:
    xs = [x0]
    xs.extend(r[2] for r in rows)  # x1
    return xs


def sequence_secant(rows: List[Tuple[int, float, float, float]], x0: float, x1: float) -> List[float]:
    xs = [x0, x1]
    cur_x0, cur_x1 = x0, x1
    for _row in rows:
        f0 = f(cur_x0)
        f1 = f(cur_x1)
        denom = (f1 - f0)
        if denom == 0:
            break
        x2 = cur_x1 - f1 * (cur_x1 - cur_x0) / denom
        if not np.isfinite(x2):
            break
        xs.append(x2)
        cur_x0, cur_x1 = cur_x1, x2
    return xs


def build_table():
    # Settings
    a, b = 0.1, 1.0
    x0_single = 0.5
    x0_sec, x1_sec = a, b
    tol = 1e-8
    max_iter = 20

    # Run methods to get iteration histories
    b_rows = bisection(f, a, b, tol, max_iter)
    fp_rows = false_point(f, a, b, epsilon=tol, max_iterations=max_iter)
    fix_rows = fixed_point(g, x0_single, eps=tol, max_iter=max_iter)
    new_rows = newton(f, df, x0_single, epsilon=tol, max_iterations=max_iter)
    sec_rows = secant(f, x0_sec, x1_sec, epsilon=tol, max_iterations=max_iter)

    # Convert to x_i sequences including explicit starting guesses
    xs_b = sequence_bisection(b_rows, a)
    xs_fp = sequence_false_position(fp_rows, a)
    xs_fix = sequence_fixed_point(fix_rows, x0_single)
    xs_new = sequence_newton(new_rows, x0_single)
    xs_sec = sequence_secant(sec_rows, x0_sec, x1_sec)

    # Build a grid of rows: x_i and f(x_i)
    max_len = max(len(xs_b), len(xs_fp), len(xs_fix), len(xs_new), len(xs_sec))

    def fmt(v: float) -> str:
        return f"{v:.6f}"

    table_rows: List[List[str]] = []
    for i in range(max_len):
        # x_i row
        table_rows.append([
            f"x_{i}",
            fmt(xs_b[i]) if i < len(xs_b) else "-",
            fmt(xs_fix[i]) if i < len(xs_fix) else "-",
            fmt(xs_new[i]) if i < len(xs_new) else "-",
            fmt(xs_sec[i]) if i < len(xs_sec) else "-",
            fmt(xs_fp[i]) if i < len(xs_fp) else "-",
        ])
        # f(x_i) row
        table_rows.append([
            f"f(x_{i})",
            fmt(f(xs_b[i])) if i < len(xs_b) else "-",
            fmt(f(xs_fix[i])) if i < len(xs_fix) else "-",
            fmt(f(xs_new[i])) if i < len(xs_new) else "-",
            fmt(f(xs_sec[i])) if i < len(xs_sec) else "-",
            fmt(f(xs_fp[i])) if i < len(xs_fp) else "-",
        ])

    headers = [
        "Iteration",
        "Bisection",
        "Fixed-Point",
        "Newton-Raphson",
        "Secant",
        "False Position",
    ]

    if _HAS_TABULATE:
        print(tabulate(table_rows, headers=headers, tablefmt="grid"))
    else:
        # Simple fallback formatting
        col_widths = [max(len(str(row[c])) for row in ([headers] + table_rows)) for c in range(len(headers))]
        def print_row(row):
            print(" | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)))
        print_row(headers)
        print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
        for row in table_rows:
            print_row(row)

    # Final approximations
    print("\nFinal Approximations (last available x_i):")
    if xs_b: print(f"Bisection: {xs_b[-1]:.10f}")
    if xs_fix: print(f"Fixed-Point: {xs_fix[-1]:.10f}")
    if xs_new: print(f"Newton-Raphson: {xs_new[-1]:.10f}")
    if xs_sec: print(f"Secant: {xs_sec[-1]:.10f}")
    if xs_fp: print(f"False Position: {xs_fp[-1]:.10f}")


if __name__ == "__main__":
    build_table()
