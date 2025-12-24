import re
import numpy as np


def parse_equation(equation_str):
    """
    Parse a single equation string and extract coefficients.
    
    Example: "4x + y + z = 7" -> ([4, 1, 1], 7)
    
    Parameters:
    equation_str: string representation of equation
    
    Returns:
    tuple: (coefficients_list, constant)
    """
    # Split by '='
    parts = equation_str.split('=')
    if len(parts) != 2:
        raise ValueError(f"Invalid equation format: {equation_str}")
    
    left_side = parts[0].strip()
    right_side = parts[1].strip()
    
    try:
        constant = float(right_side)
    except ValueError:
        raise ValueError(f"Invalid constant value: {right_side}")
    
    # Find all variables and their coefficients
    # Pattern matches: optional sign, optional coefficient, variable
    pattern = r'([+-]?\s*\d*\.?\d*)\s*([a-zA-Z]\d*)'
    matches = re.findall(pattern, left_side)
    
    if not matches:
        raise ValueError(f"No variables found in equation: {equation_str}")
    
    # Extract coefficients and variable names
    terms = {}
    for coef, var in matches:
        coef = coef.replace(' ', '')
        
        # Handle empty coefficient (means 1 or -1)
        if coef == '' or coef == '+':
            coef = 1.0
        elif coef == '-':
            coef = -1.0
        else:
            coef = float(coef)
        
        terms[var] = coef
    
    return terms, constant


def parse_system(equations_text):
    """
    Parse multiple equations and create coefficient matrix A and constant vector b.
    
    Parameters:
    equations_text: multi-line string or list of equation strings
    
    Returns:
    tuple: (A, b) where A is coefficient matrix and b is constants vector
    """
    # Handle both string and list input
    if isinstance(equations_text, str):
        equations = [eq.strip() for eq in equations_text.strip().split('\n') if eq.strip()]
    else:
        equations = [eq.strip() for eq in equations_text if eq.strip()]
    
    if not equations:
        raise ValueError("No equations provided")
    
    # Parse all equations
    all_terms = []
    constants = []
    all_vars = set()
    
    for eq in equations:
        terms, constant = parse_equation(eq)
        all_terms.append(terms)
        constants.append(constant)
        all_vars.update(terms.keys())
    
    # Sort variables alphabetically
    variables = sorted(all_vars)
    n_vars = len(variables)
    n_eqs = len(equations)
    
    if n_eqs != n_vars:
        print(f"Warning: System has {n_eqs} equations and {n_vars} variables")
    
    # Create coefficient matrix
    A = np.zeros((n_eqs, n_vars))
    for i, terms in enumerate(all_terms):
        for j, var in enumerate(variables):
            A[i, j] = terms.get(var, 0.0)
    
    b = np.array(constants)
    
    return A, b, variables


def read_system_from_input():
    """
    Read system of equations from user input.
    
    Returns:
    tuple: (A, b, variables)
    """
    print("\nEnter system of equations (one per line)")
    print("Example format: 4x + y + z = 7")
    print("Press Enter twice to finish:\n")
    
    equations = []
    empty_count = 0
    
    while True:
        line = input()
        
        if not line.strip():
            empty_count += 1
            if empty_count >= 2 or (equations and empty_count >= 1):
                break
        else:
            empty_count = 0
            equations.append(line)
    
    if not equations:
        raise ValueError("No equations entered")
    
    return parse_system(equations)


def read_system_from_string(system_str):
    """
    Parse system from a multi-line string.
    
    Parameters:
    system_str: string containing equations separated by newlines
    
    Returns:
    tuple: (A, b, variables)
    """
    return parse_system(system_str)
