from table import print_table
from graph import make_plot
from tabulate import tabulate
from methods.bisection import bisection
from methods.fixed_point import fixed_point
from methods.newton_raphson import newton
from methods.secant import secant
from methods.false_point import false_point
import math
import re

# Dictionary of available methods
METHODS = {
    '1': ('Bisection', bisection, ['func', 'a', 'b']),
    '2': ('Fixed Point', fixed_point, ['gx', 'x0']),
    '3': ('Newton-Raphson', newton, ['func', 'dfunc', 'x0']),
    '4': ('Secant', secant, ['func', 'x0', 'x1']),
    '5': ('False Position', false_point, ['func', 'a', 'b']),
}

# Predefined functions for quick testing
EXAMPLE_FUNCTIONS = {
    '1': {
        'name': 'x³ - x - 2 = 0',
        'func': lambda x: x**3 - x - 2,
        'dfunc': lambda x: 3*x**2 - 1,
        'gx': lambda x: (x + 2)**(1/3),
        'interval': (1, 2),
        'x0': 1.5
    },
    '2': {
        'name': 'ln(x) + x - 2 = 0',
        'func': lambda x: math.log(x) + x - 2,
        'dfunc': lambda x: (1/x) + 1,
        'gx': lambda x: 2 - math.log(x),
        'interval': (1, 2),
        'x0': 1.5
    },
    '3': {
        'name': 'cos(x) - x = 0',
        'func': lambda x: math.cos(x) - x,
        'dfunc': lambda x: -math.sin(x) - 1,
        'gx': lambda x: math.cos(x),
        'interval': (0, 1),
        'x0': 0.5
    },
    '4': {
        'name': 'e^x - x² = 0',
        'func': lambda x: math.exp(x) - x**2,
        'dfunc': lambda x: math.exp(x) - 2*x,
        'gx': lambda x: math.log(x**2) if x > 0 else 0,
        'interval': (-1, 1),
        'x0': 0.5
    },
}


def numerical_derivative(func, h=1e-5):
    """
    Create numerical derivative function using central differences
    f'(x) ≈ (f(x + h) - f(x - h)) / (2h)
    """
    def dfunc(x):
        try:
            return (func(x + h) - func(x - h)) / (2 * h)
        except:
            # Fallback to forward difference if central fails
            try:
                return (func(x + h) - func(x)) / h
            except:
                return 0
    return dfunc


def create_fixed_point_function(func, x0, alpha=0.1):
    """
    Create g(x) for fixed-point iteration from f(x)
    g(x) = x - alpha * f(x)
    Alpha is chosen to ensure convergence near x0
    """
    def gx(x):
        try:
            return x - alpha * func(x)
        except:
            return x
    return gx


def parse_function(func_str):
    """Parse user-input function string into Python lambda"""
    try:
        # Replace common math notations (order matters!)
        func_str = func_str.replace('^', '**')
        func_str = func_str.replace('sqrt', 'math.sqrt')
        func_str = func_str.replace('sin', 'math.sin')
        func_str = func_str.replace('cos', 'math.cos')
        func_str = func_str.replace('tan', 'math.tan')
        func_str = func_str.replace('exp', 'math.exp')
        
        # Handle log functions: both ln and log mean natural logarithm
        func_str = func_str.replace('ln(', 'math.log(')
        if 'log(' in func_str and 'math.log(' not in func_str:
            func_str = func_str.replace('log(', 'math.log(')
        
        # Create lambda function
        func = eval(f"lambda x: {func_str}")
        
        # Test the function
        func(1.0)
        return func
    except Exception as e:
        print(f"Error parsing function: {e}")
        return None



def select_methods():
    """Let user select methods to use"""
    print("\nAVAILABLE METHODS:")
    print("1. Bisection (requires interval [a,b])")
    print("2. Fixed Point (requires g(x) and x0)")
    print("3. Newton-Raphson (requires f(x), f'(x), and x0)")
    print("4. Secant (requires f(x), x0, and x1)")
    print("5. False Position (requires interval [a,b])")
    print("0. All methods")
    
    choice = input("\nSelect methods (comma-separated, e.g., '1,3,4' or '0' for all): ").strip()
    
    if choice == '0':
        return list(METHODS.keys())
    
    selected = [c.strip() for c in choice.split(',') if c.strip() in METHODS]
    return selected if selected else None


def get_parameters():
    """Get common parameters from user"""
    print("\nPARAMETERS:")
    try:
        tol = input("Tolerance (default 1e-6): ").strip()
        tolerance = float(tol) if tol else 1e-6
        
        max_it = input("Max iterations (default 50): ").strip()
        max_iter = int(max_it) if max_it else 50
        
        return tolerance, max_iter
    except ValueError:
        print("Invalid input, using defaults.")
        return 1e-6, 50


