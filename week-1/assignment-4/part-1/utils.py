def validate_data(x_values: list, y_values: list):
    """
    Validate input data for difference calculations.
    
    Parameters:
    -----------
    x_values : list
        List of x values
    y_values : list
        List of y values
    
    Raises:
    -------
    ValueError if data is invalid
    """
    if not x_values or not y_values:
        raise ValueError("x_values and y_values cannot be empty")
    
    if len(x_values) != len(y_values):
        raise ValueError("x_values and y_values must have the same length")
    
    if len(x_values) < 2:
        raise ValueError("Need at least 2 data points")

# ========================================================
#                       h
def check_equal_spacing(x_values: list, tolerance: float = 1e-10) -> tuple:
    if len(x_values) < 2:
        return False, None
    
    h = x_values[1] - x_values[0]
    
    for i in range(1, len(x_values) - 1):
        current_h = x_values[i + 1] - x_values[i]
        if abs(current_h - h) > tolerance:
            return False, None
    
    return True, h


def format_difference_symbol(order: int, method: str = "forward") -> str:
    symbol = "Δ" if method == "forward" else "∇"
    
    if order == 0:
        return "f(xᵢ)"
    elif order == 1:
        return f"{symbol}f(xᵢ)"
    else:
        # Unicode superscripts for order
        superscripts = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        order_str = str(order).translate(superscripts)
        return f"{symbol}{order_str}f(xᵢ)"


def create_difference_headers(max_order: int, method: str = "forward") -> list:
    headers = ["i", "xᵢ", "f(xᵢ)"]
    
    for order in range(1, max_order + 1):
        headers.append(format_difference_symbol(order, method))
    
    return headers


def detect_polynomial_degree(differences: list, tolerance: float = 1e-8) -> int:
    for order, diffs in enumerate(differences):
        if not diffs:
            continue
        
        # Check if all differences are approximately equal (constant)
        if len(diffs) > 1:
            first = diffs[0]
            is_constant = all(abs(d - first) < tolerance for d in diffs)
            if is_constant:
                return order + 1
        
        # Check if all differences are approximately zero
        if all(abs(d) < tolerance for d in diffs):
            return order + 1
    
    return -1  # Not a polynomial or degree > max_order


def get_function_value(func, x):
    if callable(func):
        return func(x)
    elif isinstance(func, dict):
        return func.get(x, None)
    else:
        raise ValueError("func must be callable or dictionary")
