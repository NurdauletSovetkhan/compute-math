"""
Simpson's 1/3 Rule Numerical Integration

Simpson's 1/3 rule uses quadratic polynomials to approximate the curve.
It provides better accuracy than the trapezoidal rule for smooth functions.

Formula:
∫[a,b] f(x)dx ≈ h/3 * [f(x₀) + 4*Σf(x_odd) + 2*Σf(x_even) + f(xₙ)]

where:
    h = (b - a) / n  (step size)
    n must be even
    x_odd: x₁, x₃, x₅, ... (odd indices)
    x_even: x₂, x₄, x₆, ... (even indices)
"""

import math


def simpson_one_third_rule(func, a: float, b: float, n: int) -> dict:
    """
    Calculate definite integral using Simpson's 1/3 Rule.
    
    Parameters:
        func: Function to integrate (must be callable)
        a: Lower bound of integration
        b: Upper bound of integration
        n: Number of intervals (must be even)
    
    Returns:
        Dictionary containing:
            - 'method': 'Simpson\'s 1/3 Rule'
            - 'result': Approximate integral value
            - 'a': Lower bound
            - 'b': Upper bound
            - 'n': Number of intervals
            - 'h': Step size
            - 'function_evaluations': Number of function evaluations
            - 'points': List of (x, f(x)) values used
    
    Raises:
        ValueError: If n is not even, n < 2, or a >= b
    """
    # Validation
    if n < 2:
        raise ValueError("Number of intervals must be at least 2")
    if n % 2 != 0:
        raise ValueError("Number of intervals must be even for Simpson's 1/3 rule")
    if a >= b:
        raise ValueError("Lower bound must be less than upper bound")
    
    # Calculate step size
    h = (b - a) / n
    
    # Initialize sums
    sum_odd = 0.0   # For x₁, x₃, x₅, ...
    sum_even = 0.0  # For x₂, x₄, x₆, ...
    points = []
    
    try:
        # Add f(a)
        f_a = func(a)
        points.append((a, f_a))
        
        # Calculate sum of odd and even indices
        for i in range(1, n):
            x_i = a + i * h
            f_xi = func(x_i)
            points.append((x_i, f_xi))
            
            if i % 2 == 1:  # Odd index
                sum_odd += f_xi
            else:  # Even index
                sum_even += f_xi
        
        # Add f(b)
        f_b = func(b)
        points.append((b, f_b))
        
        # Calculate final result
        # Formula: h/3 * [f(a) + 4*sum_odd + 2*sum_even + f(b)]
        result = (h / 3) * (f_a + 4 * sum_odd + 2 * sum_even + f_b)
        
    except Exception as e:
        raise ValueError(f"Error evaluating function: {str(e)}")
    
    return {
        'method': "Simpson's 1/3 Rule",
        'result': result,
        'a': a,
        'b': b,
        'n': n,
        'h': h,
        'function_evaluations': n + 1,
        'points': points,
        'sum_odd': sum_odd,
        'sum_even': sum_even,
        'formula': f'∫[{a},{b}] f(x)dx ≈ {h}/3 * [f({a}) + 4*Σf(x_odd) + 2*Σf(x_even) + f({b})]'
    }


def simpson_one_third_rule_with_error(func, a: float, b: float, n: int,
                                      fourth_derivative_max: float = None) -> dict:
    """
    Calculate integral with error estimate using Simpson's 1/3 Rule.
    
    Error bound: |E| ≤ (b-a)⁵/(180n⁴) * max|f⁽⁴⁾(x)|
    
    Parameters:
        func: Function to integrate
        a: Lower bound
        b: Upper bound
        n: Number of intervals (must be even)
        fourth_derivative_max: Maximum value of |f⁽⁴⁾(x)| on [a,b]
    
    Returns:
        Dictionary with result and error estimate
    """
    result = simpson_one_third_rule(func, a, b, n)
    
    if fourth_derivative_max is not None:
        error_bound = ((b - a) ** 5) / (180 * n ** 4) * fourth_derivative_max
        result['error_bound'] = error_bound
        result['error_formula'] = f'|E| ≤ ({b}-{a})⁵/(180*{n}⁴) * {fourth_derivative_max}'
    
    return result


def adaptive_simpson(func, a: float, b: float, tolerance: float = 1e-6) -> dict:
    """
    Adaptive Simpson's rule that automatically adjusts n to meet tolerance.
    
    Parameters:
        func: Function to integrate
        a: Lower bound
        b: Upper bound
        tolerance: Desired accuracy
    
    Returns:
        Dictionary with result and number of intervals used
    """
    n = 2
    max_iterations = 20
    
    prev_result = simpson_one_third_rule(func, a, b, n)['result']
    
    for iteration in range(max_iterations):
        n *= 2
        current_result = simpson_one_third_rule(func, a, b, n)['result']
        
        if abs(current_result - prev_result) < tolerance:
            result_dict = simpson_one_third_rule(func, a, b, n)
            result_dict['iterations'] = iteration + 1
            result_dict['tolerance_met'] = True
            return result_dict
        
        prev_result = current_result
    
    result_dict = simpson_one_third_rule(func, a, b, n)
    result_dict['iterations'] = max_iterations
    result_dict['tolerance_met'] = False
    result_dict['warning'] = 'Maximum iterations reached'
    return result_dict


# Example usage and test functions
if __name__ == "__main__":
    # Test with simple functions
    
    # Example 1: ∫[0,1] x² dx = 1/3 ≈ 0.333333
    print("Example 1: ∫[0,1] x² dx")
    result1 = simpson_one_third_rule(lambda x: x**2, 0, 1, 10)
    print(f"Result: {result1['result']:.6f}")
    print(f"Exact: {1/3:.6f}")
    print(f"Error: {abs(result1['result'] - 1/3):.6f}")
    print()
    
    # Example 2: ∫[0,π] sin(x) dx = 2
    print("Example 2: ∫[0,π] sin(x) dx")
    result2 = simpson_one_third_rule(math.sin, 0, math.pi, 100)
    print(f"Result: {result2['result']:.6f}")
    print(f"Exact: 2.000000")
    print(f"Error: {abs(result2['result'] - 2):.6f}")
    print()
    
    # Example 3: ∫[0,1] e^x dx = e - 1 ≈ 1.718282
    print("Example 3: ∫[0,1] e^x dx")
    result3 = simpson_one_third_rule(math.exp, 0, 1, 50)
    exact3 = math.e - 1
    print(f"Result: {result3['result']:.6f}")
    print(f"Exact: {exact3:.6f}")
    print(f"Error: {abs(result3['result'] - exact3):.6f}")
    print()
    
    # Example 4: Adaptive Simpson
    print("Example 4: Adaptive Simpson for ∫[0,1] x² dx")
    result4 = adaptive_simpson(lambda x: x**2, 0, 1, tolerance=1e-8)
    print(f"Result: {result4['result']:.10f}")
    print(f"Intervals used: {result4['n']}")
    print(f"Iterations: {result4['iterations']}")
