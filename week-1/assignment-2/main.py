import numpy as np
from tabulate import tabulate
from gaussian_elimination import solve as gaussian_solve
from gauss_seidel import solve as gauss_seidel_solve
from test_systems import get_systems
from determinant import get_determinant
from inverse_matrix import get_inverse_matrix, print_inverse_matrix

def print_system(A, b, description):
    print(f"\n{description}")
    print("Coefficient Matrix A:")
    print(A)
    print("Constant Vector b:")
    print(b)


def print_direct_solution(x_true):
    print("\nDIRECT METHOD (Gaussian Elimination) - TRUE VALUE")
    for i, val in enumerate(x_true):
        print(f"x{i+1} = {val:.4f}")


def print_iteration_table(iterations_data, x_true):
    """Print table showing iterations of Gauss-Seidel method"""
    print("\nITERATIVE METHOD (Gauss-Seidel) - APPROXIMATION")
    
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


def solve_system(A, b, description, max_iter=50, tol=1e-6):
    """Solve a system using both direct and iterative methods"""
    print_system(A, b, description)
    print_determinant(A)
    
    # Solve with direct method (Gaussian Elimination)
    try:
        x_direct = gaussian_solve(A.copy(), b.copy())
        print_direct_solution(x_direct)
    except Exception as e:
        print(f"Error in Gaussian Elimination: {e}")
        return
    
    # Solve with iterative method (Gauss-Seidel)
    try:
        x_iterative, iterations_data, converged = gauss_seidel_solve(
            A.copy(), b.copy(), max_iter=max_iter, tol=tol
        )
        print_iteration_table(iterations_data, x_direct)
        print_direct_solution(x_direct)
        compare_solutions(x_direct, x_iterative, converged)
    except Exception as e:
        print(f"Error in Gauss-Seidel: {e}")
        return
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


def main():
    print("SYSTEM OF LINEAR EQUATIONS SOLVER")
    print("Direct Method: Gaussian Elimination (True Value)")
    print("Iterative Method: Gauss-Seidel (Approximate Value)")
    
    while True:
        print("\nMENU:")
        print("1. Run example systems")
        print("2. Enter your own system")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            # Run predefined examples
            systems = get_systems()
            for A, b, description in systems:
                solve_system(A, b, description)
            print_determinant(systems[0][0])  # Example of determinant calculation
            print("\nALL SYSTEMS SOLVED")
        
        elif choice == '2':
            # Get custom system from user
            A, b = get_user_system()
            if A is not None and b is not None:
                solve_system(A, b, "Custom System")
        
        elif choice == '3':
            print("\nExiting...")
            break
        
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
