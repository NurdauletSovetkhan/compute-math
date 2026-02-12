"""
Main program for Curve Fitting Models.
Runs all models on input data and finds the best fit.
"""

import sys
import os
import math
import ast

# --- CHEAT MODE IMPORTS ---
try:
    import numpy as np
    from scipy.optimize import curve_fit
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("Warning: numpy or scipy not installed. Cheat mode will be disabled.")
# ---------------------------

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from methods import StraightLine, Quadratic, Cubic, Exponential, ExponentialABx, Logarithmic, Power
from table import display_results_table, display_data_table
from graph import plot_best_model, plot_all_models
from examples import get_all_examples, get_example

# All available standard models
ALL_MODELS = [
    ('Straight Line', StraightLine),
    ('Quadratic (2nd degree)', Quadratic),
    ('Cubic (3rd degree)', Cubic),
    ('Exponential', Exponential),
    ('Exponential (a·b^x)', ExponentialABx),
    ('Logarithmic', Logarithmic),
    ('Power', Power)
]

# ==============================================================================
#  SCIPY CHEAT MODELS (True Non-Linear Least Squares)
# ==============================================================================

class ScipyModelBase:
    """Base wrapper for Scipy models to match the existing interface."""
    def __init__(self, name):
        self.name = name
        self.popt = None
    
    def fit(self, x, y):
        # Convert to numpy arrays for scipy
        x_arr = np.array(x, dtype=float)
        y_arr = np.array(y, dtype=float)
        try:
            # curve_fit returns optimal parameters (popt) and covariance (pcov)
            self.popt, _ = curve_fit(self._func, x_arr, y_arr, maxfev=10000)
        except Exception as e:
            raise RuntimeError(f"Scipy convergence failed: {e}")

    def get_sse(self, x, y):
        if self.popt is None: return float('inf')
        x_arr = np.array(x, dtype=float)
        y_arr = np.array(y, dtype=float)
        y_pred = self._func(x_arr, *self.popt)
        return np.sum((y_arr - y_pred) ** 2)

    def get_coefficients(self):
        return {f'p{i}': p for i, p in enumerate(self.popt)} if self.popt is not None else {}

class ScipyExponential(ScipyModelBase):
    def __init__(self):
        super().__init__("Exponential (Scipy/True Fit)")
    
    def _func(self, x, a, b):
        return a * np.exp(b * x)
    
    def get_equation_string(self):
        a, b = self.popt
        return f"y = {a:.5f}·e^({b:.5f}x)"
class ScipyExponentialABx(ScipyModelBase):
    def __init__(self):
        super().__init__("Exponential (a*b^x)")
    
    def _func(self, x, a, b):
        # Именно та форма, которая в задаче
        return a * np.power(b, x)
    
    def get_equation_string(self):
        if self.popt is None: return "Model not fitted"
        a, b = self.popt
        return f"y = {a:.4f}({b:.4f})^x"
class ScipyPower(ScipyModelBase):
    def __init__(self):
        super().__init__("Power (Scipy/True Fit)")
    
    def _func(self, x, a, b):
        return a * np.power(x, b)
        
    def get_equation_string(self):
        a, b = self.popt
        return f"y = {a:.5f}·x^({b:.5f})"

class ScipyLogarithmic(ScipyModelBase):
    def __init__(self):
        super().__init__("Logarithmic (Scipy)")
        
    def _func(self, x, a, b):
        return a + b * np.log(x)
        
    def get_equation_string(self):
        a, b = self.popt
        sign = "+" if b >= 0 else "-"
        return f"y = {a:.5f} {sign} {abs(b):.5f}·ln(x)"

# We can also wrap polynomials for consistency, though np.polyfit is usually fine
class ScipyPoly(ScipyModelBase):
    def __init__(self, degree, name):
        super().__init__(name)
        self.degree = degree
        
    def _func(self, x, *coeffs):
        # Construct polynomial: c0 + c1*x + c2*x^2 ...
        # Note: Scipy curve_fit args must be explicit, so we use a dynamic wrapper or fixed
        return np.polyval(list(reversed(coeffs)), x) 
        
    def fit(self, x, y):
        # Use simple polyfit for polynomials as it's stable
        self.popt = np.polyfit(x, y, self.degree)[::-1] # reverse to match c0, c1...

    def get_equation_string(self):
        coeffs = self.popt
        terms = []
        for i, c in enumerate(coeffs):
            if i == 0: terms.append(f"{c:.4f}")
            elif i == 1: terms.append(f"{c:+.4f}x")
            else: terms.append(f"{c:+.4f}x^{i}")
        return "y = " + "".join(terms)


