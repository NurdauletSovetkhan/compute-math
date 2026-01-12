import numpy as np
from tabulate import tabulate
from test_systems import get_systems
from determinant import get_determinant
from inverse_matrix import get_inverse_matrix, print_inverse_matrix

# Direct methods
from methods.direct.gaussian_elimination import solve as gaussian_solve
from methods.direct.cramer import solve as cramer_solve
from methods.direct.gauss_jordan import solve as gauss_jordan_solve

# Iterative methods
from methods.iterative.gauss_seidel import solve as gauss_seidel_solve
from methods.iterative.jacobi import solve as jacobi_solve
from methods.iterative.sor import solve as sor_solve

# Dictionary of available methods
DIRECT_METHODS = {
    '1': ('Cramer', cramer_solve),
    '2': ('Gaussian Elimination', gaussian_solve),
    '3': ('Gauss-Jordan', gauss_jordan_solve),
}

ITERATIVE_METHODS = {
    '1': ('Jacobi', jacobi_solve),
    '2': ('Gauss-Seidel', gauss_seidel_solve),
    '3': ('SOR', sor_solve),
}

def print_system(A, b, description):
    print(f"\n{description}")
    print("Coefficient Matrix A:")
    print(A)
    print("Constant Vector b:")
    print(b)


def print_direct_solution(x_true, method_name="Direct Method"):
    print(f"\n{method_name.upper()} - SOLUTION")
    for i, val in enumerate(x_true):
        print(f"x{i+1} = {val:.6f}")


def print_iteration_table(iterations_data, x_true, method_name="Iterative Method"):
    """Print table showing iterations of iterative method"""
    print(f"\n{method_name.upper()} - ITERATIONS")
    
    n = len(iterations_data[0]['x'])
    
    # Create headers
    headers = ["Iter"]
    for i in range(n):
        headers.append(f"x{i+1}")
    headers.extend(["Max Error", "Error vs True"])
    
    # Create table data
    table_data = []
    for data in iterations_data:
        iter_num = data['iteration']
        x = data['x']
        error = data['error']
        
        # Calculate error compared to true solution
        true_error = np.max(np.abs(x - x_true))
        
        # Build row
        row = [iter_num]
        for val in x:
            row.append(f"{val:.2f}")
        
        if error is not None:
            row.append(f"{error:.4f}")
        else:
            row.append("N/A")
        
        row.append(f"{true_error:.4f}")
        table_data.append(row)
    
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def print_determinant(matrix):
    """Calculate and print the determinant of the matrix"""
    det = get_determinant(matrix.tolist())
    print(f"\nDeterminant of the coefficient matrix: {det:.4f}")
    
    # Also print inverse matrix
    try:
        inverse = get_inverse_matrix(matrix)
        print("\nInverse Matrix A^-1:")
        print(inverse)
    except ValueError as e:
        print(f"\nInverse matrix cannot be calculated: {e}")


