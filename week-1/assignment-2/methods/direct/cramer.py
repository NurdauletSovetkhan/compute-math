import numpy as np

def cramer_method(A, b):
    """
    Solve system of linear equations using Cramer's method.
    
    Parameters:
    A: coefficient matrix (n x n)
    b: constants vector (n x 1)
    
    Returns:
    x: solution vector
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    n = len(b)
    det_A = np.linalg.det(A)
    
    if abs(det_A) < 1e-10:
        raise ValueError("Matrix is singular, Cramer's method cannot be applied")
    
    x = np.zeros(n)
    
    for i in range(n):
        A_i = A.copy()
        A_i[:, i] = b
        x[i] = np.linalg.det(A_i) / det_A
    
    return x