def solve_with_methods(func, dfunc, gx, methods, a, b, x0, x1, tolerance, max_iter):
    """Solve equation using selected methods"""
    results = {}
    tables = {}
    
    print("\n" + "=" * 80)
    print("SOLVING...")
    print("=" * 80)
    
    for method_id in methods:
        method_name, method_func, required_params = METHODS[method_id]
        print(f"\n{method_name}:")
        
        try:
            if method_id == '1':  # Bisection
                table = method_func(func, a, b, tolerance, max_iter)
                root = table[-1][1] if table else None
            elif method_id == '2':  # Fixed Point
                if gx is None:
                    print("  Skipped: g(x) not provided")
                    continue
                table = method_func(gx, x0, tolerance, max_iter)
                root = table[-1][1] if table else None
            elif method_id == '3':  # Newton-Raphson
                if dfunc is None:
                    print("  Skipped: f'(x) not provided")
                    continue
                table = method_func(func, dfunc, x0, tolerance, max_iter)
                root = table[-1][2] if table else None
            elif method_id == '4':  # Secant
                table = method_func(func, x0, x1, tolerance, max_iter)
                root = table[-1][2] if table else None
            elif method_id == '5':  # False Position
                table = method_func(func, a, b, tolerance, max_iter)
                root = table[-1][1] if table else None
            
            if table:
                tables[method_name] = table
                results[method_name] = root
                iterations = len(table)
                print(f"  Root found: x = {root:.6f}")
                print(f"  Iterations: {iterations}")
                print(f"  f(x) = {func(root):.2e}")
            else:
                print(f"  Failed to converge")
                
        except Exception as e:
            print(f"  Error: {e}")
    
    # Always show detailed iteration table
    if tables:
        print("\n" + "=" * 80)
        print("DETAILED ITERATION TABLE")
        print("=" * 80)
        
        # Get table values for print_table function
        b_table = tables.get('Bisection', [])
        fp_table = tables.get('Fixed Point', [])
        newton_table = tables.get('Newton-Raphson', [])
        secant_table = tables.get('Secant', [])
        false_table = tables.get('False Position', [])
        
        max_len = max(len(table) for table in tables.values())
        print_table(b_table, fp_table, newton_table, secant_table, false_table, max_len)
    
    return results, tables


def print_comparison(results):
    """Print comparison of all methods"""
    if not results:
        print("\nNo results to compare.")
        return
    
    print("\n" + "=" * 80)
    print("COMPARISON OF METHODS")
    print("=" * 80)
    
    table_data = []
    for method, root in results.items():
        table_data.append([method, f"{root:.8f}"])
    
    print(tabulate(table_data, headers=["Method", "Root"], tablefmt="grid"))
    
    # Calculate differences
    if len(results) > 1:
        roots = list(results.values())
        max_diff = max(roots) - min(roots)
        print(f"\nMaximum difference between methods: {max_diff:.2e}")


def plot_results(results, tables, func, func_name="f(x)"):
    """Generate comparison plots"""
    if not results:
        print("\nNo results to plot.")
        return
    
    # Prepare data for plotting
    plot_data = {}
    x_star = list(results.values())[0]  # Use first result as reference
    
    for method_name, table in tables.items():
        if method_name in ["Newton-Raphson", "Secant"]:
            plot_data[method_name] = [row[2] for row in table]
        else:
            plot_data[method_name] = [row[1] for row in table]
    
    try:
        make_plot(plot_data, x_star, func_name=func_name)
        print("\nPlot generated successfully!")
    except Exception as e:
        print(f"\nError generating plot: {e}")


