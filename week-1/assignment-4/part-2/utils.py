def check_equal_spacing(x_values: list, tolerance: float = 1e-10) -> tuple:
    """
    Check if x values are equally spaced.
    
    Returns:
        tuple: (is_equal, h) where is_equal is bool and h is the step size
    """
    if len(x_values) < 2:
        return False, None
    
    h = x_values[1] - x_values[0]
    
    for i in range(1, len(x_values) - 1):
        current_h = x_values[i + 1] - x_values[i]
        if abs(current_h - h) > tolerance:
            return False, None
    
    return True, h


def validate_data(x_values: list, y_values: list):
    """
    Validate input data for interpolation.
    
    Raises:
        ValueError if data is invalid
    """
    if not x_values or not y_values:
        raise ValueError("x_values and y_values cannot be empty")
    
    if len(x_values) != len(y_values):
        raise ValueError("x_values and y_values must have the same length")
    
    if len(x_values) < 2:
        raise ValueError("Need at least 2 data points for interpolation")


def format_polynomial(coefficients: list, precision: int = 6) -> str:
    """
    Format polynomial coefficients into a readable string.
    
    Parameters:
        coefficients: List of coefficients [c0, c1, c2, ...] for c0 + c1*x + c2*x^2 + ...
        precision: Number of decimal places to display
    
    Returns:
        Formatted polynomial string
    """
    if not coefficients:
        return "0"
    
    terms = []
    n = len(coefficients)
    
    for i in range(n - 1, -1, -1):  # Start from highest degree
        coef = coefficients[i]
        
        # Skip zero coefficients
        if abs(coef) < 10**(-precision):
            continue
        
        # Format coefficient
        if abs(coef - round(coef)) < 1e-10:
            coef_str = f"{int(round(coef))}"
        else:
            coef_str = f"{coef:.{precision}f}".rstrip('0').rstrip('.')
        
        # Build term
        if i == 0:
            # Constant term
            terms.append(coef_str)
        elif i == 1:
            # Linear term
            if abs(coef - 1) < 1e-10:
                terms.append("x")
            elif abs(coef + 1) < 1e-10:
                terms.append("-x")
            else:
                terms.append(f"{coef_str}x")
        else:
            # Higher degree terms
            if abs(coef - 1) < 1e-10:
                terms.append(f"x^{i}")
            elif abs(coef + 1) < 1e-10:
                terms.append(f"-x^{i}")
            else:
                terms.append(f"{coef_str}x^{i}")
    
    if not terms:
        return "0"
    
    # Join terms with proper signs
    result = terms[0]
    for term in terms[1:]:
        if term.startswith('-'):
            result += f" - {term[1:]}"
        else:
            result += f" + {term}"
    
    return result


def format_polynomial_pretty(coefficients: list, precision: int = 4) -> str:
    """
    Format polynomial with better visual appearance using Unicode.
    
    Parameters:
        coefficients: List of coefficients [c0, c1, c2, ...] for c0 + c1*x + c2*x^2 + ...
        precision: Number of decimal places to display
    
    Returns:
        Formatted polynomial string with Unicode superscripts
    """
    if not coefficients:
        return "0"
    
    # Unicode superscripts
    superscripts = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    
    terms = []
    n = len(coefficients)
    
    for i in range(n - 1, -1, -1):  # Start from highest degree
        coef = coefficients[i]
        
        # Skip zero coefficients
        if abs(coef) < 10**(-precision):
            continue
        
        # Format coefficient
        if abs(coef - round(coef)) < 1e-10:
            coef_str = f"{int(round(coef))}"
        else:
            coef_str = f"{coef:.{precision}f}".rstrip('0').rstrip('.')
        
        # Build term
        if i == 0:
            # Constant term
            terms.append(coef_str)
        elif i == 1:
            # Linear term
            if abs(coef - 1) < 1e-10:
                terms.append("x")
            elif abs(coef + 1) < 1e-10:
                terms.append("-x")
            else:
                terms.append(f"{coef_str}x")
        else:
            # Higher degree terms with Unicode superscripts
            power_str = str(i).translate(superscripts)
            if abs(coef - 1) < 1e-10:
                terms.append(f"x{power_str}")
            elif abs(coef + 1) < 1e-10:
                terms.append(f"-x{power_str}")
            else:
                terms.append(f"{coef_str}x{power_str}")
    
    if not terms:
        return "0"
    
    # Join terms with proper signs
    result = terms[0]
    for term in terms[1:]:
        if term.startswith('-'):
            result += f" - {term[1:]}"
        else:
            result += f" + {term}"
    
    return result


def evaluate_polynomial(coefficients: list, x: float) -> float:
    """
    Evaluate polynomial at given x using Horner's method.
    
    Parameters:
        coefficients: List of coefficients [c0, c1, c2, ...] for c0 + c1*x + c2*x^2 + ...
        x: Point at which to evaluate
    
    Returns:
        Value of polynomial at x
    """
    if not coefficients:
        return 0.0
    
    # Horner's method: more numerically stable
    result = coefficients[-1]
    for i in range(len(coefficients) - 2, -1, -1):
        result = result * x + coefficients[i]
    
    return result


def find_nearest_index(x_values: list, x_target: float) -> int:
    """
    Find the index of the x value nearest to x_target.
    
    Parameters:
        x_values: List of x values
        x_target: Target x value
    
    Returns:
        Index of nearest x value
    """
    min_dist = float('inf')
    nearest_idx = 0
    
    for i, x in enumerate(x_values):
        dist = abs(x - x_target)
        if dist < min_dist:
            min_dist = dist
            nearest_idx = i
    
    return nearest_idx


def is_within_range(x_values: list, x_target: float, tolerance: float = 0.1) -> tuple:
    """
    Check if x_target is within or near the data range.
    
    Parameters:
        x_values: List of x values
        x_target: Target x value
        tolerance: Fraction of range to allow outside (default 10%)
    
    Returns:
        tuple: (is_within, position) where position is 'start', 'middle', or 'end'
    """
    x_min = min(x_values)
    x_max = max(x_values)
    range_span = x_max - x_min
    extended_min = x_min - tolerance * range_span
    extended_max = x_max + tolerance * range_span
    
    if x_target < extended_min or x_target > extended_max:
        return False, None
    
    # Determine position
    if x_target <= x_min + 0.25 * range_span:
        return True, 'start'
    elif x_target >= x_max - 0.25 * range_span:
        return True, 'end'
    else:
        return True, 'middle'