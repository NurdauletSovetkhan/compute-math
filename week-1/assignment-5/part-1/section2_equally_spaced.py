"""
Section 2: Derivatives using equally spaced values of argument
- 2.1 Numerical differentiation using Newton's forward difference formula
- 2.2 Numerical differentiation using Newton's backward difference formula
"""

def forward_difference_table(f_values, n):
    """
    Construct forward difference table for equally spaced data
    Returns a 2D list where table[i][j] represents Δ^j f_i
    """
    table = [[0 for _ in range(n)] for _ in range(n)]
    
    # First column is the function values
    for i in range(n):
        table[i][0] = f_values[i]
    
    # Compute forward differences
    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = table[i + 1][j - 1] - table[i][j - 1]
    
    return table

def backward_difference_table(f_values, n):
    """
    Construct backward difference table for equally spaced data
    Returns a 2D list where table[i][j] represents ∇^j f_i
    """
    table = [[0 for _ in range(n)] for _ in range(n)]
    
    # First column is the function values
    for i in range(n):
        table[i][0] = f_values[i]
    
    # Compute backward differences
    for j in range(1, n):
        for i in range(j, n):
            table[i][j] = table[i][j - 1] - table[i - 1][j - 1]
    
    return table

def newton_forward_derivative(x_values, f_values, h, point_index=0, order=1):
    """
    2.1: Calculate derivative using Newton's forward difference formula
    
    Parameters:
    - x_values: list of x values
    - f_values: list of function values
    - h: step size
    - point_index: index of point where derivative is needed (default: 0)
    - order: derivative order (1 or 2)
    
    Returns:
    - derivative value at specified point
    """
    n = len(f_values)
    table = forward_difference_table(f_values, n)
    
    if order == 1:
        # First derivative: f'(x₀) ≈ (1/h)[Δf₀ - (1/2)Δ²f₀ + (1/3)Δ³f₀ - ...]
        derivative = table[point_index][1] / h
        
        # Add higher order terms for better accuracy
        if n > point_index + 2:
            derivative -= table[point_index][2] / (2 * h)
        if n > point_index + 3:
            derivative += table[point_index][3] / (3 * h)
        if n > point_index + 4:
            derivative -= table[point_index][4] / (4 * h)
            
    elif order == 2:
        # Second derivative: f''(x₀) ≈ (1/h²)[Δ²f₀ - Δ³f₀ + (11/12)Δ⁴f₀ - ...]
        derivative = table[point_index][2] / (h ** 2)
        
        if n > point_index + 3:
            derivative -= table[point_index][3] / (h ** 2)
        if n > point_index + 4:
            derivative += (11 * table[point_index][4]) / (12 * h ** 2)
    else:
        raise ValueError("Only first and second derivatives are supported")
    
    return derivative

def newton_backward_derivative(x_values, f_values, h, point_index=None, order=1):
    """
    2.2: Calculate derivative using Newton's backward difference formula
    
    Parameters:
    - x_values: list of x values
    - f_values: list of function values
    - h: step size
    - point_index: index of point where derivative is needed (default: last point)
    - order: derivative order (1 or 2)
    
    Returns:
    - derivative value at specified point
    """
    n = len(f_values)
    if point_index is None:
        point_index = n - 1
    
    table = backward_difference_table(f_values, n)
    
    if order == 1:
        # First derivative: f'(xₙ) ≈ (1/h)[∇fₙ + (1/2)∇²fₙ + (1/3)∇³fₙ + ...]
        derivative = table[point_index][1] / h
        
        if point_index >= 2:
            derivative += table[point_index][2] / (2 * h)
        if point_index >= 3:
            derivative += table[point_index][3] / (3 * h)
        if point_index >= 4:
            derivative += table[point_index][4] / (4 * h)
            
    elif order == 2:
        # Second derivative: f''(xₙ) ≈ (1/h²)[∇²fₙ + ∇³fₙ + (11/12)∇⁴fₙ + ...]
        derivative = table[point_index][2] / (h ** 2)
        
        if point_index >= 3:
            derivative += table[point_index][3] / (h ** 2)
        if point_index >= 4:
            derivative += (11 * table[point_index][4]) / (12 * h ** 2)
    else:
        raise ValueError("Only first and second derivatives are supported")
    
    return derivative

