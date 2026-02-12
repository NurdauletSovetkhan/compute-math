"""
Section 3: Derivatives using unequally spaced values of argument
- 3.1 Unequally Spaced Forward Difference
- 3.2 Unequally spaced backward difference
"""

def unequally_spaced_forward(x_values, f_values, point_index=0):
    """
    3.1: Calculate first derivative using forward difference for unequally spaced data
    Uses three-point formula based on Lagrange interpolation
    
    Parameters:
    - x_values: list of x values (unequally spaced)
    - f_values: list of function values
    - point_index: index of point where derivative is needed
    
    Returns:
    - first derivative at specified point
    """
    n = len(x_values)
    
    if point_index + 2 >= n:
        raise ValueError("Not enough points ahead for forward difference")
    
    x0 = x_values[point_index]
    x1 = x_values[point_index + 1]
    x2 = x_values[point_index + 2]
    
    f0 = f_values[point_index]
    f1 = f_values[point_index + 1]
    f2 = f_values[point_index + 2]
    
    # Three-point forward difference formula for unequal spacing
    # f'(x₀) ≈ f₀·[(2x₀-x₁-x₂)/((x₀-x₁)(x₀-x₂))] + f₁·[(2x₀-x₀-x₂)/((x₁-x₀)(x₁-x₂))] 
    #        + f₂·[(2x₀-x₀-x₁)/((x₂-x₀)(x₂-x₁))]
    
    coeff0 = (2 * x0 - x1 - x2) / ((x0 - x1) * (x0 - x2))
    coeff1 = (2 * x0 - x0 - x2) / ((x1 - x0) * (x1 - x2))
    coeff2 = (2 * x0 - x0 - x1) / ((x2 - x0) * (x2 - x1))
    
    derivative = f0 * coeff0 + f1 * coeff1 + f2 * coeff2
    
    return derivative

def unequally_spaced_backward(x_values, f_values, point_index=None):
    """
    3.2: Calculate first derivative using backward difference for unequally spaced data
    Uses three-point formula based on Lagrange interpolation
    
    Parameters:
    - x_values: list of x values (unequally spaced)
    - f_values: list of function values
    - point_index: index of point where derivative is needed (default: last point)
    
    Returns:
    - first derivative at specified point
    """
    n = len(x_values)
    if point_index is None:
        point_index = n - 1
    
    if point_index < 2:
        raise ValueError("Not enough points behind for backward difference")
    
    xn = x_values[point_index]
    xn_1 = x_values[point_index - 1]
    xn_2 = x_values[point_index - 2]
    
    fn = f_values[point_index]
    fn_1 = f_values[point_index - 1]
    fn_2 = f_values[point_index - 2]
    
    # Three-point backward difference formula for unequal spacing
    coeffn = (2 * xn - xn_1 - xn_2) / ((xn - xn_1) * (xn - xn_2))
    coeffn_1 = (2 * xn - xn - xn_2) / ((xn_1 - xn) * (xn_1 - xn_2))
    coeffn_2 = (2 * xn - xn - xn_1) / ((xn_2 - xn) * (xn_2 - xn_1))
    
    derivative = fn * coeffn + fn_1 * coeffn_1 + fn_2 * coeffn_2
    
    return derivative

def unequally_spaced_central(x_values, f_values, point_index):
    """
    Calculate first derivative using central-like approach for unequally spaced data
    Uses three-point formula centered at the point of interest
    
    Parameters:
    - x_values: list of x values (unequally spaced)
    - f_values: list of function values
    - point_index: index of point where derivative is needed
    
    Returns:
    - first derivative at specified point
    """
    n = len(x_values)
    
    if point_index <= 0 or point_index >= n - 1:
        raise ValueError("Central difference requires interior points")
    
    x_prev = x_values[point_index - 1]
    x_curr = x_values[point_index]
    x_next = x_values[point_index + 1]
    
    f_prev = f_values[point_index - 1]
    f_curr = f_values[point_index]
    f_next = f_values[point_index + 1]
    
    # Three-point formula using points before, at, and after
    coeff_prev = (2 * x_curr - x_curr - x_next) / ((x_prev - x_curr) * (x_prev - x_next))
    coeff_curr = (2 * x_curr - x_prev - x_next) / ((x_curr - x_prev) * (x_curr - x_next))
    coeff_next = (2 * x_curr - x_prev - x_curr) / ((x_next - x_prev) * (x_next - x_curr))
    
    derivative = f_prev * coeff_prev + f_curr * coeff_curr + f_next * coeff_next
    
    return derivative

def run_section3(x_values, f_values):
    """
    Execute Section 3: Unequally spaced numerical differentiation
    """
    n = len(x_values)
    
    print("\n" + "="*70)
    print("SECTION 3: DERIVATIVES USING UNEQUALLY SPACED VALUES")
    print("="*70)
    
    # Display spacing information
    print("\nSpacing between consecutive points:")
    for i in range(n - 1):
        spacing = x_values[i + 1] - x_values[i]
        print(f"h_{i} = x_{i+1} - x_{i} = {spacing:.6f}")
    
    print("\n" + "="*70)
    print("DERIVATIVE CALCULATIONS")
    print("="*70)
    
    # 3.1: Unequally Spaced Forward Difference
    print("\n--- 3.1: Unequally Spaced Forward Difference ---")
    for i in range(min(3, n - 2)):
        try:
            f_prime = unequally_spaced_forward(x_values, f_values, i)
            print(f"f'(x_{i}) at x = {x_values[i]:.4f}: {f_prime:.6f}")
        except Exception as e:
            print(f"Error at index {i}: {e}")
    
    # Central-like differences for interior points
    print("\n--- Unequally Spaced Central-Like Difference (Interior Points) ---")
    for i in range(1, n - 1):
        try:
            f_prime = unequally_spaced_central(x_values, f_values, i)
            print(f"f'(x_{i}) at x = {x_values[i]:.4f}: {f_prime:.6f}")
        except Exception as e:
            print(f"Error at index {i}: {e}")
    
    # 3.2: Unequally Spaced Backward Difference
    print("\n--- 3.2: Unequally Spaced Backward Difference ---")
    for i in range(max(2, n - 3), n):
        try:
            f_prime = unequally_spaced_backward(x_values, f_values, i)
            print(f"f'(x_{i}) at x = {x_values[i]:.4f}: {f_prime:.6f}")
        except Exception as e:
            print(f"Error at index {i}: {e}")
