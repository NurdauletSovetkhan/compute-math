"""
Newton's Forward Difference Interpolation Formula

This method is typically used when x_target is near the beginning of the data.
It requires equally spaced x values.

Formula:
P(x) = y₀ + u*Δy₀ + u(u-1)/2!*Δ²y₀ + u(u-1)(u-2)/3!*Δ³y₀ + ...
P(x) = 
where u = (x - x₀) / h
"""

import math
from utils import validate_data, check_equal_spacing


def calculate_forward_differences(y_values: list) -> list:
    """
    Calculate forward difference table.
    
    Parameters:
        y_values: List of y values
    
    Returns:
        List of difference lists, where differences[i] contains (i+1)-th order differences
    """
    differences = []
    current = y_values[:]
    
    while len(current) > 1:
        next_diff = []
        for i in range(len(current) - 1):
            next_diff.append(current[i + 1] - current[i])
        differences.append(next_diff)
        current = next_diff
    
    return differences


def newton_forward_interpolation(x_values: list, y_values: list, x_target: float) -> dict:
    """
    Perform Newton's forward difference interpolation.
    
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
        raise ValueError("Newton's forward difference requires equally spaced x values")
    
    if h == 0:
        raise ValueError("Step size h cannot be zero")
    
    n = len(x_values)
    x0 = x_values[0]
    
    # Calculate u = (x - x₀) / h
    u = (x_target - x0) / h
    
    # Calculate forward differences
    differences = calculate_forward_differences(y_values)
    
    # Calculate interpolated value using Newton's forward formula
    y_estimated = y_values[0]
    u_term = u
    factorial = 1
    
    for i, diff_list in enumerate(differences):
        factorial *= (i + 1)
        y_estimated += u_term * diff_list[0] / factorial
        u_term *= (u - (i + 1))
    
    # Get polynomial coefficients
    coefficients = get_newton_forward_coefficients(x_values, y_values, differences)
    
    return {
        'method': 'Newton Forward',
        'x_target': x_target,
        'y_estimated': y_estimated,
        'polynomial_coefficients': coefficients,
        'x_values': x_values,
        'y_values': y_values,
        'differences': differences,
        'h': h,
        'u': u,
        'x0': x0,
        'degree': n - 1
    }


def get_newton_forward_coefficients(x_values: list, y_values: list, differences: list) -> list:
    """
    Convert Newton's forward difference formula to standard polynomial form.
    
    Parameters:
        x_values: List of x coordinates
        y_values: List of y coordinates
        differences: Forward difference table
    
    Returns:
        List of polynomial coefficients [c0, c1, c2, ...]
    """
    n = len(x_values)
    h = x_values[1] - x_values[0]
    x0 = x_values[0]
    
    # Initialize result polynomial
    result_coeffs = [0.0] * n
    
    # Start with the constant term y₀
    result_coeffs[0] = y_values[0]
    
    # Build polynomial term by term
    # Current polynomial in terms of u
    u_poly = [1.0]  # Represents 1
    
    factorial = 1
    for i, diff_list in enumerate(differences):
        order = i + 1
        factorial *= order
        
        # Multiply u_poly by (u - (order-1))
        # u - (order-1) = (x - x0)/h - (order-1) = (x - x0 - (order-1)*h)/h
        u_poly = multiply_and_shift(u_poly, order - 1)
        
        # Convert from u to x: u = (x - x0) / h
        # So we need to convert polynomial in u to polynomial in x
        x_poly = convert_u_to_x(u_poly, x0, h)
        
        # Add contribution: (diff_list[0] / factorial) * x_poly
        coeff_factor = diff_list[0] / factorial
        for j in range(len(x_poly)):
            if j < len(result_coeffs):
                result_coeffs[j] += coeff_factor * x_poly[j]
    
    return result_coeffs


def multiply_and_shift(poly: list, shift: int) -> list:
    """
    Multiply polynomial by (u - shift).
    
    Parameters:
        poly: Coefficients of polynomial in u
        shift: Shift value
    
    Returns:
        Coefficients of poly * (u - shift)
    """
    # (u - shift) = u + (-shift)
    result = [0.0] * (len(poly) + 1)
    
    for i in range(len(poly)):
        result[i + 1] += poly[i]  # u term
        result[i] += poly[i] * (-shift)  # constant term
    
    return result


def convert_u_to_x(u_poly: list, x0: float, h: float) -> list:
    """
    Convert polynomial in u to polynomial in x.
    u = (x - x0) / h
    
    Parameters:
        u_poly: Coefficients of polynomial in u
        x0: Starting x value
        h: Step size
    
    Returns:
        Coefficients of polynomial in x
    """
    # u = (x - x0) / h
    # u^n = (x - x0)^n / h^n
    # (x - x0)^n needs to be expanded using binomial theorem
    
    n = len(u_poly)
    result = [0.0] * n
    
    for i, coeff in enumerate(u_poly):
        # u^i = (x - x0)^i / h^i
        # Expand (x - x0)^i
        expanded = expand_binomial_shift(i, -x0)
        
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


def newton_forward_interpolation_full(x_values: list, y_values: list) -> dict:
    """
    Perform Newton's forward difference interpolation and return complete information.
    
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
        raise ValueError("Newton's forward difference requires equally spaced x values")
    
    differences = calculate_forward_differences(y_values)
    coefficients = get_newton_forward_coefficients(x_values, y_values, differences)
    
    return {
        'method': 'Newton Forward',
        'polynomial_coefficients': coefficients,
        'x_values': x_values,
        'y_values': y_values,
        'differences': differences,
        'h': h,
        'degree': len(x_values) - 1
    }
