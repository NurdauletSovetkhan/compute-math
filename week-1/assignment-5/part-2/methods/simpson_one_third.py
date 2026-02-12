"""
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

