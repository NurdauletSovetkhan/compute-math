"""
Utility functions for curve fitting.
Contains SSE calculation and solving normal equations.
"""

import math


def calculate_sse(y_actual: list, y_predicted: list) -> float:
    """
    Calculate Sum of Squared Errors (SSE).
    SSE = Σ(y_actual - y_predicted)²
    """
    sse = 0.0
    for actual, predicted in zip(y_actual, y_predicted):
        sse += (actual - predicted) ** 2
    return sse


def solve_2x2(a11, a12, b1, a21, a22, b2):
    """
    Solve 2x2 system of linear equations using Cramer's rule.
    | a11  a12 | | x1 |   | b1 |
    | a21  a22 | | x2 | = | b2 |
    """
    det = a11 * a22 - a12 * a21
    if abs(det) < 1e-12:
        raise ValueError("System has no unique solution (determinant is zero)")
    
    x1 = (b1 * a22 - b2 * a12) / det
    x2 = (a11 * b2 - a21 * b1) / det
    return x1, x2


def solve_3x3(matrix, constants):
    """
    Solve 3x3 system using Gaussian elimination.
    matrix: 3x3 coefficient matrix
    constants: 3x1 right-hand side
    """
    # Create augmented matrix
    n = 3
    aug = [matrix[i][:] + [constants[i]] for i in range(n)]
    
    # Forward elimination
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i + 1, n):
            if abs(aug[k][i]) > abs(aug[max_row][i]):
                max_row = k
        aug[i], aug[max_row] = aug[max_row], aug[i]
        
        if abs(aug[i][i]) < 1e-12:
            raise ValueError("System has no unique solution")
        
        # Eliminate column
        for k in range(i + 1, n):
            factor = aug[k][i] / aug[i][i]
            for j in range(i, n + 1):
                aug[k][j] -= factor * aug[i][j]
    
    # Back substitution
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = aug[i][n]
        for j in range(i + 1, n):
            x[i] -= aug[i][j] * x[j]
        x[i] /= aug[i][i]
    
    return x


def solve_4x4(matrix, constants):
    """
    Solve 4x4 system using Gaussian elimination.
    matrix: 4x4 coefficient matrix
    constants: 4x1 right-hand side
    """
    n = 4
    aug = [matrix[i][:] + [constants[i]] for i in range(n)]
    
    # Forward elimination
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i + 1, n):
            if abs(aug[k][i]) > abs(aug[max_row][i]):
                max_row = k
        aug[i], aug[max_row] = aug[max_row], aug[i]
        
        if abs(aug[i][i]) < 1e-12:
            raise ValueError("System has no unique solution")
        
        # Eliminate column
        for k in range(i + 1, n):
            factor = aug[k][i] / aug[i][i]
            for j in range(i, n + 1):
                aug[k][j] -= factor * aug[i][j]
    
    # Back substitution
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = aug[i][n]
        for j in range(i + 1, n):
            x[i] -= aug[i][j] * x[j]
        x[i] /= aug[i][i]
    
    return x