# List of Scipy Cheat Models
SCIPY_MODELS = [
    ('Exponential (Scipy)', ScipyExponential),
    ('Power (Scipy)', ScipyPower),
    ('Logarithmic (Scipy)', ScipyLogarithmic),
    ('Exponential like ab^x', ScipyExponentialABx)
    # ('Quadratic (Scipy)', lambda: ScipyPoly(2, "Quadratic (Scipy)")), # Optional
]

# ==============================================================================
#  END CHEAT MODELS
# ==============================================================================


def _safe_eval_math(expr: str) -> float:
    """Safely evaluate a simple math expression (numbers, + - * / **, parentheses, e, pi)."""
    allowed_names = {
        'e': math.e,
        'pi': math.pi,
    }
    allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Constant,
        ast.Name,
        ast.Load,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Pow,
        ast.USub,
        ast.UAdd,
    )

    node = ast.parse(expr, mode='eval')

    for subnode in ast.walk(node):
        if not isinstance(subnode, allowed_nodes):
            raise ValueError(f"Unsupported expression: {expr}")
        if isinstance(subnode, ast.Name) and subnode.id not in allowed_names:
            raise ValueError(f"Unknown symbol '{subnode.id}' in: {expr}")
        if isinstance(subnode, ast.Constant) and not isinstance(subnode.value, (int, float)):
            raise ValueError(f"Invalid constant in: {expr}")

    return float(eval(compile(node, '<expr>', 'eval'), {'__builtins__': {}}, allowed_names))


def parse_input(input_str: str) -> list:
    """Parse space-separated numbers or simple math expressions from input string."""
    try:
        tokens = input_str.strip().split()
        values = [
            _safe_eval_math(token.replace('^', '**'))
            for token in tokens
        ]
        return values
    except ValueError as e:
        raise ValueError(f"Invalid number format: {e}")


def validate_data(x_data: list, y_data: list) -> tuple:
    """Validate input data for curve fitting."""
    if not x_data or not y_data:
        return False, "Error: Data arrays cannot be empty!"
    if len(x_data) != len(y_data):
        return False, f"Error: Number of x values ({len(x_data)}) must match number of y values ({len(y_data)})!"
    if len(x_data) < 2:
        return False, "Error: At least 2 data points are required!"
    if len(x_data) != len(set(x_data)):
        duplicates = [x for x in set(x_data) if x_data.count(x) > 1]
        return False, f"Error: x values must be unique! Duplicate values found: {duplicates}"
    return True, ""


def get_models_by_indices(indices: list) -> list:
    """Get model instances by their indices (1-based)."""
    models = []
    for idx in indices:
        if 1 <= idx <= len(ALL_MODELS):
            models.append(ALL_MODELS[idx - 1][1]())  # Create instance
    return models


def fit_models(x_data: list, y_data: list, models: list):
    """Fit specified models to the data and return results."""
    results = []
    fitted_models = []
    
    for model in models:
        try:
            model.fit(x_data, y_data)
            sse = model.get_sse(x_data, y_data)
            
            results.append({
                'name': model.name,
                'equation': model.get_equation_string(),
                'sse': sse,
                'coefficients': model.get_coefficients()
            })
            fitted_models.append(model)
        except Exception as e:
            print(f"Warning: {model.name} fitting failed: {e}")
            results.append({
                'name': model.name,
                'equation': "N/A (fitting failed)",
                'sse': float('inf'),
                'coefficients': {}
            })
    
    return results, fitted_models


def fit_all_models(x_data: list, y_data: list):
    """Fit all standard models."""
    models = [model_class() for _, model_class in ALL_MODELS]
    return fit_models(x_data, y_data, models)


