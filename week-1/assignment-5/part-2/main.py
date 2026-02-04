"""
Assignment 5 - Part 2: Numerical Integration
Trapezoidal Rule, Simpson's 1/3 Rule, and Simpson's 3/8 Rule

This program provides implementations of three numerical integration methods
and allows users to test them on various functions.
"""

import sys
import math
import sympy as sp
from methods.trapezoidal import trapezoidal_rule
from methods.simpson_one_third import simpson_one_third_rule
from methods.simpson_three_eighth import simpson_three_eighth_rule
from utils import (
    validate_integration_params,
    validate_function,
    compare_methods,
    get_common_test_functions,
    calculate_error_metrics
)
from table import (
    display_welcome,
    display_menu,
    display_integration_result,
    display_comparison,
    display_method_info,
    display_error_analysis
)


def calculate_exact_integral(func_str: str, a: float, b: float):
    """
    Try to calculate exact integral using sympy.
    
    Parameters:
        func_str: String representation of the function
        a: Lower bound
        b: Upper bound
    
    Returns:
        Exact value of the integral or None if unable to compute
    """
    try:
        # Define sympy symbol
        x = sp.Symbol('x')
        
        # Convert string to sympy expression
        # Replace Python operators with sympy equivalents
        expr_str = func_str.replace('^', '**')
        
        # Parse the expression
        expr = sp.sympify(expr_str)
        
        # Calculate definite integral
        result = sp.integrate(expr, (x, a, b))
        
        # Convert to float
        exact_value = float(result.evalf())
        
        print(f"\n✓ Exact integral computed: {exact_value:.10f}")
        return exact_value
        
    except Exception as e:
        print(f"\n⚠ Unable to compute exact integral symbolically: {str(e)}")
        return None


def get_function_from_user():
    """
    Get a function from the user.
    
    Returns:
        Tuple of (function, function_string, exact_value)
    """
    print("\n" + "="*80)
    print("DEFINE YOUR FUNCTION")
    print("="*80)
    print("Enter a mathematical function of x.")
    print("You can use: +, -, *, /, **, sin, cos, tan, exp, log, sqrt, pi, e")
    print("\nExamples:")
    print("  - x**2")
    print("  - sin(x)")
    print("  - exp(x)")
    print("  - 1/(1+x**2)")
    print("  - x**3 + 2*x - 1")
    print("="*80)
    
    while True:
        func_str = input("\nEnter function f(x) = ").strip()
        
        if not func_str:
            print("Function cannot be empty. Please try again.")
            continue
        
        try:
            # Create a safe namespace for eval
            safe_namespace = {
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'exp': math.exp,
                'log': math.log,
                'sqrt': math.sqrt,
                'pi': math.pi,
                'e': math.e,
                'abs': abs,
                'pow': pow,
            }
            
            # Create lambda function
            func = lambda x: eval(func_str, {"__builtins__": {}}, {**safe_namespace, 'x': x})
            
            # Test the function
            test_val = func(1.0)
            print(f"\nTest: f(1) = {test_val}")
            
            return func, func_str, None
            
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Please enter a valid mathematical expression.")


def get_integration_bounds():
    """
    Get integration bounds from user.
    
    Returns:
        Tuple of (a, b)
    """
    print("\n" + "-"*80)
    print("INTEGRATION BOUNDS")
    print("-"*80)
    
    while True:
        try:
            a = float(input("Enter lower bound (a): "))
            b = float(input("Enter upper bound (b): "))
            
            if a >= b:
                print("Error: Lower bound must be less than upper bound.")
                continue
            
            return a, b
            
        except ValueError:
            print("Error: Please enter valid numbers.")


