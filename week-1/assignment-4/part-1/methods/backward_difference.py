def backward_difference_table(x_values: list, y_values: list, max_order: int = None):

    n = len(x_values)
    if n != len(y_values):
        raise ValueError("x_values and y_values must have the same length")
    
    if n < 2:
        raise ValueError("Need at least 2 points for difference calculation")
    
    # Determine maximum order
    if max_order is None:
        max_order = n - 1
    else:
        max_order = min(max_order, n - 1)
    
    # Initialize table
    differences = []
    
    # Calculate each order of differences
    current_diff = y_values[:]  # Start with 0-th order (original values)
    
    for order in range(max_order):
        next_diff = []
        for i in range(1, len(current_diff)):
            # Backward difference: ∇f(xi) = f(xi) - f(xi-1)
            diff = current_diff[i] - current_diff[i - 1]
            next_diff.append(diff)
        
        if not next_diff:
            break
            
        differences.append(next_diff)
        current_diff = next_diff
        
        # Stop if all differences are zero (or very close to zero)
        if all(abs(d) < 1e-10 for d in next_diff):
            break
    
    return {
        'x': x_values,
        'y': y_values,
        'differences': differences,
        'order': len(differences)
    }


def calculate_backward_difference(values: list, order: int = 1):
    if order < 1:
        return values
    
    current = values[:]
    for _ in range(order):
        next_diff = []
        for i in range(1, len(current)):
            next_diff.append(current[i] - current[i - 1])
        current = next_diff
        if not current:
            break
    
    return current
