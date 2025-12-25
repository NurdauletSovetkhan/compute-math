import numpy as np
from tabulate import tabulate
from gaussian_elimination import solve as gaussian_solve
from gauss_seidel import solve as gauss_seidel_solve
from test_systems import get_systems




def print_system(A, b, description):
    """Print the system of equations"""
    print(f"\n{description}")
    print("Coefficient Matrix A:")
    print(A)
    print("\nConstant Vector b:")
    print(b)
    print()


def print_direct_solution(x_true):
    """Print the solution from direct method"""
    print("DIRECT METHOD (Gaussian Elimination) - TRUE VALUE")
    for i, val in enumerate(x_true):
        print(f"x{i+1} = {val:.10f}")
    print()


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
            row.append(f"{val:.8f}")
        
        if error is not None:
            row.append(f"{error:.4e}")
        else:
            row.append("N/A")
        
        row.append(f"{true_error:.4e}")
        table_data.append(row)
    
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print()


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
            f"{x_direct[i]:.10f}",
            f"{x_iterative[i]:.10f}",
            f"{error:.4e}"
        ])
    
    headers = ["Variable", "Direct", "Iterative", "Absolute Error"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    print(f"\nMaximum Absolute Error: {max_error:.4e}")
    print(f"Convergence Status: {'CONVERGED' if converged else 'NOT CONVERGED'}")
    print()


def solve_system(A, b, description, max_iter=50, tol=1e-6):
    """Solve a system using both direct and iterative methods"""
    print_system(A, b, description)
    
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
    
    print("\n\n")


def main():
    """Main function to solve all test systems"""
    print("\nDirect Method: Gaussian Elimination (True Value)")
    print("Iterative Method: Gauss-Seidel (Approximate Value)")
    
    # Get all test systems
    systems = get_systems()
    
    # Solve each system
    for A, b, description in systems:
        solve_system(A, b, description)
    
    print(" " * 35 + "ALL SYSTEMS SOLVED")


if __name__ == "__main__":
    main()
