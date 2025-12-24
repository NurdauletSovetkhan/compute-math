import numpy as np

def gauss_jordan(A, b):
    """
    Solve system of linear equations using Gauss-Jordan elimination.
    
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
    
    # Forward elimination with pivoting
    for i in range(n):
        # Partial pivoting
        max_row = i + np.argmax(np.abs(Ab[i:, i]))
        if i != max_row:
            Ab[[i, max_row]] = Ab[[max_row, i]]
        
        # Check for zero pivot
        if abs(Ab[i, i]) < 1e-10:
            raise ValueError("Matrix is singular or nearly singular")
        
        # Normalize pivot row
        Ab[i] = Ab[i] / Ab[i, i]
        
        # Eliminate column (both above and below)
        for j in range(n):
            if i != j:
                factor = Ab[j, i]
                Ab[j] -= factor * Ab[i]
    
    # Extract solution
    x = Ab[:, -1]
    
    return x
