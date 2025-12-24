import numpy as np

def jacobi_method(A, b, x0=None, tol=1e-10, max_iter=1000):
    """
    Solve system of linear equations using Jacobi iteration method.
    
    Parameters:
    A: coefficient matrix (n x n)
    b: constants vector (n x 1)
    x0: initial guess (if None, uses zero vector)
    tol: convergence tolerance
    max_iter: maximum number of iterations
    
    Returns:
    x: solution vector
    iterations: number of iterations performed
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    n = len(b)
    
    if x0 is None:
        x = np.zeros(n)
    else:
        x = np.array(x0, dtype=float)
    
    x_new = np.zeros(n)
    
    for iteration in range(max_iter):
        for i in range(n):
            if abs(A[i, i]) < 1e-10:
                raise ValueError(f"Zero diagonal element at position {i}")
            
            sum_val = 0
            for j in range(n):
                if j != i:
                    sum_val += A[i, j] * x[j]
            
            x_new[i] = (b[i] - sum_val) / A[i, i]
        
        # Check convergence
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new, iteration + 1
        
        x = x_new.copy()
    
    print(f"Warning: Jacobi method did not converge in {max_iter} iterations")
    return x_new, max_iter
