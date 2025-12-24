import numpy as np
from methods.direct.cramer import cramer_method
from methods.direct.gaussian import gaussian_elimination
from methods.direct.gauss_jordan import gauss_jordan
from methods.iterative.jacobi import jacobi_method
from methods.iterative.gauss_seidel import gauss_seidel_method
from methods.iterative.relaxation import relaxation_method
from tabulate import tabulate


def print_system(A, b):
    """Print the system of equations in a readable format."""
    n = len(b)
    print("\nSystem of Linear Equations:")
    print("=" * 50)
    for i in range(n):
        equation = ""
        for j in range(n):
            coef = A[i][j]
            if j == 0:
                equation += f"{coef:+.0f}x{j+1}"
            else:
                equation += f" {coef:+.0f}x{j+1}"
        equation += f" = {b[i]:+.0f}"
        print(equation)
    print("=" * 50)


def format_value(val):
    """
    Format a numeric value for display in the table.
    
    Returns a nicely formatted string that fits well in tables.
    """
    if abs(val) < 1e-8:
        return "0.0000"
    elif abs(val) >= 1e6 or abs(val) < 1e-3:
        return f"{val:.4e}"
    else:
        return f"{val:.6f}"


def is_solution_valid(solution):
    """Check if solution contains valid finite numbers."""
    return solution is not None and np.all(np.isfinite(solution))


def solve_with_method(method_name, method_func, A, b, *args):
    """
    Solve system with a single method and return result.
    
    Returns:
    tuple: (method_name, solution, iterations, error_msg)
    """
    try:
        result = method_func(A, b, *args)
        
        # Handle different return types
        if isinstance(result, tuple):
            solution, iterations = result
            return (method_name, solution, iterations, None)
        else:
            solution = result
            return (method_name, solution, None, None)
            
    except Exception as e:
        return (method_name, None, None, str(e))


def solve_system(A, b):
    """
    Solve the system using all implemented methods and display results in a table.
    
    Parameters:
    A: coefficient matrix (n x n)
    b: constants vector (n x 1)
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    
    print_system(A, b)
    
    # Define all methods to test
    methods = [
        ("Cramer's Method", cramer_method),
        ("Gaussian Elimination", gaussian_elimination),
        ("Gauss-Jordan", gauss_jordan),
        ("Jacobi", jacobi_method),
        ("Gauss-Seidel", gauss_seidel_method),
        ("Relaxation (ω=1.25)", lambda A, b: relaxation_method(A, b, omega=1.25))
    ]
    
    # Solve with all methods
    results = []
    print("\n" + "="*60)
    print("SOLVING WITH ALL METHODS")
    print("="*60)
    
    for method_name, method_func in methods:
        result = solve_with_method(method_name, method_func, A, b)
        name, solution, iterations, error = result
        
        if error:
            print(f"\n{name}: Failed")
            print(f"  Error: {error}")
            results.append([name] + ["Failed"] * n + ["-"])
        elif not is_solution_valid(solution):
            print(f"\n{name}: Invalid (diverged or nan)")
            if iterations:
                print(f"  Iterations: {iterations}")
            results.append([name] + ["Diverged"] * n + [f"{iterations}" if iterations else "-"])
        else:
            iter_str = f"{iterations}" if iterations else "-"
            print(f"\n{name}: Success")
            if iterations:
                print(f"  Iterations: {iterations}")
            print(f"  Solution: {solution}")
            
            results.append([name] + [format_value(val) for val in solution] + [iter_str])
    
    # Create summary table
    print("\n" + "="*80)
    print("SUMMARY TABLE")
    print("="*80)
    
    headers = ["Method"] + [f"x{i+1}" for i in range(n)] + ["Iterations"]
    print(tabulate(results, headers=headers, tablefmt="grid"))
    
    # Verification
    print("\n" + "="*60)
    print("VERIFICATION")
    print("="*60)
    
    successful_solution = None
    successful_method = None
    
    for name, solution, iterations, error in [solve_with_method(name, func, A, b) 
                                               for name, func in methods[:3]]:
        if is_solution_valid(solution):
            successful_solution = solution
            successful_method = name
            break
    
    if successful_solution is not None:
        residual = np.dot(A, successful_solution) - b
        print(f"Using {successful_method} solution:")
        print(f"A·x - b = {residual}")
        print(f"Max residual: {np.max(np.abs(residual)):.2e}")
    else:
        print("No valid solution found for verification.")
        print("Note: This system may be singular or ill-conditioned.")
