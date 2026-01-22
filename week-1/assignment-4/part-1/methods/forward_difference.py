def forward_difference_table(x_values: list, y_values: list, max_order: int = None):
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
    # differences[0] is the 1st order difference (Δf)
    # differences[1] is the 2nd order difference (Δ²f)
    differences = []
    
    # Calculate each order of differences
    current_diff = y_values[:]  # Start with 0-th order (original values)
    
    for order in range(max_order):
        next_diff = []
        for i in range(len(current_diff) - 1):
            # Forward difference: Δf(xi) = f(xi+1) - f(xi)
            diff = current_diff[i + 1] - current_diff[i]
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


def calculate_forward_difference(values: list, order: int = 1):
    """   
    Parameters:
    -----------
    values : list
        List of values
    order : int
        Order of difference to calculate
    
    Returns:
    --------
    list : differences of specified order
    """
    if order < 1:
        return values
    
    current = values[:]
    for _ in range(order):
        next_diff = []
        for i in range(len(current) - 1):
            next_diff.append(current[i + 1] - current[i])
        current = next_diff
        if not current:
            break
    
    return current
