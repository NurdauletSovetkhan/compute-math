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


def trapezoidal_rule_with_error_estimate(func, a: float, b: float, n: int, 
                                         second_derivative_max: float = None) -> dict:
    """
    Calculate integral with error estimate using Trapezoidal Rule.
    
    Error bound: |E| ≤ (b-a)³/(12n²) * max|f''(x)|
    
    Parameters:
        func: Function to integrate
        a: Lower bound
        b: Upper bound
        n: Number of intervals
        second_derivative_max: Maximum value of |f''(x)| on [a,b]
    
    Returns:
        Dictionary with result and error estimate
    """
    result = trapezoidal_rule(func, a, b, n)
    
    if second_derivative_max is not None:
        error_bound = ((b - a) ** 3) / (12 * n ** 2) * second_derivative_max
        result['error_bound'] = error_bound
        result['error_formula'] = f'|E| ≤ ({b}-{a})³/(12*{n}²) * {second_derivative_max}'
    
    return result


# Example usage and test functions
if __name__ == "__main__":
    # Test with simple functions
    
    # Example 1: ∫[0,1] x² dx = 1/3 ≈ 0.333333
    print("Example 1: ∫[0,1] x² dx")
    result1 = trapezoidal_rule(lambda x: x**2, 0, 1, 10)
    print(f"Result: {result1['result']:.6f}")
    print(f"Exact: {1/3:.6f}")
    print(f"Error: {abs(result1['result'] - 1/3):.6f}")
    print()
    
    # Example 2: ∫[0,π] sin(x) dx = 2
    print("Example 2: ∫[0,π] sin(x) dx")
    result2 = trapezoidal_rule(math.sin, 0, math.pi, 100)
    print(f"Result: {result2['result']:.6f}")
    print(f"Exact: 2.000000")
    print(f"Error: {abs(result2['result'] - 2):.6f}")
    print()
    
    # Example 3: ∫[0,1] e^x dx = e - 1 ≈ 1.718282
    print("Example 3: ∫[0,1] e^x dx")
    result3 = trapezoidal_rule(math.exp, 0, 1, 50)
    exact3 = math.e - 1
    print(f"Result: {result3['result']:.6f}")
    print(f"Exact: {exact3:.6f}")
    print(f"Error: {abs(result3['result'] - exact3):.6f}")