def get_number_of_intervals(method: str):
    """
    Get number of intervals from user based on method requirements.
    
    Parameters:
        method: 'trapezoidal', 'simpson_1/3', or 'simpson_3/8'
    
    Returns:
        int: Number of intervals
    """
    print("\n" + "-"*80)
    print("NUMBER OF INTERVALS")
    print("-"*80)
    
    if method == 'trapezoidal':
        print("Requirements: n ≥ 1")
        divisibility = None
        min_n = 1
    elif method == 'simpson_1/3':
        print("Requirements: n must be even and n ≥ 2")
        divisibility = 2
        min_n = 2
    elif method == 'simpson_3/8':
        print("Requirements: n must be divisible by 3 and n ≥ 3")
        divisibility = 3
        min_n = 3
    else:
        divisibility = None
        min_n = 1
    
    while True:
        try:
            n = int(input(f"Enter number of intervals (n ≥ {min_n}): "))
            
            if n < min_n:
                print(f"Error: n must be at least {min_n}")
                continue
            
            if divisibility and n % divisibility != 0:
                print(f"Error: n must be divisible by {divisibility}")
                continue
            
            return n
            
        except ValueError:
            print("Error: Please enter a valid integer.")


def run_single_method(method_name: str):
    """
    Run a single integration method.
    
    Parameters:
        method_name: 'trapezoidal', 'simpson_1/3', or 'simpson_3/8'
    """
    # Get function
    func, func_str, exact_value = get_function_from_user()
    
    # Get bounds
    a, b = get_integration_bounds()
    
    # Get number of intervals
    n = get_number_of_intervals(method_name)
    
    # Try to compute exact value automatically
    print("\n" + "-"*80)
    print("EXACT VALUE CALCULATION")
    print("-"*80)
    print("Attempting to compute exact integral symbolically...")
    
    exact_value = calculate_exact_integral(func_str, a, b)
    
    # If automatic computation failed, ask user
    if exact_value is None:
        exact_str = input("\nDo you know the exact value of the integral? (y/n): ").strip().lower()
        if exact_str == 'y':
            try:
                exact_value = float(input("Enter exact value: "))
            except ValueError:
                print("Invalid value, proceeding without exact value.")
                exact_value = None
    
    # Perform integration
    try:
        if method_name == 'trapezoidal':
            result = trapezoidal_rule(func, a, b, n)
        elif method_name == 'simpson_1/3':
            result = simpson_one_third_rule(func, a, b, n)
        elif method_name == 'simpson_3/8':
            result = simpson_three_eighth_rule(func, a, b, n)
        else:
            print(f"Unknown method: {method_name}")
            return
        
        # Add exact value if provided
        if exact_value is not None:
            metrics = calculate_error_metrics(result['result'], exact_value)
            result['error'] = metrics['absolute_error']
            result['relative_error'] = metrics['relative_error']
        
        # Display result
        display_integration_result(result)
        
        if exact_value is not None:
            display_error_analysis(result['result'], exact_value)
        
        # Ask if user wants to see computation points
        show_points = input("\nShow computation points? (y/n): ").strip().lower()
        if show_points == 'y':
            from table import display_computation_points
            display_computation_points(result['points'])
        
    except Exception as e:
        print(f"\nError during integration: {str(e)}")


def run_comparison():
    """Run comparison of all three methods."""
    # Get function
    func, func_str, exact_value = get_function_from_user()
    
    # Get bounds
    a, b = get_integration_bounds()
    
    # Try to compute exact value automatically
    print("\n" + "-"*80)
    print("EXACT VALUE CALCULATION")
    print("-"*80)
    print("Attempting to compute exact integral symbolically...")
    
    exact_value = calculate_exact_integral(func_str, a, b)
    
    # If automatic computation failed, ask user
    if exact_value is None:
        exact_str = input("\nDo you know the exact value of the integral? (y/n): ").strip().lower()
        if exact_str == 'y':
            try:
                exact_value = float(input("Enter exact value: "))
            except ValueError:
                print("Invalid value, proceeding without exact value.")
                exact_value = None
    
    # Perform comparison
    try:
        results = compare_methods(func, a, b, exact_value)
        
        # Display detailed results for each method
        print("\n" + "="*80)
        print("DETAILED RESULTS FOR EACH METHOD")
        print("="*80)
        
        method_order = [('trapezoidal', 'TRAPEZOIDAL RULE', 'n ≥ 1'),
                        ('simpson_1/3', "SIMPSON'S 1/3 RULE", 'n must be even'),
                        ('simpson_3/8', "SIMPSON'S 3/8 RULE", 'n must be divisible by 3')]
        
        for i, (method_key, method_name, constraint) in enumerate(method_order, 1):
            if method_key in results:
                result = results[method_key]
                if 'error' in result and isinstance(result['error'], str):
                    print(f"\n{i}. {method_name} - ERROR")
                    print(f"   {result['error']}")
                else:
                    n = result.get('n', 'N/A')
                    h = result.get('h', 0)
                    value = result.get('result', 0)
                    
                    print(f"\n{i}. {method_name} (n={n}, {constraint}):")
                    print(f"   h = {h:.10f}")
                    print(f"   Result = {value:.10f}")
                    
                    if exact_value is not None and 'error' in result:
                        abs_error = result.get('error', 0)
                        rel_error = result.get('relative_error', 0)
                        print(f"   Absolute Error = {abs_error:.10e}")
                        print(f"   Relative Error = {rel_error:.10e}")
        
        # Display comparison table
        display_comparison(results)
        
    except Exception as e:
        print(f"\nError during comparison: {str(e)}")


