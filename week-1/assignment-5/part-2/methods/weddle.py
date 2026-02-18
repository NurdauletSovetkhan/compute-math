"""
Weddle's Rule Numerical Integration

Weddle's rule uses 7 equally-spaced points (6 intervals) to approximate the integral.
It provides higher accuracy than Simpson's rules.

Formula:
∫[a,b] f(x)dx ≈ (3h/10) * [f₀ + 5f₁ + f₂ + 6f₃ + f₄ + 5f₅ + f₆]

where:
    h = (b - a) / 6  (step size)
    fᵢ = f(a + i*h)  (function values at grid points)
    n = 6 intervals (7 points)

Note: Weddle's rule requires exactly 6 intervals (7 points).
"""

import math


def weddle_rule(func, a: float, b: float, n: int) -> dict:
    """
    Calculate definite integral using Weddle's Rule.
    
    Parameters:
        func: Function to integrate (must be callable)
        a: Lower bound of integration
        b: Upper bound of integration
        n: Number of intervals (must be a multiple of 6)
    
    Returns:
        Dictionary containing:
            - 'method': 'Weddle's Rule'
            - 'result': Approximate integral value
            - 'a': Lower bound
            - 'b': Upper bound
            - 'n': Number of intervals
            - 'h': Step size
            - 'function_evaluations': Number of function evaluations
            - 'points': List of (x, f(x)) values used in computation
    
    Raises:
        ValueError: If n is not a multiple of 6, n < 6, or a >= b
    """
    # Validation
    if n < 6:
        raise ValueError("Number of intervals must be at least 6 for Weddle's rule")
    if n % 6 != 0:
        raise ValueError("Number of intervals must be a multiple of 6 for Weddle's rule")
    if a >= b:
        raise ValueError("Lower bound must be less than upper bound")
    
    # Calculate step size
    h = (b - a) / n
    
    # Weddle's coefficients: [1, 5, 1, 6, 1, 5, 1]
    weddle_coeffs = [1, 5, 1, 6, 1, 5, 1]
    
    result = 0.0
    points = []
    num_segments = n // 6  # Number of 6-interval segments
    
    try:
        for seg in range(num_segments):
            # Starting point for this segment
            x_start = a + seg * 6 * h
            
            # Apply Weddle's rule for this 6-interval segment
            segment_sum = 0.0
            
            for i in range(7):
                x_i = x_start + i * h
                f_xi = func(x_i)
                
                # Store points (avoid duplicates at segment boundaries)
                if seg == 0 or i > 0:
                    points.append((x_i, f_xi))
                
                segment_sum += weddle_coeffs[i] * f_xi
            
            result += (3 * h / 10) * segment_sum
        
    except Exception as e:
        raise ValueError(f"Error evaluating function: {str(e)}")
    
    return {
        'method': "Weddle's Rule",
        'result': result,
        'a': a,
        'b': b,
        'n': n,
        'h': h,
        'function_evaluations': len(points),
        'points': points,
        'formula': f'∫[{a},{b}] f(x)dx ≈ (3h/10) * [f₀ + 5f₁ + f₂ + 6f₃ + f₄ + 5f₅ + f₆]'
    }
