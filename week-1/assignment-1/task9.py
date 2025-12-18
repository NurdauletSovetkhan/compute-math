import numpy as np
import matplotlib.pyplot as plt

from methods.bisection import bisection
from methods.false_point import false_point
from methods.fixed_point import fixed_point
from methods.newton_raphson import newton
from methods.secant import secant


def f(x: float) -> float:
	return x**3 - 2 * x - 5


def df(x: float) -> float:
	return 3 * x**2 - 2


def g(x: float) -> float:
	return np.cbrt(2 * x + 5)


def extract_xi_from_table(method_name: str, row: tuple) -> float:
	if method_name in ("bisection", "false_position"):
		return row[1]
	elif method_name == "fixed_point":
		return row[2]
	elif method_name in ("newton", "secant"):
		return row[2]
	else:
		raise ValueError(f"Unknown method: {method_name}")


def run_methods_and_collect(x_star: float):
	epsilon = 1e-8
	max_iter = 1000

	results = {}

	# Bisection [2, 3]
	bis_table = bisection(f, 2.0, 3.0, epsilon, max_iterations=max_iter)
	results["Bisection"] = [extract_xi_from_table("bisection", r) for r in bis_table]

	# False Position [2, 3]
	fp_table = false_point(f, 2.0, 3.0, epsilon=epsilon, max_iterations=max_iter)
	results["False Position"] = [extract_xi_from_table("false_position", r) for r in fp_table]

	# Fixed-Point x0 = 3 (g(x) = cbrt(2x + 5))
	fpit_table = fixed_point(g, 3.0, eps=epsilon, max_iter=max_iter)
	results["Fixed-Point"] = [extract_xi_from_table("fixed_point", r) for r in fpit_table]

	# Newton-Raphson x0 = 3
	newt_table = newton(f, df, 3.0, epsilon=epsilon, max_iterations=max_iter)
	results["Newton-Raphson"] = [extract_xi_from_table("newton", r) for r in newt_table]

	# Secant x0 = 2, x1 = 3
	sec_table = secant(f, 2.0, 3.0, epsilon=epsilon, max_iterations=max_iter)
	results["Secant"] = [extract_xi_from_table("secant", r) for r in sec_table]

	# Also compute errors per method
	errors = {name: [abs(xi - x_star) for xi in xis] for name, xis in results.items()}

	return results, errors


def make_plot(results: dict, errors: dict, x_star: float):
	# Prepare styles
	styles = {
		"Bisection": {"color": "tab:blue", "marker": "o"},
		"False Position": {"color": "tab:orange", "marker": "s"},
		"Fixed-Point": {"color": "tab:green", "marker": "^"},
		"Newton-Raphson": {"color": "tab:red", "marker": "D"},
		"Secant": {"color": "tab:purple", "marker": "v"},
	}

	fig, axes = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

	ax1 = axes[0]
	for name, xs in results.items():
		iters = list(range(len(xs)))
		style = styles.get(name, {})
		ax1.plot(iters, xs, label=name, **style)

	ax1.axhline(y=x_star, color="black", linestyle="--", linewidth=1.2, label="$x^*$")
	ax1.set_ylabel("Approximation $x_i$")
	ax1.set_title("Convergence Comparison for $f(x) = x^3 - 2x - 5$")
	ax1.legend()
	ax1.grid(True, which="both", linestyle=":", alpha=0.6)

	ax2 = axes[1]
	for name, errs in errors.items():
		iters = list(range(len(errs)))
		style = styles.get(name, {})
		ax2.plot(iters, errs, label=name, **style)

	ax2.set_yscale("log")
	ax2.set_xlabel("Iteration i")
	ax2.set_ylabel(r"Error $|x_i - x^*|$")
	ax2.legend()
	ax2.grid(True, which="both", linestyle=":", alpha=0.6)

	plt.tight_layout()
	plt.savefig("convergence_comparison.png")


def main():
	x_star = 2.0945514815
	results, errors = run_methods_and_collect(x_star)
	make_plot(results, errors, x_star)


if __name__ == "__main__":
	main()