def run_test_examples():
    """Run predefined test examples."""
    test_functions = get_common_test_functions()
    
    print("\n" + "="*80)
    print("TEST EXAMPLES")
    print("="*80)
    
    for i, (name, (func, a, b, exact, desc)) in enumerate(test_functions.items(), 1):
        print(f"  {i}. {desc}")
    
    print("  0. Back to main menu")
    print("="*80)
    
    try:
        choice = int(input("\nSelect example: "))
        
        if choice == 0:
            return
        
        if choice < 1 or choice > len(test_functions):
            print("Invalid choice.")
            return
        
        # Get selected function
        func_name = list(test_functions.keys())[choice - 1]
        func, a, b, exact, desc = test_functions[func_name]
        
        print(f"\nTesting: {desc}")
        print(f"Exact value: {exact:.10f}")
        
        # Run comparison
        results = compare_methods(func, a, b, exact)
        display_comparison(results)
        
    except ValueError:
        print("Invalid input.")
    except Exception as e:
        print(f"Error: {str(e)}")


def show_method_information():
    """Display information about integration methods."""
    print("\n" + "="*80)
    print("METHOD INFORMATION")
    print("="*80)
    print("  1. Trapezoidal Rule")
    print("  2. Simpson's 1/3 Rule")
    print("  3. Simpson's 3/8 Rule")
    print("  4. All Methods")
    print("  0. Back")
    print("="*80)
    
    try:
        choice = int(input("\nSelect option: "))
        
        if choice == 0:
            return
        elif choice == 1:
            display_method_info('trapezoidal')
        elif choice == 2:
            display_method_info('simpson_1/3')
        elif choice == 3:
            display_method_info('simpson_3/8')
        elif choice == 4:
            display_method_info('trapezoidal')
            display_method_info('simpson_1/3')
            display_method_info('simpson_3/8')
        else:
            print("Invalid choice.")
            
    except ValueError:
        print("Invalid input.")


def main():
    """Main program loop."""
    display_welcome()
    
    while True:
        display_menu()
        
        try:
            choice = input("\nYour choice: ").strip()
            
            if choice == '0':
                print("\nThank you for using the Numerical Integration Calculator!")
                sys.exit(0)
            
            elif choice == '1':
                run_single_method('trapezoidal')
            
            elif choice == '2':
                run_single_method('simpson_1/3')
            
            elif choice == '3':
                run_single_method('simpson_3/8')
            
            elif choice == '4':
                run_comparison()
            
            elif choice == '5':
                run_test_examples()
            
            elif choice == '6':
                show_method_information()
            
            else:
                print("\nInvalid choice. Please select a valid option.")
        
        except KeyboardInterrupt:
            print("\n\nProgram interrupted by user.")
            sys.exit(0)
        
        except Exception as e:
            print(f"\nUnexpected error: {str(e)}")
            print("Returning to main menu...")


if __name__ == "__main__":
    main()
