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
