import matplotlib.pyplot as plt
import numpy as np


def make_plot(results: dict, x_star: float, func_name: str = "f(x)"):
  # Styles for each method
  styles = {
    "Bisection": {"color": "tab:blue", "marker": "o"},
    "False Position": {"color": "tab:orange", "marker": "s"},
    "Fixed-Point": {"color": "tab:green", "marker": "^"},
    "Newton-Raphson": {"color": "tab:red", "marker": "D"},
    "Secant": {"color": "tab:purple", "marker": "v"},
  }

  fig, ax = plt.subplots(figsize=(10, 6))

  # Plot approximations
  for name, xs in results.items():
    if xs:  # Check that list is not empty
      iters = list(range(len(xs)))
      style = styles.get(name, {})
      ax.plot(iters, xs, label=name, **style, linewidth=1.5, markersize=5)

  ax.axhline(y=x_star, color="black", linestyle="--", linewidth=1.2, label="$x^*$")
  ax.set_ylabel("Approximation $x_i$", fontsize=12)
  ax.set_xlabel("Iteration", fontsize=12)
  ax.set_title(f"Approximation Comparison for {func_name}", fontsize=14, fontweight='bold')
  ax.legend(loc='best')
  ax.grid(True, which="both", linestyle=":", alpha=0.6)

  plt.tight_layout()
  plt.savefig("approximation_comparison.png")
