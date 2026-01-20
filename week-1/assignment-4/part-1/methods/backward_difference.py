"""
Backward Difference Method

Backward difference formula:
∇f(xi) = f(xi) - f(xi-1)
∇²f(xi) = ∇f(xi) - ∇f(xi-1)
∇ⁿf(xi) = ∇ⁿ⁻¹f(xi) - ∇ⁿ⁻¹f(xi-1)
"""


def backward_difference_table(x_values: list, y_values: list, max_order: int = None):
    """  
    Parameters:
    -----------
    x_values : list
        List of x values
    y_values : list
        List of f(x) values
    max_order : int, optional
        Maximum order of differences to calculate.
        If None, calculates until differences become zero or n-1 order.
    
    Returns:
    --------
    dict with keys:
        'x': x values
        'y': y values (f(x))
        'differences': list of lists, where differences[i] contains i-th order differences
        'order': maximum order calculated
    """
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
        for i in range(1, len(current)):
            next_diff.append(current[i] - current[i - 1])
        current = next_diff
        if not current:
            break
    
    return current
