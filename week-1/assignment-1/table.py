from tabulate import tabulate

def print_table(b_table, fp_table, newton_table, secant_table, false_table, max_len):
    rows = []
    for i in range(max_len):
        rows.append([
            i,
            f"{b_table[i][1]:.6f}" if i < len(b_table) else "-",
            f"{fp_table[i][1]:.6f}" if i < len(fp_table) else "-",
            f"{newton_table[i][1]:.6f}" if i < len(newton_table) else "-",
            f"{secant_table[i][1]:.6f}" if i < len(secant_table) else "-",
            f"{false_table[i][1]:.6f}" if i < len(false_table) else "-",
            # f"{muller_table[i][1]:.6f}" if i < len(muller_table) else "-",
        ])

    print(tabulate(
        rows,
        headers=["Iter", "Bisection", "Fixed-Point", "Newton-Raphson", "Secant", "False-Position", "Muller"],
        tablefmt="grid"
    ))

    print("\nFinal Approximations:")
    if b_table:
        print(f"Bisection: x ≈ {b_table[-1][1]:.5f}")
    if fp_table:
        print(f"Fixed-Point: x ≈ {fp_table[-1][1]:.5f}")
    if newton_table:
        print(f"Newton-Raphson: x ≈ {newton_table[-1][2]:.5f}")
    if secant_table:
        print(f"Secant: x ≈ {secant_table[-1][2]:.5f}")
    if false_table:
        print(f"False-Position: x ≈ {false_table[-1][1]:.5f}")

# if muller_table:
    # print(f"Muller: x ≈ {muller_table[-1][2]:.5f}")