def compare_solutions(x_direct, x_iterative, converged):
    """Print comparison between direct and iterative solutions"""
    print("\nCOMPARISON OF SOLUTIONS")
    
    # Create table data
    table_data = []
    max_error = 0
    for i in range(len(x_direct)):
        error = abs(x_direct[i] - x_iterative[i])
        max_error = max(max_error, error)
        table_data.append([
            f"x{i+1}",
            f"{x_direct[i]:.4f}",
            f"{x_iterative[i]:.4f}",
            f"{error:.4f}"
        ])
    
    headers = ["Variable", "Direct", "Iterative", "Absolute Error"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print(f"Maximum Absolute Error: {max_error:.4f}")
    print(f"Convergence Status: {'CONVERGED' if converged else 'NOT CONVERGED'}")


def solve_system(A, b, description, direct_method=None, iterative_method=None, max_iter=50, tol=1e-6, omega=1.25):
    """Solve a system using selected direct and/or iterative methods"""
    print_system(A, b, description)
    print_determinant(A)
    
    x_direct = None
    
    # Solve with direct method if selected
    if direct_method:
        method_name, method_func = direct_method
        try:
            x_direct = method_func(A.copy(), b.copy())
            print_direct_solution(x_direct, method_name)
        except Exception as e:
            print(f"Error in {method_name}: {e}")
    
    # Solve with iterative method if selected
    if iterative_method:
        method_name, method_func = iterative_method
        try:
            # SOR requires omega parameter
            if 'SOR' in method_name:
                x_iterative, iterations_data, converged = method_func(
                    A.copy(), b.copy(), omega=omega, max_iter=max_iter, tol=tol
                )
            else:
                x_iterative, iterations_data, converged = method_func(
                    A.copy(), b.copy(), max_iter=max_iter, tol=tol
                )
            
            # Use direct solution for comparison, or compute one
            if x_direct is None:
                x_direct = gaussian_solve(A.copy(), b.copy())
            
            print_iteration_table(iterations_data, x_direct, method_name)
            compare_solutions(x_direct, x_iterative, converged)
        except Exception as e:
            print(f"Error in {method_name}: {e}")
    
    print("=" * 80)


def get_user_system():
    try:
        n = int(input("\nEnter the size of the system (n x n): "))
        if n <= 0:
            print("Invalid size!")
            return None, None
        
        print(f"\nEnter coefficient matrix A ({n}x{n}):")
        A = []
        for i in range(n):
            row_input = input(f"Row {i+1} (space-separated values): ")
            row = list(map(float, row_input.split()))
            if len(row) != n:
                print(f"Error: Expected {n} values, got {len(row)}")
                return None, None
            A.append(row)
        
        print(f"\nEnter constant vector b ({n} values):")
        b_input = input("Space-separated values: ")
        b = list(map(float, b_input.split()))
        if len(b) != n:
            print(f"Error: Expected {n} values, got {len(b)}")
            return None, None
        
        return np.array(A, dtype=float), np.array(b, dtype=float)
    
    except ValueError:
        print("Invalid input! Please enter numeric values.")
        return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None


def select_direct_method():
    """Let user select a direct method"""
    print("\nDIRECT METHODS:")
    print("1. Cramer's Rule")
    print("2. Gaussian Elimination")
    print("3. Gauss-Jordan")
    print("0. Skip direct method")
    
    choice = input("Select direct method (0-3): ").strip()
    if choice == '0':
        return None
    return DIRECT_METHODS.get(choice)


def select_iterative_method():
    """Let user select an iterative method"""
    print("\nITERATIVE METHODS:")
    print("1. Jacobi (converges)")
    print("2. Gauss-Seidel (converges faster)")
    print("3. SOR (fastest with optimal omega)")
    print("0. Skip iterative method")
    
    choice = input("Select iterative method (0-3): ").strip()
    if choice == '0':
        return None
    return ITERATIVE_METHODS.get(choice)


def get_iterative_params():
    """Get parameters for iterative methods"""
    print("\nIterative method parameters:")
    try:
        max_iter = input("Max iterations (default 100): ").strip()
        max_iter = int(max_iter) if max_iter else 100
        
        tol = input("Tolerance (default 1e-6): ").strip()
        tol = float(tol) if tol else 1e-6
        
        omega = input("Omega for SOR (default 1.25, range 0-2): ").strip()
        omega = float(omega) if omega else 1.25
        
        return max_iter, tol, omega
    except ValueError:
        print("Invalid input, using defaults.")
        return 100, 1e-6, 1.25


def main():
    print("=" * 60)
    print("      SYSTEM OF LINEAR EQUATIONS SOLVER")
    print("=" * 60)
    print("\nAvailable Methods:")
    print("  DIRECT: Cramer | Gaussian | Gauss-Jordan")
    print("  ITERATIVE: Jacobi | Gauss-Seidel | SOR")
    
    while True:
        print("\n" + "-" * 40)
        print("MAIN MENU:")
        print("-" * 40)
        print("1. Solve example systems")
        print("2. Enter custom system")
        print("3. Compare all methods on example")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            # Select methods
            direct = select_direct_method()
            iterative = select_iterative_method()
            
            if not direct and not iterative:
                print("Please select at least one method!")
                continue
            
            max_iter, tol, omega = 100, 1e-6, 1.25
            if iterative:
                max_iter, tol, omega = get_iterative_params()
            
            # Run predefined examples
            systems = get_systems()
            for A, b, description in systems:
                solve_system(A, b, description, direct, iterative, max_iter, tol, omega)
            print("\nALL SYSTEMS SOLVED")
        
        elif choice == '2':
            # Get custom system from user
            A, b = get_user_system()
            if A is not None and b is not None:
                direct = select_direct_method()
                iterative = select_iterative_method()
                
                if not direct and not iterative:
                    print("Please select at least one method!")
                    continue
                
                max_iter, tol, omega = 100, 1e-6, 1.25
                if iterative:
                    max_iter, tol, omega = get_iterative_params()
                
                solve_system(A, b, "Custom System", direct, iterative, max_iter, tol, omega)
        
        elif choice == '3':
            # Compare all methods
            print("\nCOMPARING ALL METHODS ON EXAMPLE SYSTEM")
            systems = get_systems()
            A, b, desc = systems[0]  # Use first example
            
            print_system(A, b, desc)
            print_determinant(A)
            
            print("\n" + "=" * 50)
            print("DIRECT METHODS COMPARISON")
            print("=" * 50)
            
            for key, (name, func) in DIRECT_METHODS.items():
                try:
                    x = func(A.copy(), b.copy())
                    print_direct_solution(x, name)
                except Exception as e:
                    print(f"{name}: Error - {e}")
            
            print("\n" + "=" * 50)
            print("ITERATIVE METHODS COMPARISON")
            print("=" * 50)
            
            x_true = gaussian_solve(A.copy(), b.copy())
            
            for key, (name, func) in ITERATIVE_METHODS.items():
                try:
                    if 'SOR' in name:
                        x, data, conv = func(A.copy(), b.copy(), omega=1.25, max_iter=100, tol=1e-6)
                    else:
                        x, data, conv = func(A.copy(), b.copy(), max_iter=100, tol=1e-6)
                    
                    iters = len(data) - 1
                    error = np.max(np.abs(x - x_true))
                    status = "✓ Converged" if conv else "✗ Not converged"
                    print(f"\n{name}: {status} in {iters} iterations (error: {error:.2e})")
                except Exception as e:
                    print(f"{name}: Error - {e}")
            
            print("\n" + "=" * 80)
        
        elif choice == '4':
            print("\nExiting...")
            break
        
        else:
            print("Invalid choice! Please enter 1-4.")


if __name__ == "__main__":
    main()
