"""
Utility functions for numerical integration
"""

import math
from typing import Callable, Tuple


def validate_integration_params(a: float, b: float, n: int, 
                                 divisibility: int = None) -> None:
    """
    Validate parameters for numerical integration.
    
    Parameters:
        a: Lower bound
        b: Upper bound
        n: Number of intervals
        divisibility: If specified, n must be divisible by this number
    
    Raises:
        ValueError: If parameters are invalid
    """
    if a >= b:
        raise ValueError(f"Lower bound (a={a}) must be less than upper bound (b={b})")
    
    if n < 1:
        raise ValueError(f"Number of intervals must be at least 1 (got n={n})")
    
    if divisibility is not None and n % divisibility != 0:
        raise ValueError(f"Number of intervals (n={n}) must be divisible by {divisibility}")


def validate_function(func: Callable, test_value: float = 0.0) -> None:
    """
    Validate that the function is callable and can be evaluated.
    
    Parameters:
        func: Function to validate
        test_value: Value to test the function with
    
    Raises:
        ValueError: If function is not callable or raises an error
    """
    if not callable(func):
        raise ValueError("Function must be callable")
    
    try:
        result = func(test_value)
        if not isinstance(result, (int, float, complex)):
            raise ValueError(f"Function must return a numeric value, got {type(result)}")
    except Exception as e:
        raise ValueError(f"Error evaluating function at x={test_value}: {str(e)}")


def compare_methods(func: Callable, a: float, b: float, 
                   exact_value: float = None, n: int = None) -> dict:
    """
    Compare different numerical integration methods on the same function.
    
    Parameters:
        func: Function to integrate
        a: Lower bound
        b: Upper bound
        exact_value: Known exact value of the integral (optional)
        n: Number of intervals for comparison (optional, defaults to 100 for trapezoidal)
    
    Returns:
        Dictionary with comparison results
    """
    from methods.trapezoidal import trapezoidal_rule
    from methods.simpson_one_third import simpson_one_third_rule
    from methods.simpson_three_eighth import simpson_three_eighth_rule
    
    results = {}
    
    # Use provided n or set defaults
    if n is None:
        n_trap = 100
        n_simp13 = 100 if 100 % 2 == 0 else 102
        n_simp38 = 99  # Divisible by 3
    else:
        n_trap = n
        n_simp13 = n
        # For simpson_3/8, adjust n to be divisible by 3
        n_simp38 = n + (3 - n % 3) % 3
    
    try:
        results['trapezoidal'] = trapezoidal_rule(func, a, b, n_trap)
    except Exception as e:
        results['trapezoidal'] = {'error': str(e)}
    
    try:
        results['simpson_1/3'] = simpson_one_third_rule(func, a, b, n_simp13)
    except Exception as e:
        results['simpson_1/3'] = {'error': str(e)}
    
    try:
        results['simpson_3/8'] = simpson_three_eighth_rule(func, a, b, n_simp38)
    except Exception as e:
        results['simpson_3/8'] = {'error': str(e)}
    
    # Calculate errors if exact value is provided
    if exact_value is not None:
        for method_name, result in results.items():
            if 'result' in result:
                result['error'] = abs(result['result'] - exact_value)
                result['relative_error'] = abs(result['error'] / exact_value) if exact_value != 0 else float('inf')
    
    results['exact_value'] = exact_value
    
    return results


def get_common_test_functions() -> dict:
    """
    Get a dictionary of common test functions with their exact integrals.
    
    Returns:
        Dictionary mapping function names to tuples of (function, a, b, exact_value)
    """
    return {
        'polynomial_x2': (
            lambda x: x**2,
            0, 1,
            1/3,
            "∫[0,1] x² dx = 1/3"
        ),
        'polynomial_x3': (
            lambda x: x**3,
            0, 2,
            4,
            "∫[0,2] x³ dx = 4"
        ),
        'sin': (
            math.sin,
            0, math.pi,
            2,
            "∫[0,π] sin(x) dx = 2"
        ),
        'cos': (
            math.cos,
            0, math.pi/2,
            1,
            "∫[0,π/2] cos(x) dx = 1"
        ),
        'exp': (
            math.exp,
            0, 1,
            math.e - 1,
            "∫[0,1] e^x dx = e - 1"
        ),
        'sqrt': (
            math.sqrt,
            0, 4,
            16/3,
            "∫[0,4] √x dx = 16/3"
        ),
        '1_over_x': (
            lambda x: 1/x if x != 0 else float('inf'),
            1, 2,
            math.log(2),
            "∫[1,2] 1/x dx = ln(2)"
        ),
        '1_over_1_plus_x2': (
            lambda x: 1 / (1 + x**2),
            0, 1,
            math.pi / 4,
            "∫[0,1] 1/(1+x²) dx = π/4"
        ),
    }


def select_optimal_n(method: str, desired_accuracy: float = 1e-6) -> int:
    """
    Suggest an optimal value of n for a given method and desired accuracy.
    
    Parameters:
        method: 'trapezoidal', 'simpson_1/3', or 'simpson_3/8'
        desired_accuracy: Desired accuracy level
    
    Returns:
        Suggested value of n
    """
    # These are rough estimates
    if method == 'trapezoidal':
        n = int(1 / math.sqrt(desired_accuracy))
    elif method == 'simpson_1/3':
        n = int(1 / (desired_accuracy ** 0.25))
        n = n + (n % 2)  # Make even
    elif method == 'simpson_3/8':
        n = int(1 / (desired_accuracy ** 0.25))
        n = n + (3 - n % 3) % 3  # Make divisible by 3
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return max(n, 10)  # At least 10 intervals


def format_result(result: dict, precision: int = 10) -> str:
    """
    Format integration result as a readable string.
    
    Parameters:
        result: Result dictionary from integration method
        precision: Number of decimal places
    
    Returns:
        Formatted string
    """
    if 'error' in result and isinstance(result['error'], str):
        return f"Error: {result['error']}"
    
    output = []
    output.append(f"Method: {result.get('method', 'Unknown')}")
    output.append(f"Result: {result.get('result', 'N/A'):.{precision}f}")
    output.append(f"Interval: [{result.get('a', 'N/A')}, {result.get('b', 'N/A')}]")
    output.append(f"Number of intervals (n): {result.get('n', 'N/A')}")
    output.append(f"Step size (h): {result.get('h', 'N/A'):.{precision}f}")
    output.append(f"Function evaluations: {result.get('function_evaluations', 'N/A')}")
    
    if 'error_bound' in result:
        output.append(f"Error bound: {result['error_bound']:.{precision}e}")
    
    return '\n'.join(output)


def calculate_error_metrics(approximate: float, exact: float) -> dict:
    """
    Calculate various error metrics.
    
    Parameters:
        approximate: Approximate value
        exact: Exact value
    
    Returns:
        Dictionary with error metrics
    """
    absolute_error = abs(approximate - exact)
    relative_error = absolute_error / abs(exact) if exact != 0 else float('inf')
    percentage_error = relative_error * 100
    
    return {
        'absolute_error': absolute_error,
        'relative_error': relative_error,
        'percentage_error': percentage_error,
        'significant_digits': -math.log10(relative_error) if relative_error > 0 else float('inf')
    }
