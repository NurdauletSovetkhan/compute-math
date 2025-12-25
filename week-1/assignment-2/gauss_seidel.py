import numpy as np


def gauss_seidel(A, b, x0=None, max_iter=100, tol=1e-6):
    """
    Solve system of linear equations Ax = b using Gauss-Seidel iterative method.
    
    Parameters:
    A: coefficient matrix (n x n)
    b: constant vector (n x 1)
    x0: initial guess (if None, starts with zeros)
    max_iter: maximum number of iterations
    tol: convergence tolerance
    
    Returns:
    x: solution vector
    iterations_data: list of dictionaries with iteration data for table display
    converged: boolean indicating if method converged
    """
    n = len(b)
    if x0 is None:
        x = np.zeros(n)
    else:
        x = x0.copy()
    
    iterations_data = []
    
    # Store initial guess
    iterations_data.append({
        'iteration': 0,
        'x': x.copy(),
        'error': None
    })
    
    for k in range(max_iter):
        x_old = x.copy()
        
        for i in range(n):
            # Calculate sum of A[i,j] * x[j] for j != i
            sum1 = np.dot(A[i, :i], x[:i])  # Uses updated values
            sum2 = np.dot(A[i, i+1:], x_old[i+1:])  # Uses old values
            
            # Update x[i]
            if abs(A[i, i]) < 1e-10:
                raise ValueError(f"Zero diagonal element at position {i}")
            
            x[i] = (b[i] - sum1 - sum2) / A[i, i]
        
        # Calculate error (maximum absolute difference)
        error = np.max(np.abs(x - x_old))
        
        # Store iteration data
        iterations_data.append({
            'iteration': k + 1,
            'x': x.copy(),
            'error': error
        })
        
        # Check for convergence
        if error < tol:
            return x, iterations_data, True
    
    # Did not converge within max_iter
    return x, iterations_data, False


def solve(A, b, x0=None, max_iter=100, tol=1e-6):
    """Wrapper function for Gauss-Seidel method"""
    return gauss_seidel(A, b, x0, max_iter, tol)
