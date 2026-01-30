"""
Table display utilities for interpolation results
"""

try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False


def display_input_data(x_values: list, y_values: list):
    """Display input data in a table."""
    print("\n" + "="*60)
    print("INPUT DATA")
    print("="*60)
    
    if TABULATE_AVAILABLE:
        headers = ["i", "x", "y"]
        table_data = []
        for i, (x, y) in enumerate(zip(x_values, y_values), 1):
            table_data.append([i, x, y])
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    else:
        print(f"{'i':<5} {'x':<15} {'y':<15}")
        print("-" * 45)
        for i, (x, y) in enumerate(zip(x_values, y_values), 1):
            print(f"{i:<5} {x:<15.6f} {y:<15.6f}")
    
    print()


def display_interpolation_result(result: dict, show_polynomial: bool = True):
    """
    Display interpolation results.
    
    Parameters:
        result: Dictionary containing interpolation results
        show_polynomial: Whether to display the polynomial representation
    """
    # Import here to avoid circular imports
    try:
        from utils import format_polynomial_pretty, format_polynomial
    except ImportError:
        # Fallback if utils not available
        def format_polynomial_pretty(coeffs, precision=6):
            return str(coeffs)
        def format_polynomial(coeffs, precision=6):
            return str(coeffs)
    
    method = result['method']
    
    print("\n" + "="*80)
    print(f"INTERPOLATION RESULT - {method.upper()}")
    print("="*80)
    
    # Display target and estimated value
    if 'x_target' in result:
        print(f"\nTarget point: x = {result['x_target']}")
        print(f"Estimated value: y = {result['y_estimated']:.10f}")
    
    # Display polynomial if requested
    if show_polynomial and 'polynomial_coefficients' in result:
        coeffs = result['polynomial_coefficients']
        
        print("\n" + "-"*80)
        print("INTERPOLATING POLYNOMIAL Pₙ(x):")
        print("-"*80)
        
        # Pretty format with Unicode
        poly_pretty = format_polynomial_pretty(coeffs, precision=6)
        print(f"\nPₙ(x) = {poly_pretty}")
        
        # Standard format
        poly_standard = format_polynomial(coeffs, precision=6)
        print(f"\nStandard form: {poly_standard}")
        
        print(f"\nDegree: {result.get('degree', len(coeffs) - 1)}")
    
    # Display method-specific information
    if method == 'Newton Forward' and 'h' in result:
        print(f"\nStep size h = {result['h']}")
        if 'u' in result:
            print(f"Parameter u = (x - x₀)/h = {result['u']:.6f}")
    
    elif method == 'Newton Backward' and 'h' in result:
        print(f"\nStep size h = {result['h']}")
        if 'u' in result:
            print(f"Parameter u = (x - xₙ)/h = {result['u']:.6f}")
    
    print("\n" + "="*80 + "\n")


def display_comparison_results(results: list):
    """
    Display comparison of multiple interpolation methods.
    
    Parameters:
        results: List of result dictionaries from different methods
    """
    print("\n" + "="*80)
    print("COMPARISON OF INTERPOLATION METHODS")
    print("="*80)
    
    if not results:
        print("No results to compare.")
        return
    
    # Check if all have the same target
    if all('x_target' in r for r in results):
        x_target = results[0]['x_target']
        print(f"\nTarget point: x = {x_target}")
        print("\n" + "-"*80)
        
        if TABULATE_AVAILABLE:
            headers = ["Method", "Estimated y", "Absolute Difference"]
            table_data = []
            
            # Use first result as reference
            y_ref = results[0]['y_estimated']
            
            for result in results:
                method = result['method']
                y_est = result['y_estimated']
                diff = abs(y_est - y_ref)
                table_data.append([method, f"{y_est:.10f}", f"{diff:.2e}"])
            
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print(f"{'Method':<20} {'Estimated y':<20} {'Abs. Difference':<20}")
            print("-" * 60)
            
            y_ref = results[0]['y_estimated']
            
            for result in results:
                method = result['method']
                y_est = result['y_estimated']
                diff = abs(y_est - y_ref)
                print(f"{method:<20} {y_est:<20.10f} {diff:<20.2e}")
        
        print("\n" + "-"*80)
        
        # Check if results are consistent
        max_diff = max(abs(r['y_estimated'] - results[0]['y_estimated']) for r in results)
        if max_diff < 1e-6:
            print("\n✓ All methods produce consistent results (difference < 10⁻⁶)")
        elif max_diff < 1e-3:
            print(f"\n⚠ Methods show small differences (max difference: {max_diff:.2e})")
        else:
            print(f"\n⚠ Methods show significant differences (max difference: {max_diff:.2e})")
    
    print("\n" + "="*80 + "\n")


def display_method_selection(method_name: str, reason: str):
    """
    Display the selected method and reason for selection.
    
    Parameters:
        method_name: Name of the selected method
        reason: Reason for selection
    """
    print("\n" + "="*80)
    print("METHOD SELECTION")
    print("="*80)
    print(f"\nSelected Method: {method_name}")
    print(f"Reason: {reason}")
    print("\n" + "="*80)


def display_spacing_info(x_values: list, is_equal: bool, h: float = None):
    """Display information about data spacing."""
    print("\n" + "-"*60)
    print("DATA SPACING ANALYSIS")
    print("-"*60)
    
    if is_equal:
        print(f"✓ Data is equally spaced with h = {h}")
        print("  → Newton's difference formulas can be used")
    else:
        print("✗ Data is NOT equally spaced")
        print("  → Only Lagrange interpolation can be used")
    
    print("-"*60 + "\n")


def display_difference_table(differences: list, method: str = "forward"):
    """
    Display forward or backward difference table.
    
    Parameters:
        differences: List of difference lists
        method: 'forward' or 'backward'
    """
    print("\n" + "-"*60)
    print(f"{method.upper()} DIFFERENCE TABLE")
    print("-"*60)
    
    if not differences:
        print("No differences calculated.")
        return
    
    for i, diff_list in enumerate(differences, 1):
        symbol = "Δ" if method == "forward" else "∇"
        print(f"\n{symbol}^{i} values: {[f'{d:.6f}' for d in diff_list]}")
    
    print("-"*60 + "\n")