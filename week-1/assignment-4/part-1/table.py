from tabulate import tabulate
from utils import format_difference_symbol, create_difference_headers, detect_polynomial_degree


def display_forward_difference_table(result: dict, precision: int = 4):
    x_values = result['x']
    y_values = result['y']
    differences = result['differences']
    max_order = result['order']
    
    # Create headers
    headers = create_difference_headers(max_order, method="forward")
    
    # Build table data
    table_data = []
    n = len(x_values)
    
    for i in range(n):
        row = [i + 1, x_values[i], y_values[i]]
        
        # Add differences of each order
        for order in range(max_order):
            if order < len(differences) and i < len(differences[order]):
                row.append(differences[order][i])
            else:
                row.append("")
        
        table_data.append(row)
    
    # Format numbers
    formatted_data = []
    for row in table_data:
        formatted_row = [row[0]]  # index stays as int
        for j in range(1, len(row)):
            if row[j] == "":
                formatted_row.append("")
            elif isinstance(row[j], (int, float)):
                # Check if it's close to integer
                if isinstance(row[j], float) and abs(row[j] - round(row[j])) < 1e-10:
                    formatted_row.append(int(round(row[j])))
                else:
                    formatted_row.append(f"{row[j]:.{precision}f}")
            else:
                formatted_row.append(row[j])
        formatted_data.append(formatted_row)
    
    # Display table
    print("\n" + "="*80)
    print("FORWARD DIFFERENCE TABLE")
    print("="*80)
    print(tabulate(formatted_data, headers=headers, tablefmt="grid"))
    
    # Detect polynomial degree
    degree = detect_polynomial_degree(differences)
    if degree > 0:
        print(f"\n  Detected: Polynomial of degree {degree}")
        print(f"  (Differences become constant at order {degree})")
    
    print()


def display_backward_difference_table(result: dict, precision: int = 4):
    x_values = result['x']
    y_values = result['y']
    differences = result['differences']
    max_order = result['order']
    
    # Create headers
    headers = create_difference_headers(max_order, method="backward")
    
    # Build table data
    table_data = []
    n = len(x_values)
    
    for i in range(n):
        row = [i + 1, x_values[i], y_values[i]]
        
        # Add differences of each order
        # For backward differences, we need to account for the offset
        for order in range(max_order):
            if order < len(differences):
                # The i-th row should show the difference that corresponds to x[i]
                # For backward diff of order k, index j corresponds to x[j+k]
                index = i - (order + 1)
                if 0 <= index < len(differences[order]):
                    row.append(differences[order][index])
                else:
                    row.append("")
            else:
                row.append("")
        
        table_data.append(row)
    
    # Format numbers
    formatted_data = []
    for row in table_data:
        formatted_row = [row[0]]  # index stays as int
        for j in range(1, len(row)):
            if row[j] == "":
                formatted_row.append("")
            elif isinstance(row[j], (int, float)):
                # Check if it's close to integer
                if isinstance(row[j], float) and abs(row[j] - round(row[j])) < 1e-10:
                    formatted_row.append(int(round(row[j])))
                else:
                    formatted_row.append(f"{row[j]:.{precision}f}")
            else:
                formatted_row.append(row[j])
        formatted_data.append(formatted_row)
    
    # Display table
    print("\n" + "="*80)
    print("BACKWARD DIFFERENCE TABLE")
    print("="*80)
    print(tabulate(formatted_data, headers=headers, tablefmt="grid"))
    
    # Detect polynomial degree
    degree = detect_polynomial_degree(differences)
    if degree > 0:
        print(f"\n  Detected: Polynomial of degree {degree}")
        print(f"  (Differences become constant at order {degree})")
    
    print()


def display_data_table(x_values: list, y_values: list, title: str = "INPUT DATA"):
    headers = ["i", "xᵢ", "f(xᵢ)"]
    table_data = []
    
    for i, (x, y) in enumerate(zip(x_values, y_values)):
        table_data.append([i + 1, x, y])
    
    print("\n" + "="*40)
    print(title)
    print("="*40)
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print()


def display_comparison(forward_result: dict, backward_result: dict, precision: int = 4):
    print("\n" + "="*80)
    print("COMPARISON: FORWARD vs BACKWARD DIFFERENCES")
    print("="*80)
    
    display_forward_difference_table(forward_result, precision)
    display_backward_difference_table(backward_result, precision)
