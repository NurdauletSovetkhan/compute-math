"""
Table display utilities for numerical integration results
"""

try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False


def display_integration_result(result: dict, show_points: bool = False):
    """
    Display integration result in a formatted table.
    
    Parameters:
        result: Dictionary containing integration results
        show_points: Whether to display all computed points
    """
    print("\n" + "="*80)
    print(f"INTEGRATION RESULT: {result.get('method', 'Unknown Method')}")
    print("="*80)
    
    # Main results
    data = [
        ["Integral Value", f"{result.get('result', 'N/A'):.10f}"],
        ["Interval", f"[{result.get('a', 'N/A')}, {result.get('b', 'N/A')}]"],
        ["Number of Intervals (n)", result.get('n', 'N/A')],
        ["Step Size (h)", f"{result.get('h', 'N/A'):.10f}"],
        ["Function Evaluations", result.get('function_evaluations', 'N/A')],
    ]
    
    # Add error bound if available
    if 'error_bound' in result:
        data.append(["Error Bound", f"{result['error_bound']:.10e}"])
    
    if 'error' in result and isinstance(result['error'], (int, float)):
        data.append(["Absolute Error", f"{result['error']:.10e}"])
    
    if 'relative_error' in result:
        data.append(["Relative Error", f"{result['relative_error']:.10e}"])
    
    if TABULATE_AVAILABLE:
        print(tabulate(data, headers=["Parameter", "Value"], tablefmt="grid"))
    else:
        for row in data:
            print(f"{row[0]:<30} {row[1]}")
    
    # Display points if requested
    if show_points and 'points' in result:
        display_computation_points(result['points'])
    
    print()