def run_with_data(x_data: list, y_data: list, models: list = None, show_graph: bool = True):
    """Run curve fitting with given data."""
    is_valid, error_msg = validate_data(x_data, y_data)
    if not is_valid:
        print(error_msg)
        return
    
    display_data_table(x_data, y_data)
    
    if models is None:
        results, fitted_models = fit_all_models(x_data, y_data)
    else:
        results, fitted_models = fit_models(x_data, y_data, models)
    
    display_results_table(results)
    
    if show_graph and fitted_models:
        best_result = min(results, key=lambda r: r['sse'])
        best_idx = results.index(best_result)
        best_model = fitted_models[best_idx]
        plot_best_model(x_data, y_data, best_model, 
                       title=f"Best Fit: {best_model.name} (SSE = {best_result['sse']:.4f})")


def interactive_input():
    """Get data from user input."""
    try:
        print("\nEnter x values (space-separated):")
        x_str = input("> ")
        x_data = parse_input(x_str)
        
        print("Enter y values (space-separated):")
        y_str = input("> ")
        y_data = parse_input(y_str)
        
        return x_data, y_data
    except ValueError as e:
        raise ValueError(f"Input parsing error: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error during input: {e}")


def select_models_menu():
    """Display model selection menu."""
    print("SELECT MODELS:")
    for i, (name, _) in enumerate(ALL_MODELS, 1):
        print(f"  {i}. {name}")
    print(f"  A. All models")
    
    print("Enter model numbers (comma or space separated)")
    choice = input("> ").strip().upper()
    
    if choice == 'A':
        return [model_class() for _, model_class in ALL_MODELS]
    
    try:
        choice = choice.replace(',', ' ')
        indices = [int(x) for x in choice.split()]
        models = get_models_by_indices(indices)
        if not models:
            return [model_class() for _, model_class in ALL_MODELS]
        print(f"Selected: {', '.join(m.name for m in models)}")
        return models
    except ValueError:
        return [model_class() for _, model_class in ALL_MODELS]


def show_menu():
    """Display main menu and handle user choice."""
    while True:
        print("       CURVE FITTING - ASSIGNMENT 3")
        
        examples = get_all_examples()
        for i, ex in enumerate(examples, 1):
            print(f"  {i}. {ex['name']}")
            print(f"     {ex['description']}")
        
        n = len(examples)
        print(f"  {n + 1}. Enter custom data (all models)")
        print(f"  {n + 2}. Enter custom data (select models)")
        if SCIPY_AVAILABLE:
            print(f"  {n + 3}. [CHEAT] Scipy Mode (True Non-Linear Fit)")
        
        print(f"  0. Exit")
        
        try:
            choice = int(input("Choose option: "))
        except ValueError:
            print("Invalid input.")
            continue
        
        if choice == 0:
            print("Goodbye!")
            break
        elif 1 <= choice <= n:
            ex = get_example(choice)
            print(f"\n>>> Running: {ex['name']}")
            run_with_data(ex['x'], ex['y'])
        elif choice == n + 1:
            try:
                x_data, y_data = interactive_input()
                run_with_data(x_data, y_data)
            except Exception as e:
                print(f"Error: {e}")
        elif choice == n + 2:
            try:
                x_data, y_data = interactive_input()
                models = select_models_menu()
                run_with_data(x_data, y_data, models=models)
            except Exception as e:
                print(f"Error: {e}")
        elif SCIPY_AVAILABLE and choice == n + 3:
            # --- CHEAT MODE EXECUTION ---
            print("\n>>> ACTIVATING SCIPY CHEAT MODE <<<")
            print("Using non-linear least squares optimization (scipy.optimize.curve_fit)")
            try:
                x_data, y_data = interactive_input()
                # Create instances of Scipy models
                scipy_models = [m_cls() for _, m_cls in SCIPY_MODELS]
                run_with_data(x_data, y_data, models=scipy_models)
            except Exception as e:
                print(f"Error in Cheat Mode: {e}")
        else:
            print("Invalid option.")


def main():
    print("\n" + "*" * 46)
    print("* Curve Fitting Models - Least Squares Method  *")
    print("*" * 46 + "\n")
    show_menu()


if __name__ == "__main__":
    main()