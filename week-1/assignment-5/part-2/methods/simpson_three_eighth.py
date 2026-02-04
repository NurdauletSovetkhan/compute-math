"""
Simpson's 3/8 Rule Numerical Integration

Simpson's 3/8 rule uses cubic polynomials to approximate the curve.
It's useful when the number of intervals is divisible by 3.

Formula:
∫[a,b] f(x)dx ≈ 3h/8 * [f(x₀) + 3*Σf(x_i) + 3*Σf(x_j) + 2*Σf(x_k) + f(xₙ)]

where:
    h = (b - a) / n  (step size)
    n must be divisible by 3
    i: indices where i mod 3 = 1  (x₁, x₄, x₇, ...)
    j: indices where j mod 3 = 2  (x₂, x₅, x₈, ...)
    k: indices where k mod 3 = 0 and k ≠ 0, n  (x₃, x₆, x₉, ...)
"""

import math


def simpson_three_eighth_rule(func, a: float, b: float, n: int) -> dict:
    """
    Calculate definite integral using Simpson's 3/8 Rule.
    
    Parameters:
        func: Function to integrate (must be callable)
        a: Lower bound of integration
        b: Upper bound of integration
        n: Number of intervals (must be divisible by 3)
    
    Returns:
        Dictionary containing:
            - 'method': 'Simpson\'s 3/8 Rule'
            - 'result': Approximate integral value
            - 'a': Lower bound
            - 'b': Upper bound
            - 'n': Number of intervals
            - 'h': Step size
            - 'function_evaluations': Number of function evaluations
            - 'points': List of (x, f(x)) values used
    
    Raises:
        ValueError: If n is not divisible by 3, n < 3, or a >= b
    """
    # Validation
    if n < 3:
        raise ValueError("Number of intervals must be at least 3")
    if n % 3 != 0:
        raise ValueError("Number of intervals must be divisible by 3 for Simpson's 3/8 rule")
    if a >= b:
        raise ValueError("Lower bound must be less than upper bound")
    
    # Calculate step size
    h = (b - a) / n
    
    # Initialize sums
    sum1 = 0.0  # For indices where i % 3 == 1
    sum2 = 0.0  # For indices where i % 3 == 2
    sum3 = 0.0  # For indices where i % 3 == 0 (except 0 and n)
    points = []
    
    try:
        # Add f(a)
        f_a = func(a)
        points.append((a, f_a))
        
        # Calculate sums for different groups
        for i in range(1, n):
            x_i = a + i * h
            f_xi = func(x_i)
            points.append((x_i, f_xi))
            
            if i % 3 == 1:
                sum1 += f_xi
            elif i % 3 == 2:
                sum2 += f_xi
            else:  # i % 3 == 0
                sum3 += f_xi
        
        # Add f(b)
        f_b = func(b)
        points.append((b, f_b))
        
        # Calculate final result
        # Formula: 3h/8 * [f(a) + 3*sum1 + 3*sum2 + 2*sum3 + f(b)]
        result = (3 * h / 8) * (f_a + 3 * sum1 + 3 * sum2 + 2 * sum3 + f_b)
        
    except Exception as e:
        raise ValueError(f"Error evaluating function: {str(e)}")
    
    return {
        'method': "Simpson's 3/8 Rule",
        'result': result,
        'a': a,
        'b': b,
        'n': n,
        'h': h,
        'function_evaluations': n + 1,
        'points': points,
        'sum1': sum1,
        'sum2': sum2,
        'sum3': sum3,
        'formula': f'∫[{a},{b}] f(x)dx ≈ 3*{h}/8 * [f({a}) + 3*Σf(x_i) + 3*Σf(x_j) + 2*Σf(x_k) + f({b})]'
    }