def display_computation_points(points: list, max_display: int = 10):
    """
    Display the points used in computation.
    
    Parameters:
        points: List of (x, f(x)) tuples
        max_display: Maximum number of points to display
    """
    print("\n" + "-"*60)
    print("COMPUTATION POINTS")
    print("-"*60)
    
    if len(points) > max_display:
        display_points = points[:max_display//2] + [('...', '...')] + points[-max_display//2:]
    else:
        display_points = points
    
    if TABULATE_AVAILABLE:
        headers = ["i", "x", "f(x)"]
        table_data = []
        for i, (x, fx) in enumerate(display_points):
            if x == '...':
                table_data.append(['...', '...', '...'])
            else:
                table_data.append([i, f"{x:.6f}", f"{fx:.6f}"])
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    else:
        print(f"{'i':<5} {'x':<20} {'f(x)':<20}")
        print("-" * 60)
        for i, (x, fx) in enumerate(display_points):
            if x == '...':
                print(f"{'...':<5} {'...':<20} {'...':<20}")
            else:
                print(f"{i:<5} {x:<20.6f} {fx:<20.6f}")
    
    if len(points) > max_display:
        print(f"\n(Showing {max_display} of {len(points)} points)")
    
    print()


def display_comparison(results: dict):
    """
    Display comparison of multiple integration methods.
    
    Parameters:
        results: Dictionary mapping method names to result dictionaries
    """
    print("\n" + "="*80)
    print("SUMMARY TABLE")
    print("="*80)
    
    exact_value = results.get('exact_value')
    
    comparison_data = []
    for method_name, result in results.items():
        if method_name == 'exact_value':
            continue
        
        if 'error' in result and isinstance(result['error'], str):
            comparison_data.append([
                method_name,
                "Error",
                "-",
                result['error'],
                "-",
                "-"
            ])
        else:
            n = result.get('n', 'N/A')
            h = result.get('h', 'N/A')
            res = result.get('result', 0)
            
            # Format h and result
            h_str = f"{h:.6f}" if isinstance(h, (int, float)) and h != 'N/A' else str(h)
            res_str = f"{res:.10f}" if isinstance(res, (int, float)) else str(res)
            
            row = [
                method_name,
                str(n),
                h_str,
                res_str,
            ]
            
            if exact_value is not None and 'result' in result:
                error = abs(result['result'] - exact_value)
                rel_error = error / abs(exact_value) if exact_value != 0 else float('inf')
                row.append(f"{error:.10e}")
                row.append(f"{rel_error:.10e}")
            else:
                row.append("-")
                row.append("-")
            
            comparison_data.append(row)
    
    headers = ["Method", "n", "h (Step Size)", "Result", "Absolute Error", "Relative Error"]
    
    if TABULATE_AVAILABLE:
        print(tabulate(comparison_data, headers=headers, tablefmt="grid"))
    else:
        # Print headers
        col_widths = [20, 10, 15, 20, 20, 20]
        header_line = "".join(h.ljust(w) for h, w in zip(headers, col_widths))
        print(header_line)
        print("-" * sum(col_widths))
        
        # Print data
        for row in comparison_data:
            line = "".join(str(val).ljust(w) for val, w in zip(row, col_widths))
            print(line)
    
    if exact_value is not None:
        print(f"\nExact Value: {exact_value:.10f}")
    
    print()


def display_method_info(method_name: str):
    """
    Display information about a specific integration method.
    
    Parameters:
        method_name: Name of the method
    """
    info = {
        'trapezoidal': {
            'name': 'Trapezoidal Rule',
            'formula': '∫[a,b] f(x)dx ≈ h/2 * [f(a) + 2*Σf(xᵢ) + f(b)]',
            'requirements': 'n ≥ 1',
            'error': 'O(h²) or O(1/n²)',
            'best_for': 'Linear functions, quick approximations'
        },
        'simpson_1/3': {
            'name': "Simpson's 1/3 Rule",
            'formula': '∫[a,b] f(x)dx ≈ h/3 * [f(a) + 4*Σf(x_odd) + 2*Σf(x_even) + f(b)]',
            'requirements': 'n must be even, n ≥ 2',
            'error': 'O(h⁴) or O(1/n⁴)',
            'best_for': 'Smooth functions, quadratic approximations'
        },
        'simpson_3/8': {
            'name': "Simpson's 3/8 Rule",
            'formula': '∫[a,b] f(x)dx ≈ 3h/8 * [f(a) + 3*Σf(x_i) + 3*Σf(x_j) + 2*Σf(x_k) + f(b)]',
            'requirements': 'n must be divisible by 3, n ≥ 3',
            'error': 'O(h⁴) or O(1/n⁴)',
            'best_for': 'Smooth functions, cubic approximations'
        }
    }
    
    if method_name not in info:
        print(f"Unknown method: {method_name}")
        return
    
    method_info = info[method_name]
    
    print("\n" + "="*80)
    print(f"METHOD INFORMATION: {method_info['name']}")
    print("="*80)
    
    data = [
        ["Formula", method_info['formula']],
        ["Requirements", method_info['requirements']],
        ["Error Order", method_info['error']],
        ["Best For", method_info['best_for']]
    ]
    
    if TABULATE_AVAILABLE:
        print(tabulate(data, tablefmt="grid"))
    else:
        for key, value in data:
            print(f"\n{key}:")
            print(f"  {value}")
    
    print()


def display_error_analysis(approximate: float, exact: float):
    """
    Display detailed error analysis.
    
    Parameters:
        approximate: Approximate value
        exact: Exact value
    """
    from utils import calculate_error_metrics
    
    metrics = calculate_error_metrics(approximate, exact)
    
    print("\n" + "="*80)
    print("ERROR ANALYSIS")
    print("="*80)
    
    data = [
        ["Approximate Value", f"{approximate:.15f}"],
        ["Exact Value", f"{exact:.15f}"],
        ["Absolute Error", f"{metrics['absolute_error']:.15e}"],
        ["Relative Error", f"{metrics['relative_error']:.15e}"],
        ["Percentage Error", f"{metrics['percentage_error']:.10f}%"],
        ["Significant Digits", f"{metrics['significant_digits']:.2f}"],
    ]
    
    if TABULATE_AVAILABLE:
        print(tabulate(data, headers=["Metric", "Value"], tablefmt="grid"))
    else:
        for row in data:
            print(f"{row[0]:<25} {row[1]}")
    
    print()


def display_welcome():
    """Display welcome message."""
    print("\n" + "="*80)
    print(" "*25 + "NUMERICAL INTEGRATION")
    print(" "*25 + "Assignment 5 - Part 2")
    print("="*80)
    print("\nThis program implements three numerical integration methods:")
    print("  1. Trapezoidal Rule")
    print("  2. Simpson's 1/3 Rule")
    print("  3. Simpson's 3/8 Rule")
    print("="*80 + "\n")


def display_menu():
    """Display main menu."""
    print("\n" + "-"*80)
    print("SELECT AN OPTION:")
    print("-"*80)
    print("  1. Trapezoidal Rule")
    print("  2. Simpson's 1/3 Rule")
    print("  3. Simpson's 3/8 Rule")
    print("  4. Compare All Methods")
    print("  5. Test Examples")
    print("  6. Method Information")
    print("  0. Exit")
    print("-"*80)