def main():
    print("=" * 60)
    print("      ROOT FINDING METHODS SOLVER")
    print("=" * 60)
    print("\nAvailable Methods:")
    print("  Bisection | Fixed Point | Newton-Raphson | Secant | False Position")
    
    while True:
        print("\n" + "-" * 40)
        print("MAIN MENU:")
        print("-" * 40)
        print("1. Use example function")
        print("2. Enter custom function")
        print("3. Compare all methods on example")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            # Select example function
            print("\nEXAMPLE FUNCTIONS:")
            for key, ex in EXAMPLE_FUNCTIONS.items():
                print(f"{key}. {ex['name']}")
            
            ex_choice = input("\nSelect function (1-4): ").strip()
            if ex_choice not in EXAMPLE_FUNCTIONS:
                print("Invalid choice!")
                continue
            
            example = EXAMPLE_FUNCTIONS[ex_choice]
            func = example['func']
            dfunc = example['dfunc']
            gx = example['gx']
            a, b = example['interval']
            x0 = example['x0']
            x1 = b
            
            print(f"\nSelected: {example['name']}")
            print(f"Interval: [{a}, {b}]")
            print(f"Initial guess: x0 = {x0}")
            
            # Select methods
            methods = select_methods()
            if not methods:
                print("Please select at least one method!")
                continue
            
            # Get parameters
            tolerance, max_iter = get_parameters()
            
            # Solve
            results, tables = solve_with_methods(
                func, dfunc, gx, methods, a, b, x0, x1, tolerance, max_iter
            )
            
            # Display results
            print_comparison(results)
            
            # Ask about plotting
            plot_choice = input("\nGenerate comparison plot? (y/n): ").strip().lower()
            if plot_choice == 'y':
                plot_results(results, tables, func, example['name'])
        
        elif choice == '2':
            # Custom function
            print("\nENTER CUSTOM FUNCTION:")
            print("Use 'x' as variable. Examples:")
            print("  x**3 - x - 2")
            print("  math.log(x) + x - 2")
            print("  math.cos(x) - x")
            
            func_str = input("\nf(x) = ").strip()
            func = parse_function(func_str)
            
            if func is None:
                print("Invalid function!")
                continue
            
            # Select methods first to know what we need
            methods = select_methods()
            if not methods:
                print("Please select at least one method!")
                continue
            
            # Determine what inputs we need
            need_interval = any(METHODS[m][0] in ['Bisection', 'False Position'] for m in methods)
            need_derivative = '3' in methods
            need_gx = '2' in methods
            need_x0 = any(m in ['2', '3', '4'] for m in methods)
            need_x1 = '4' in methods
            
            # Get required inputs
            dfunc = None
            gx = None
            a, b, x0, x1 = 0, 1, 0.5, 1.0
            
            if need_interval:
                try:
                    a = float(input("\nEnter interval start (a): ").strip())
                    b = float(input("Enter interval end (b): ").strip())
                except ValueError:
                    print("Invalid interval!")
                    continue
            
            if need_x0:
                try:
                    x0 = float(input("\nEnter initial guess (x0): ").strip())
                except ValueError:
                    print("Invalid x0!")
                    continue
            
            if need_x1:
                try:
                    x1 = float(input("Enter second initial guess (x1): ").strip())
                except ValueError:
                    print("Invalid x1!")
                    continue
            
            if need_derivative:
                print("\nAutomatically computing derivative using numerical differentiation...")
                dfunc = numerical_derivative(func)
            
            if need_gx:
                print("\nAutomatically creating g(x) for fixed-point iteration...")
                gx = create_fixed_point_function(func, x0)
            
            # Get parameters
            tolerance, max_iter = get_parameters()
            
            # Solve
            results, tables = solve_with_methods(
                func, dfunc, gx, methods, a, b, x0, x1, tolerance, max_iter
            )
            
            # Display results
            print_comparison(results)
            
            # Ask about plotting
            plot_choice = input("\nGenerate comparison plot? (y/n): ").strip().lower()
            if plot_choice == 'y':
                plot_results(results, tables, func, f"f(x) = {func_str}")
        
        elif choice == '3':
            # Compare all methods on example
            print("\nSELECT EXAMPLE FUNCTION:")
            for key, ex in EXAMPLE_FUNCTIONS.items():
                print(f"{key}. {ex['name']}")
            
            ex_choice = input("\nSelect function (1-4): ").strip()
            if ex_choice not in EXAMPLE_FUNCTIONS:
                print("Invalid choice!")
                continue
            
            example = EXAMPLE_FUNCTIONS[ex_choice]
            func = example['func']
            dfunc = example['dfunc']
            gx = example['gx']
            a, b = example['interval']
            x0 = example['x0']
            x1 = b
            
            print(f"\nComparing all methods on: {example['name']}")
            
            tolerance, max_iter = get_parameters()
            
            # Use all methods
            methods = list(METHODS.keys())
            
            results, tables = solve_with_methods(
                func, dfunc, gx, methods, a, b, x0, x1, tolerance, max_iter
            )
            
            # Display full comparison table
            if tables:
                max_len = max(len(table) for table in tables.values())
                print("\n" + "=" * 80)
                print("DETAILED ITERATION TABLE")
                print("=" * 80)
                
                # Get table values
                b_table = tables.get('Bisection', [])
                fp_table = tables.get('Fixed Point', [])
                newton_table = tables.get('Newton-Raphson', [])
                secant_table = tables.get('Secant', [])
                false_table = tables.get('False Position', [])
                
                print_table(b_table, fp_table, newton_table, secant_table, false_table, max_len)
            
            print_comparison(results)
            
            # Generate plot
            plot_choice = input("\nGenerate comparison plot? (y/n): ").strip().lower()
            if plot_choice == 'y':
                plot_results(results, tables, func, example['name'])
        
        elif choice == '4':
            print("\nExiting...")
            break
        
        else:
            print("Invalid choice! Please enter 1-4.")


if __name__ == "__main__":
    main()