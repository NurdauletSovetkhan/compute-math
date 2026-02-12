import math

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
    Calculate derivative using Newton's forward difference formula
    
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
    Calculate derivative using Newton's backward difference formula
    
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

def unequally_spaced_forward(x_values, f_values, point_index=0):
    """
    Calculate first derivative using forward difference for unequally spaced data
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
    Calculate first derivative using backward difference for unequally spaced data
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

def find_extrema(x_values, f_values, h=None, is_equally_spaced=True):
    """
    Find local maxima and minima in tabulated function data
    
    Parameters:
    - x_values: list of x values
    - f_values: list of function values
    - h: step size (for equally spaced data)
    - is_equally_spaced: whether data points are equally spaced
    
    Returns:
    - list of dictionaries containing extrema information
    """
    n = len(f_values)
    extrema = []
    
    # Check interior points for potential extrema
    for i in range(1, n - 1):
        # Check if it's a local maximum or minimum
        if f_values[i] > f_values[i-1] and f_values[i] > f_values[i+1]:
            extrema_type = "Maximum"
        elif f_values[i] < f_values[i-1] and f_values[i] < f_values[i+1]:
            extrema_type = "Minimum"
        else:
            continue
        
        # Calculate first derivative at this point
        if is_equally_spaced and h is not None:
            f_prime = central_difference(f_values, h, i, order=1)
            f_double_prime = central_difference(f_values, h, i, order=2)
        else:
            f_prime = unequally_spaced_central(x_values, f_values, i)
            # For second derivative, use finite difference approximation
            if i > 1 and i < n - 2:
                h_left = x_values[i] - x_values[i-1]
                h_right = x_values[i+1] - x_values[i]
                f_double_prime = (f_values[i+1] - 2*f_values[i] + f_values[i-1]) / ((h_left + h_right) / 2)**2
            else:
                f_double_prime = None
        
        extrema.append({
            'index': i,
            'x': x_values[i],
            'f(x)': f_values[i],
            'type': extrema_type,
            'f_prime': f_prime,
            'f_double_prime': f_double_prime
        })
    
    return extrema

def first_derivative_test(extrema):
    """
    Apply first derivative test to classify extrema
    
    The first derivative test states:
    - If f'(x) changes from positive to negative, x is a local maximum
    - If f'(x) changes from negative to positive, x is a local minimum
    
    Parameters:
    - extrema: list of extrema dictionaries from find_extrema
    
    Returns:
    - Updated extrema list with first derivative test results
    """
    for ext in extrema:
        f_prime = ext['f_prime']
        
        # Classification based on first derivative
        if abs(f_prime) < 1e-6:  # Close to zero
            if ext['type'] == "Maximum":
                ext['first_derivative_test'] = "Critical point (f'≈0), likely Maximum"
            else:
                ext['first_derivative_test'] = "Critical point (f'≈0), likely Minimum"
        else:
            ext['first_derivative_test'] = f"f' = {f_prime:.6f} (not exactly zero, approximate extremum)"
    
    return extrema

def second_derivative_test(extrema):
    """
    Apply second derivative test to classify extrema
    
    The second derivative test states:
    - If f''(x) > 0 at a critical point, x is a local minimum (concave up)
    - If f''(x) < 0 at a critical point, x is a local maximum (concave down)
    - If f''(x) = 0, the test is inconclusive
    
    Parameters:
    - extrema: list of extrema dictionaries from find_extrema
    
    Returns:
    - Updated extrema list with second derivative test results
    """
    for ext in extrema:
        f_double_prime = ext['f_double_prime']
        
        if f_double_prime is None:
            ext['second_derivative_test'] = "Unable to compute (insufficient data)"
            ext['concavity'] = "Unknown"
        elif f_double_prime > 1e-6:
            ext['second_derivative_test'] = f"f'' = {f_double_prime:.6f} > 0 → Local Minimum"
            ext['concavity'] = "Concave up"
        elif f_double_prime < -1e-6:
            ext['second_derivative_test'] = f"f'' = {f_double_prime:.6f} < 0 → Local Maximum"
            ext['concavity'] = "Concave down"
        else:
            ext['second_derivative_test'] = f"f'' ≈ 0 → Test inconclusive"
            ext['concavity'] = "Inflection point"
    
    return extrema

def analyze_extrema(x_values, f_values, h=None, is_equally_spaced=True):
    """
    Complete analysis of extrema using both first and second derivative tests
    
    Parameters:
    - x_values: list of x values
    - f_values: list of function values
    - h: step size (for equally spaced data)
    - is_equally_spaced: whether data points are equally spaced
    """
    print("\n" + "="*70)
    print("SECTION 4: ANALYSIS OF TABULATED FUNCTIONS")
    print("="*70)
    
    # Find potential extrema
    extrema = find_extrema(x_values, f_values, h, is_equally_spaced)
    
    if not extrema:
        print("\nNo local maxima or minima found in the data.")
        return
    
    print(f"\n✓ Found {len(extrema)} potential extrema")
    
    # Apply first derivative test
    extrema = first_derivative_test(extrema)
    
    # Apply second derivative test
    extrema = second_derivative_test(extrema)
    
    # Display results
    print("\n" + "="*70)
    print("4.1 MAXIMA AND MINIMA OF TABULATED FUNCTION")
    print("="*70)
    
    for i, ext in enumerate(extrema, 1):
        print(f"\nExtremum #{i}:")
        print(f"  Location: x = {ext['x']:.6f} (index {ext['index']})")
        print(f"  Value: f(x) = {ext['f(x)']:.6f}")
        print(f"  Type: {ext['type']}")
    
    print("\n" + "="*70)
    print("4.2 FIRST DERIVATIVE TEST FOR MAXIMA AND MINIMA")
    print("="*70)
    print("\nTheory: At a local extremum, f'(x) = 0 (or very close to 0)")
    
    for i, ext in enumerate(extrema, 1):
        print(f"\nExtremum #{i} at x = {ext['x']:.6f}:")
        print(f"  {ext['first_derivative_test']}")
    
    print("\n" + "="*70)
    print("4.3 SECOND DERIVATIVE TEST FOR MAXIMA AND MINIMA")
    print("="*70)
    print("\nTheory:")
    print("  • If f''(x) > 0 → Local Minimum (concave up)")
    print("  • If f''(x) < 0 → Local Maximum (concave down)")
    print("  • If f''(x) = 0 → Test inconclusive")
    
    for i, ext in enumerate(extrema, 1):
        print(f"\nExtremum #{i} at x = {ext['x']:.6f}:")
        print(f"  {ext['second_derivative_test']}")
        print(f"  Concavity: {ext['concavity']}")
        
        # Verify consistency
        if ext['type'] == "Maximum" and ext['concavity'] == "Concave down":
            print(f"  ✓ Verification: Confirmed as Maximum")
        elif ext['type'] == "Minimum" and ext['concavity'] == "Concave up":
            print(f"  ✓ Verification: Confirmed as Minimum")
        elif ext['concavity'] != "Unknown" and ext['concavity'] != "Inflection point":
            print(f"  ⚠ Warning: Type mismatch - review data")
    
    print("\n" + "="*70)
    print("SUMMARY OF EXTREMA")
    print("="*70)
    
    maxima = [ext for ext in extrema if ext['type'] == "Maximum"]
    minima = [ext for ext in extrema if ext['type'] == "Minimum"]
    
    if maxima:
        print("\nLocal Maxima:")
        for ext in maxima:
            print(f"  x = {ext['x']:.6f}, f(x) = {ext['f(x)']:.6f}")
    
    if minima:
        print("\nLocal Minima:")
        for ext in minima:
            print(f"  x = {ext['x']:.6f}, f(x) = {ext['f(x)']:.6f}")

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

def equal_spacing(x_values, f_values, h):
    """
    Handle equally spaced differentiation
    """
    n = len(x_values)
    
    print("\n" + "="*70)
    print("EQUALLY SPACED NUMERICAL DIFFERENTIATION")
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
    
    # Forward differences at the beginning
    print("\n--- Newton's Forward Difference Method ---")
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
    
    # Backward differences at the end
    print("\n--- Newton's Backward Difference Method ---")
    for i in range(max(n - 3, 2), n):
        try:
            f_prime = newton_backward_derivative(x_values, f_values, h, i, order=1)
            print(f"f'(x_{i}) at x = {x_values[i]:.4f}: {f_prime:.6f}")
            
            if i >= 2:
                f_double_prime = newton_backward_derivative(x_values, f_values, h, i, order=2)
                print(f"f''(x_{i}) at x = {x_values[i]:.4f}: {f_double_prime:.6f}")
        except Exception as e:
            print(f"Error calculating at index {i}: {e}")

def unequal_spacing(x_values, f_values):
    """
    Handle unequally spaced differentiation
    """
    n = len(x_values)
    
    print("\n" + "="*70)
    print("UNEQUALLY SPACED NUMERICAL DIFFERENTIATION")
    print("="*70)
    
    # Display spacing information
    print("\nSpacing between consecutive points:")
    for i in range(n - 1):
        spacing = x_values[i + 1] - x_values[i]
        print(f"h_{i} = x_{i+1} - x_{i} = {spacing:.6f}")
    
    print("\n" + "="*70)
    print("DERIVATIVE CALCULATIONS")
    print("="*70)
    
    # Forward differences
    print("\n--- Unequally Spaced Forward Difference ---")
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
    
    # Backward differences
    print("\n--- Unequally Spaced Backward Difference ---")
    for i in range(max(2, n - 3), n):
        try:
            f_prime = unequally_spaced_backward(x_values, f_values, i)
            print(f"f'(x_{i}) at x = {x_values[i]:.4f}: {f_prime:.6f}")
        except Exception as e:
            print(f"Error at index {i}: {e}")

def main():
    """
    Main function integrating with your existing code structure
    """
    print("="*70)
    print("NUMERICAL DIFFERENTIATION CALCULATOR")
    print("="*70)
    
    # Input x values
    x_input = input("\nEnter x values separated by spaces: ")
    x_values = [float(val) for val in x_input.split()]
    n = len(x_values)
    
    if n < 3:
        print("Error: Need at least 3 data points for numerical differentiation")
        return
    
    # Input function
    print("\nAvailable: sin, cos, tan, log, exp, sqrt, e, pi")
    f = input("Enter your function f(x) (e.g., x**2 or sin(x)): ")
    
    # Create tool dictionary for function evaluation
    tool = {
        "x": 0, 
        "sin": math.sin, 
        "cos": math.cos, 
        "tan": math.tan, 
        "log": math.log, 
        "exp": math.exp, 
        "sqrt": math.sqrt, 
        "e": math.e, 
        "pi": math.pi
    }
    
    # Option to use manual f(x) values or compute from function
    choice = input("\nDo you want to (1) Enter f(x) values manually or (2) Compute from function? Enter 1 or 2: ")
    
    if choice == '1':
        f_input = input("Enter f(x) values separated by spaces: ")
        f_values = [float(val) for val in f_input.split()]
        
        if len(f_values) != n:
            print(f"Error: Number of f(x) values ({len(f_values)}) must match number of x values ({n})")
            return
    else:
        # Compute f(x) values from function
        f_values = []
        for x in x_values:
            tool["x"] = x
            try:
                f_values.append(eval(f, {"__builtins__": None}, tool))
            except Exception as e:
                print(f"Error evaluating function at x={x}: {e}")
                return
    
    # Display data table
    print("\n" + "="*70)
    print("DATA TABLE")
    print("="*70)
    print(f"{'i':<5} {'x':<15} {'f(x)':<15}")
    print("-" * 40)
    for i in range(n):
        print(f"{i:<5} {x_values[i]:<15.6f} {f_values[i]:<15.6f}")
    print("="*70)
    
    # Check if spacing is equal
    h = x_values[1] - x_values[0]
    is_equally_spaced = True
    
    for i in range(n - 1):
        current_spacing = x_values[i + 1] - x_values[i]
        if not math.isclose(h, current_spacing, rel_tol=1e-7):
            is_equally_spaced = False
            break
    
    # Process based on spacing type
    if is_equally_spaced:
        print(f"\n✓ Data points are EQUALLY SPACED with h = {h:.6f}")
        equal_spacing(x_values, f_values, h)
    else:
        print("\n✓ Data points are UNEQUALLY SPACED")
        unequal_spacing(x_values, f_values)
    
    # Analyze extrema (Section 4)
    analyze_extrema(x_values, f_values, h if is_equally_spaced else None, is_equally_spaced)
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()
