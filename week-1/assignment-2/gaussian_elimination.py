import numpy as np


def gaussian_elimination(A, b):
    n = len(b)
    # Create augmented matrix
    Ab = np.hstack([A.astype(float), b.reshape(-1, 1).astype(float)])
    
    # Forward elimination with partial pivoting
    for i in range(n):
        # Partial pivoting: find the row with maximum value in column i
        max_row = i + np.argmax(np.abs(Ab[i:, i]))
        if max_row != i:
            Ab[[i, max_row]] = Ab[[max_row, i]]
        
        # Check for zero pivot
        if abs(Ab[i, i]) < 1e-10:
            raise ValueError("Matrix is singular or nearly singular")
        
        # Eliminate column i in rows below
        for j in range(i + 1, n):
            factor = Ab[j, i] / Ab[i, i]
            Ab[j, i:] -= factor * Ab[i, i:]
    
    # Back substitution
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (Ab[i, -1] - np.dot(Ab[i, i+1:n], x[i+1:n])) / Ab[i, i]
    
    return x


def solve(A, b):
    return gaussian_elimination(A, b)
