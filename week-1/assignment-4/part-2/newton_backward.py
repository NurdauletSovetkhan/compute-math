"""
Newton's Backward Difference Interpolation Formula

This method is typically used when x_target is near the end of the data.
It requires equally spaced x values.

Formula:
P(x) = yₙ + u*∇yₙ + u(u+1)/2!*∇²yₙ + u(u+1)(u+2)/3!*∇³yₙ + ...

where u = (x - xₙ) / h and n is the last index
"""

import math
from utils import validate_data, check_equal_spacing


def calculate_backward_differences(y_values: list) -> list:
    """
    Calculate backward difference table.
    
    Parameters:
        y_values: List of y values
    
    Returns:
        List of difference lists, where differences[i] contains (i+1)-th order differences
    """
    differences = []
    current = y_values[:]
    
    while len(current) > 1:
        next_diff = []
        for i in range(1, len(current)):
            next_diff.append(current[i] - current[i - 1])
        differences.append(next_diff)
        current = next_diff
    
    return differences


def newton_backward_interpolation(x_values: list, y_values: list, x_target: float) -> dict:
    """
    Perform Newton's backward difference interpolation.
    
    Parameters:
        x_values: List of equally spaced x coordinates
        y_values: List of y coordinates
        x_target: Point at which to interpolate
    
    Returns:
        Dictionary containing interpolation results
    """
    validate_data(x_values, y_values)
    
    # Check equal spacing
    is_equal, h = check_equal_spacing(x_values)
    if not is_equal:
        raise ValueError("Newton's backward difference requires equally spaced x values")
    
    if h == 0:
        raise ValueError("Step size h cannot be zero")
    
    n = len(x_values)
    xn = x_values[-1]  # Last x value
    
    # Calculate u = (x - xₙ) / h
    u = (x_target - xn) / h
    
    # Calculate backward differences
    differences = calculate_backward_differences(y_values)
    
    # Calculate interpolated value using Newton's backward formula
    y_estimated = y_values[-1]
    u_term = u
    factorial = 1
    
    for i, diff_list in enumerate(differences):
        factorial *= (i + 1)
        # Use the last value of each difference order
        y_estimated += u_term * diff_list[-1] / factorial
        u_term *= (u + (i + 1))
    
    # Get polynomial coefficients
    coefficients = get_newton_backward_coefficients(x_values, y_values, differences)
    
    return {
        'method': 'Newton Backward',
        'x_target': x_target,
        'y_estimated': y_estimated,
        'polynomial_coefficients': coefficients,
        'x_values': x_values,
        'y_values': y_values,
        'differences': differences,
        'h': h,
        'u': u,
        'xn': xn,
        'degree': n - 1
    }


def get_newton_backward_coefficients(x_values: list, y_values: list, differences: list) -> list:
    """
    Convert Newton's backward difference formula to standard polynomial form.
    
    Parameters:
        x_values: List of x coordinates
        y_values: List of y coordinates
        differences: Backward difference table
    
    Returns:
        List of polynomial coefficients [c0, c1, c2, ...]
    """
    n = len(x_values)
    h = x_values[1] - x_values[0]
    xn = x_values[-1]
    
    # Initialize result polynomial
    result_coeffs = [0.0] * n
    
    # Start with the constant term yₙ
    result_coeffs[0] = y_values[-1]
    
    # Build polynomial term by term
    # Current polynomial in terms of u
    u_poly = [1.0]  # Represents 1
    
    factorial = 1
    for i, diff_list in enumerate(differences):
        order = i + 1
        factorial *= order
        
        # Multiply u_poly by (u + i)
        # u + i = (x - xn)/h + i = (x - xn + i*h)/h
        u_poly = multiply_and_shift_backward(u_poly, order)
        
        # Convert from u to x: u = (x - xn) / h
        x_poly = convert_u_to_x_backward(u_poly, xn, h)
        
        # Add contribution: (diff_list[-1] / factorial) * x_poly
        coeff_factor = diff_list[-1] / factorial
        for j in range(len(x_poly)):
            if j < len(result_coeffs):
                result_coeffs[j] += coeff_factor * x_poly[j]
    
    return result_coeffs


def multiply_and_shift_backward(poly: list, shift: int) -> list:
    """
    Multiply polynomial by (u + shift).
    
    Parameters:
        poly: Coefficients of polynomial in u
        shift: Shift value (positive)
    
    Returns:
        Coefficients of poly * (u + shift)
    """
    # (u + shift) = u + shift
    result = [0.0] * (len(poly) + 1)
    
    for i in range(len(poly)):
        result[i + 1] += poly[i]  # u term
        result[i] += poly[i] * shift  # constant term
    
    return result


def convert_u_to_x_backward(u_poly: list, xn: float, h: float) -> list:
    """
    Convert polynomial in u to polynomial in x for backward differences.
    u = (x - xn) / h
    
    Parameters:
        u_poly: Coefficients of polynomial in u
        xn: Last x value
        h: Step size
    
    Returns:
        Coefficients of polynomial in x
    """
    n = len(u_poly)
    result = [0.0] * n
    
    for i, coeff in enumerate(u_poly):
        # u^i = (x - xn)^i / h^i
        # Expand (x - xn)^i
        expanded = expand_binomial_shift(i, -xn)
        
        # Multiply by coeff / h^i and add to result
        factor = coeff / (h ** i) if h != 0 else 0
        for j in range(len(expanded)):
            if j < len(result):
                result[j] += factor * expanded[j]
    
    return result


def expand_binomial_shift(n: int, shift: float) -> list:
    """
    Expand (x + shift)^n using binomial theorem.
    
    Parameters:
        n: Power
        shift: Shift value
    
    Returns:
        Coefficients [c0, c1, c2, ...] for c0 + c1*x + c2*x^2 + ...
    """
    if n == 0:
        return [1.0]
    
    result = [0.0] * (n + 1)
    
    for k in range(n + 1):
        # Binomial coefficient C(n, k)
        binom_coeff = math.comb(n, k)
        # Term: C(n, k) * shift^(n-k) * x^k
        result[k] = binom_coeff * (shift ** (n - k))
    
    return result


def newton_backward_interpolation_full(x_values: list, y_values: list) -> dict:
    """
    Perform Newton's backward difference interpolation and return complete information.
    
    Parameters:
        x_values: List of equally spaced x coordinates
        y_values: List of y coordinates
    
    Returns:
        Dictionary with polynomial information
    """
    validate_data(x_values, y_values)
    
    # Check equal spacing
    is_equal, h = check_equal_spacing(x_values)
    if not is_equal:
        raise ValueError("Newton's backward difference requires equally spaced x values")
    
    differences = calculate_backward_differences(y_values)
    coefficients = get_newton_backward_coefficients(x_values, y_values, differences)
    
    return {
        'method': 'Newton Backward',
        'polynomial_coefficients': coefficients,
        'x_values': x_values,
        'y_values': y_values,
        'differences': differences,
        'h': h,
        'degree': len(x_values) - 1
    }
