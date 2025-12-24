import numpy as np

def gaussian_elimination(A, b):
    """
    Solve system of linear equations using Gaussian elimination.
    
    Parameters:
    A: coefficient matrix (n x n)
    b: constants vector (n x 1)
    
    Returns:
    x: solution vector
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float).reshape(-1, 1)
    
    n = len(b)
    
    # Create augmented matrix
    Ab = np.hstack([A, b])
    
    # Forward elimination
    for i in range(n):
        # Partial pivoting
        max_row = i + np.argmax(np.abs(Ab[i:, i]))
        if i != max_row:
            Ab[[i, max_row]] = Ab[[max_row, i]]
        
        # Check for zero pivot
        if abs(Ab[i, i]) < 1e-10:
            raise ValueError("Matrix is singular or nearly singular")
        
        # Eliminate column
        for j in range(i + 1, n):
            factor = Ab[j, i] / Ab[i, i]
            Ab[j, i:] -= factor * Ab[i, i:]
    
    # Back substitution
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (Ab[i, -1] - np.dot(Ab[i, i+1:n], x[i+1:n])) / Ab[i, i]
    
    return x
