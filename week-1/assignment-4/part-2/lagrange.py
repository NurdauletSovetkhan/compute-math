"""
Lagrange Interpolation

The Lagrange interpolation formula works for any point distribution (equal or unequal spacing).
It constructs a polynomial that passes through all given points.

Formula:
P(x) = Σ [y_i * L_i(x)]

where L_i(x) = Π [(x - x_j) / (x_i - x_j)] for j ≠ i
"""

from utils import validate_data, evaluate_polynomial


def lagrange_basis(x_values: list, i: int, x: float) -> float:
    """
    Calculate the i-th Lagrange basis polynomial L_i(x).
    
    Parameters:
        x_values: List of x values
        i: Index of the basis polynomial
        x: Point at which to evaluate
    
    Returns:
        Value of L_i(x)
    """
    result = 1.0
    xi = x_values[i]
    
    for j, xj in enumerate(x_values):
        if j != i:
            result *= (x - xj) / (xi - xj)
    
    return result


def lagrange_interpolation(x_values: list, y_values: list, x_target: float) -> dict:
    """
    Perform Lagrange interpolation to find y at x_target.
    
    Parameters:
        x_values: List of x coordinates
        y_values: List of y coordinates
        x_target: Point at which to interpolate
    
    Returns:
        Dictionary containing:
            - 'method': 'Lagrange'
            - 'x_target': Target x value
            - 'y_estimated': Estimated y value
            - 'polynomial_coefficients': Coefficients of the interpolating polynomial
            - 'x_values': Input x values
            - 'y_values': Input y values
    """
    validate_data(x_values, y_values)
    
    n = len(x_values)
    
    # Calculate interpolated value
    y_estimated = 0.0
    for i in range(n):
        L_i = lagrange_basis(x_values, i, x_target)
        y_estimated += y_values[i] * L_i
    
    # Calculate polynomial coefficients
    # We need to expand the Lagrange form into standard polynomial form
    coefficients = get_lagrange_coefficients(x_values, y_values)
    
    return {
        'method': 'Lagrange',
        'x_target': x_target,
        'y_estimated': y_estimated,
        'polynomial_coefficients': coefficients,
        'x_values': x_values,
        'y_values': y_values,
        'degree': n - 1
    }


def get_lagrange_coefficients(x_values: list, y_values: list) -> list:
    """
    Convert Lagrange interpolation to standard polynomial form.
    Returns coefficients [c0, c1, c2, ...] for c0 + c1*x + c2*x^2 + ...
    
    Parameters:
        x_values: List of x coordinates
        y_values: List of y coordinates
    
    Returns:
        List of polynomial coefficients
    """
    n = len(x_values)
    
    # Initialize result polynomial with zeros
    result_coeffs = [0.0] * n
    
    # For each term in the Lagrange sum
    for i in range(n):
        # Calculate the i-th Lagrange basis polynomial coefficients
        basis_coeffs = get_basis_coefficients(x_values, i)
        
        # Multiply by y_i and add to result
        for j in range(len(basis_coeffs)):
            result_coeffs[j] += y_values[i] * basis_coeffs[j]
    
    return result_coeffs


def get_basis_coefficients(x_values: list, i: int) -> list:
    """
    Get coefficients of the i-th Lagrange basis polynomial.
    
    Parameters:
        x_values: List of x coordinates
        i: Index of the basis polynomial
    
    Returns:
        Coefficients of L_i(x)
    """
    n = len(x_values)
    xi = x_values[i]
    
    # Start with polynomial = 1
    poly = [1.0]
    
    # Multiply by (x - x_j) for each j ≠ i
    for j in range(n):
        if j != i:
            xj = x_values[j]
            # Multiply current polynomial by (x - xj)
            poly = multiply_polynomial(poly, [-xj, 1.0])
    
    # Divide by the denominator
    denominator = 1.0
    for j in range(n):
        if j != i:
            denominator *= (xi - x_values[j])
    
    # Divide all coefficients by denominator
    poly = [c / denominator for c in poly]
    
    return poly


def multiply_polynomial(p1: list, p2: list) -> list:
    """
    Multiply two polynomials.
    
    Parameters:
        p1: Coefficients of first polynomial
        p2: Coefficients of second polynomial
    
    Returns:
        Coefficients of product polynomial
    """
    result = [0.0] * (len(p1) + len(p2) - 1)
    
    for i in range(len(p1)):
        for j in range(len(p2)):
            result[i + j] += p1[i] * p2[j]
    
    return result


def lagrange_interpolation_full(x_values: list, y_values: list) -> dict:
    """
    Perform Lagrange interpolation and return complete polynomial information.
    
    Parameters:
        x_values: List of x coordinates
        y_values: List of y coordinates
    
    Returns:
        Dictionary with polynomial information
    """
    validate_data(x_values, y_values)
    
    coefficients = get_lagrange_coefficients(x_values, y_values)
    
    return {
        'method': 'Lagrange',
        'polynomial_coefficients': coefficients,
        'x_values': x_values,
        'y_values': y_values,
        'degree': len(x_values) - 1
    }