def simpson_three_eighth_rule_with_error(func, a: float, b: float, n: int,
                                         fourth_derivative_max: float = None) -> dict:
    """
    Calculate integral with error estimate using Simpson's 3/8 Rule.
    
    Error bound: |E| ≤ (b-a)⁵/(80n⁴) * max|f⁽⁴⁾(x)|
    
    Parameters:
        func: Function to integrate
        a: Lower bound
        b: Upper bound
        n: Number of intervals (must be divisible by 3)
        fourth_derivative_max: Maximum value of |f⁽⁴⁾(x)| on [a,b]
    
    Returns:
        Dictionary with result and error estimate
    """
    result = simpson_three_eighth_rule(func, a, b, n)
    
    if fourth_derivative_max is not None:
        # Error bound for Simpson's 3/8 rule
        error_bound = ((b - a) ** 5) / (80 * n ** 4) * fourth_derivative_max
        result['error_bound'] = error_bound
        result['error_formula'] = f'|E| ≤ ({b}-{a})⁵/(80*{n}⁴) * {fourth_derivative_max}'
    
    return result


def adaptive_simpson_three_eighth(func, a: float, b: float, tolerance: float = 1e-6) -> dict:
    """
    Adaptive Simpson's 3/8 rule that automatically adjusts n to meet tolerance.
    
    Parameters:
        func: Function to integrate
        a: Lower bound
        b: Upper bound
        tolerance: Desired accuracy
    
    Returns:
        Dictionary with result and number of intervals used
    """
    n = 3
    max_iterations = 20
    
    prev_result = simpson_three_eighth_rule(func, a, b, n)['result']
    
    for iteration in range(max_iterations):
        n += 3  # Increment by 3 to maintain divisibility
        current_result = simpson_three_eighth_rule(func, a, b, n)['result']
        
        if abs(current_result - prev_result) < tolerance:
            result_dict = simpson_three_eighth_rule(func, a, b, n)
            result_dict['iterations'] = iteration + 1
            result_dict['tolerance_met'] = True
            return result_dict
        
        prev_result = current_result
    
    result_dict = simpson_three_eighth_rule(func, a, b, n)
    result_dict['iterations'] = max_iterations
    result_dict['tolerance_met'] = False
    result_dict['warning'] = 'Maximum iterations reached'
    return result_dict


# Example usage and test functions
if __name__ == "__main__":
    # Test with simple functions
    
    # Example 1: ∫[0,1] x² dx = 1/3 ≈ 0.333333
    print("Example 1: ∫[0,1] x² dx")
    result1 = simpson_three_eighth_rule(lambda x: x**2, 0, 1, 9)
    print(f"Result: {result1['result']:.6f}")
    print(f"Exact: {1/3:.6f}")
    print(f"Error: {abs(result1['result'] - 1/3):.6f}")
    print()
    
    # Example 2: ∫[0,π] sin(x) dx = 2
    print("Example 2: ∫[0,π] sin(x) dx")
    result2 = simpson_three_eighth_rule(math.sin, 0, math.pi, 99)
    print(f"Result: {result2['result']:.6f}")
    print(f"Exact: 2.000000")
    print(f"Error: {abs(result2['result'] - 2):.6f}")
    print()
    
    # Example 3: ∫[0,1] e^x dx = e - 1 ≈ 1.718282
    print("Example 3: ∫[0,1] e^x dx")
    result3 = simpson_three_eighth_rule(math.exp, 0, 1, 48)
    exact3 = math.e - 1
    print(f"Result: {result3['result']:.6f}")
    print(f"Exact: {exact3:.6f}")
    print(f"Error: {abs(result3['result'] - exact3):.6f}")
    print()
    
    # Example 4: ∫[0,2] x³ dx = 4
    print("Example 4: ∫[0,2] x³ dx")
    result4 = simpson_three_eighth_rule(lambda x: x**3, 0, 2, 12)
    print(f"Result: {result4['result']:.6f}")
    print(f"Exact: 4.000000")
    print(f"Error: {abs(result4['result'] - 4):.6f}")
    print()
    
    # Example 5: Adaptive Simpson's 3/8
    print("Example 5: Adaptive Simpson's 3/8 for ∫[0,1] x² dx")
    result5 = adaptive_simpson_three_eighth(lambda x: x**2, 0, 1, tolerance=1e-8)
    print(f"Result: {result5['result']:.10f}")
    print(f"Intervals used: {result5['n']}")
    print(f"Iterations: {result5['iterations']}")