def central_difference(f_values, h, point_index, order=1):
    """
    Calculate derivative using central difference formula
    (Used for interior points in equally spaced data)
    
    Parameters:
    - f_values: list of function values
    - h: step size
    - point_index: index of point where derivative is needed
    - order: derivative order (1 or 2)
    """
    n = len(f_values)
    
    if point_index <= 0 or point_index >= n - 1:
        raise ValueError("Central difference requires interior points")
    
    if order == 1:
        # f'(xᵢ) ≈ (f(xᵢ₊₁) - f(xᵢ₋₁)) / (2h)
        derivative = (f_values[point_index + 1] - f_values[point_index - 1]) / (2 * h)
    elif order == 2:
        # f''(xᵢ) ≈ (f(xᵢ₊₁) - 2f(xᵢ) + f(xᵢ₋₁)) / h²
        derivative = (f_values[point_index + 1] - 2 * f_values[point_index] + 
                     f_values[point_index - 1]) / (h ** 2)
    else:
        raise ValueError("Only first and second derivatives are supported")
    
    return derivative

def print_difference_table(table, n, table_type="Forward"):
    """Print forward or backward difference table in formatted manner"""
    print(f"\n{table_type} Difference Table:")
    print("-" * (15 * (n + 1)))
    
    # Header
    header = "i\tf(x)\t"
    for j in range(1, n):
        if table_type == "Forward":
            header += f"Δ^{j}f\t"
        else:
            header += f"∇^{j}f\t"
    print(header)
    print("-" * (15 * (n + 1)))
    
    # Data rows
    for i in range(n):
        row = f"{i}\t{table[i][0]:.4f}\t"
        for j in range(1, n):
            if table[i][j] != 0 or (table_type == "Forward" and i + j < n) or (table_type == "Backward" and i >= j):
                row += f"{table[i][j]:.4f}\t"
            else:
                row += "-\t"
        print(row)
    print("-" * (15 * (n + 1)))

def run_section2(x_values, f_values, h):
    """
    Execute Section 2: Equally spaced numerical differentiation
    """
    n = len(x_values)
    
    print("\n" + "="*70)
    print("SECTION 2: DERIVATIVES USING EQUALLY SPACED VALUES")
    print("="*70)
    print(f"\nStep size h = {h:.6f}")
    
    # Construct and display forward difference table
    forward_table = forward_difference_table(f_values, n)
    print_difference_table(forward_table, n, "Forward")
    
    # Construct and display backward difference table
    backward_table = backward_difference_table(f_values, n)
    print_difference_table(backward_table, n, "Backward")
    
    print("\n" + "="*70)
    print("DERIVATIVE CALCULATIONS")
    print("="*70)
    
    # 2.1: Newton's Forward Difference Method (for beginning points)
    print("\n--- 2.1: Newton's Forward Difference Formula ---")
    for i in range(min(3, n - 2)):
        try:
            f_prime = newton_forward_derivative(x_values, f_values, h, i, order=1)
            print(f"f'(x_{i}) at x = {x_values[i]:.4f}: {f_prime:.6f}")
            
            if n > i + 2:
                f_double_prime = newton_forward_derivative(x_values, f_values, h, i, order=2)
                print(f"f''(x_{i}) at x = {x_values[i]:.4f}: {f_double_prime:.6f}")
        except Exception as e:
            print(f"Error calculating at index {i}: {e}")
    
    # Central differences for interior points
    print("\n--- Central Difference Method (Interior Points) ---")
    for i in range(1, n - 1):
        try:
            f_prime = central_difference(f_values, h, i, order=1)
            print(f"f'(x_{i}) at x = {x_values[i]:.4f}: {f_prime:.6f}")
            
            f_double_prime = central_difference(f_values, h, i, order=2)
            print(f"f''(x_{i}) at x = {x_values[i]:.4f}: {f_double_prime:.6f}")
        except Exception as e:
            print(f"Error calculating at index {i}: {e}")
    
    # 2.2: Newton's Backward Difference Method (for ending points)
    print("\n--- 2.2: Newton's Backward Difference Formula ---")
    for i in range(max(n - 3, 2), n):
        try:
            f_prime = newton_backward_derivative(x_values, f_values, h, i, order=1)
            print(f"f'(x_{i}) at x = {x_values[i]:.4f}: {f_prime:.6f}")
            
            if i >= 2:
                f_double_prime = newton_backward_derivative(x_values, f_values, h, i, order=2)
                print(f"f''(x_{i}) at x = {x_values[i]:.4f}: {f_double_prime:.6f}")
        except Exception as e:
            print(f"Error calculating at index {i}: {e}")
