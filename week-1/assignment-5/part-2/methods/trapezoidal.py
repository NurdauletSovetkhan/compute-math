"""
Trapezoidal Rule Numerical Integration

The trapezoidal rule approximates the integral by dividing the area under the curve 
into trapezoids and summing their areas.

Formula:
∫[a,b] f(x)dx ≈ h/2 * [f(x₀) + 2*Σf(xᵢ) + f(xₙ)]

where:
    h = (b - a) / n  (step size)
    xᵢ = a + i*h     (grid points)
    n = number of intervals
"""

import math


def trapezoidal_rule(func, a: float, b: float, n: int) -> dict:
    """
    Calculate definite integral using the Trapezoidal Rule.
    
    Parameters:
        func: Function to integrate (must be callable)
        a: Lower bound of integration
        b: Upper bound of integration
        n: Number of intervals (subintervals)
    
    Returns:
        Dictionary containing:
            - 'method': 'Trapezoidal Rule'
            - 'result': Approximate integral value
            - 'a': Lower bound
            - 'b': Upper bound
            - 'n': Number of intervals
            - 'h': Step size
            - 'function_evaluations': Number of function evaluations
            - 'points': List of (x, f(x)) values used in computation
    
    Raises:
        ValueError: If n < 1 or a >= b
    """
    # Validation
    if n < 1:
        raise ValueError("Number of intervals must be at least 1")
    if a >= b:
        raise ValueError("Lower bound must be less than upper bound")
    
    # Calculate step size
    h = (b - a) / n
    
    # Initialize sum with boundary terms
    sum_value = 0.0
    points = []
    
    try:
        # Add f(a)
        f_a = func(a)
        points.append((a, f_a))
        sum_value += f_a
        
        # Add 2 * Σf(xᵢ) for i = 1 to n-1
        for i in range(1, n):
            x_i = a + i * h
            f_xi = func(x_i)
            points.append((x_i, f_xi))
            sum_value += 2 * f_xi
        
        # Add f(b)
        f_b = func(b)
        points.append((b, f_b))
        sum_value += f_b
        
        # Calculate final result
        result = (h / 2) * sum_value
        
    except Exception as e:
        raise ValueError(f"Error evaluating function: {str(e)}")
    
    return {
        'method': 'Trapezoidal Rule',
        'result': result,
        'a': a,
        'b': b,
        'n': n,
        'h': h,
        'function_evaluations': n + 1,
        'points': points,
        'formula': f'∫[{a},{b}] f(x)dx ≈ {h}/2 * [f({a}) + 2*Σf(xᵢ) + f({b})]'
    }

