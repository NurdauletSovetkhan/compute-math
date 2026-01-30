"""
Assignment 4 - Part 2: Interpolation Methods
Newton's Forward/Backward Difference and Lagrange Interpolation

This program automatically selects the appropriate interpolation method based on:
1. Data spacing (equal or variable)
2. Position of target point (start, middle, or end)
"""

import sys
from lagrange import lagrange_interpolation
from newton_forward import newton_forward_interpolation
from newton_backward import newton_backward_interpolation
from utils import (
    validate_data, 
    check_equal_spacing, 
    is_within_range,
)
from table import (
    display_input_data,
    display_interpolation_result,
    display_comparison_results,
    display_method_selection,
    display_spacing_info
)


def print_header():
    """Print program header."""
    print("\n" + "="*80)
    print(" "*20 + "INTERPOLATION CALCULATOR")
    print(" "*20 + "Assignment 4 - Part 2")
    print("="*80)


def print_menu():
    """Print main menu."""
    print("\n" + "-"*80)
    print("SELECT AN OPTION:")
    print("-"*80)
    print("  1. Automatic Method Selection (Recommended)")
    print("  2. Manual Input - Choose Method")
    print("  3. Test Example: Population Data (2010-2025)")
    print("  4. Test Example: Polynomial Data")
    print("  5. Compare All Methods")
    print("  0. Exit")
    print("-"*80)


def select_interpolation_method(x_values: list, y_values: list, x_target: float) -> tuple:
    """
    Automatically select the appropriate interpolation method.
    
    Logic:
    1. Check if data is equally spaced
       - If NO: Use Lagrange (universal method)
       - If YES: Continue to step 2
    
    2. Determine target position
       - If near START: Use Newton Forward
       - If near END: Use Newton Backward
       - If in MIDDLE: Use Lagrange (or compare both Newton methods)
    
    Parameters:
        x_values: List of x coordinates
        y_values: List of y coordinates
        x_target: Target point for interpolation
    
    Returns:
        tuple: (method_name, reason, method_function)
    """
    # Step 1: Check equal spacing
    is_equal, h = check_equal_spacing(x_values)
    
    if not is_equal:
        return (
            "Lagrange Interpolation",
            "Data is not equally spaced. Lagrange is the universal method.",
            lagrange_interpolation
        )
    
    # Step 2: Data is equally spaced, check target position
    within_range, position = is_within_range(x_values, x_target)
    
    if not within_range:
        return (
            "Lagrange Interpolation",
            f"Target x={x_target} is outside the data range. Using universal method.",
            lagrange_interpolation
        )
    
    # Determine best method based on position
    if position == 'start':
        return (
            "Newton Forward Difference",
            f"Target x={x_target} is near the beginning of equally-spaced data.",
            newton_forward_interpolation
        )
    elif position == 'end':
        return (
            "Newton Backward Difference",
            f"Target x={x_target} is near the end of equally-spaced data.",
            newton_backward_interpolation
        )
    else:  # position == 'middle'
        return (
            "Lagrange Interpolation",
            f"Target x={x_target} is in the middle of the data range. Lagrange provides balanced accuracy.",
            lagrange_interpolation
        )


def automatic_interpolation():
    """Perform interpolation with automatic method selection."""
    print("\n" + "="*80)
    print("AUTOMATIC METHOD SELECTION")
    print("="*80)
    
    # Get input data
    x_values, y_values, x_target = get_input_data()
    
    if x_values is None:
        return
    
    # Display input data
    display_input_data(x_values, y_values)
    
    # Check spacing
    is_equal, h = check_equal_spacing(x_values)
    display_spacing_info(x_values, is_equal, h)
    
    # Select method
    method_name, reason, method_func = select_interpolation_method(x_values, y_values, x_target)
    display_method_selection(method_name, reason)
    
    # Perform interpolation
    try:
        result = method_func(x_values, y_values, x_target)
        display_interpolation_result(result)
    except Exception as e:
        print(f"\n✗ Error during interpolation: {e}")


def manual_interpolation():
    """Perform interpolation with manual method selection."""
    print("\n" + "="*80)
    print("MANUAL METHOD SELECTION")
    print("="*80)
    
    # Get input data
    x_values, y_values, x_target = get_input_data()
    
    if x_values is None:
        return
    
    # Display input data
    display_input_data(x_values, y_values)
    
    # Check spacing
    is_equal, h = check_equal_spacing(x_values)
    display_spacing_info(x_values, is_equal, h)
    
    # Show method options
    print("\nAVAILABLE METHODS:")
    print("  1. Lagrange Interpolation (works for any spacing)")
    
    if is_equal:
        print("  2. Newton Forward Difference (best for beginning)")
        print("  3. Newton Backward Difference (best for end)")
    
    # Get user choice
    while True:
        try:
            choice = input("\nSelect method (1-3): ").strip()
            
            if choice == '1':
                result = lagrange_interpolation(x_values, y_values, x_target)
                display_interpolation_result(result)
                break
            elif choice == '2' and is_equal:
                result = newton_forward_interpolation(x_values, y_values, x_target)
                display_interpolation_result(result)
                break
            elif choice == '3' and is_equal:
                result = newton_backward_interpolation(x_values, y_values, x_target)
                display_interpolation_result(result)
                break
            else:
                print("Invalid choice. Please try again.")
        
        except Exception as e:
            print(f"\n✗ Error: {e}")
            break


def compare_all_methods():
    """Compare all applicable interpolation methods."""
    print("\n" + "="*80)
    print("COMPARE ALL METHODS")
    print("="*80)
    
    # Get input data
    x_values, y_values, x_target = get_input_data()
    
    if x_values is None:
        return
    
    # Display input data
    display_input_data(x_values, y_values)
    
    # Check spacing
    is_equal, h = check_equal_spacing(x_values)
    display_spacing_info(x_values, is_equal, h)
    
    # Perform interpolation with all applicable methods
    results = []
    
    # Lagrange (always applicable)
    try:
        result = lagrange_interpolation(x_values, y_values, x_target)
        results.append(result)
        print("\n✓ Lagrange interpolation completed")
    except Exception as e:
        print(f"\n✗ Lagrange failed: {e}")
    
    # Newton Forward (only if equally spaced)
    if is_equal:
        try:
            result = newton_forward_interpolation(x_values, y_values, x_target)
            results.append(result)
            print("✓ Newton Forward interpolation completed")
        except Exception as e:
            print(f"✗ Newton Forward failed: {e}")
        
        # Newton Backward (only if equally spaced)
        try:
            result = newton_backward_interpolation(x_values, y_values, x_target)
            results.append(result)
            print("✓ Newton Backward interpolation completed")
        except Exception as e:
            print(f"✗ Newton Backward failed: {e}")
    
    # Display comparison
    if results:
        display_comparison_results(results)
        
        # Display each result in detail
        for result in results:
            display_interpolation_result(result)


def get_input_data() -> tuple:
    """
    Get input data from user.
    
    Returns:
        tuple: (x_values, y_values, x_target) or (None, None, None) if error
    """
    try:
        # Get number of points
        n = int(input("\nEnter number of data points: "))
        if n < 2:
            print("✗ Error: Need at least 2 data points!")
            return None, None, None
        
        x_values = []
        y_values = []
        
        print(f"\nEnter {n} data points (x, y):")
        for i in range(n):
            x = float(input(f"  x[{i+1}]: "))
            y = float(input(f"  y[{i+1}]: "))
            x_values.append(x)
            y_values.append(y)
        
        # Get target point
        x_target = float(input("\nEnter target x value for interpolation: "))
        
        # Validate data
        validate_data(x_values, y_values)
        
        return x_values, y_values, x_target
    
    except ValueError as e:
        print(f"\n✗ Error: {e}")
        return None, None, None
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return None, None, None


def example_population_data():
    """Test with population data example."""
    print("\n" + "="*80)
    print("EXAMPLE: POPULATION DATA (2010-2025)")
    print("="*80)
    
    # Data from the image
    x_values = [2010, 2015, 2020, 2025]
    y_values = [16.5, 17.5, 18.7, 20.0]
    
    # Target: estimate population in 2018
    x_target = 2018
    
    print("\nDataset: Year vs Population (millions)")
    display_input_data(x_values, y_values)
    
    print(f"Task: Estimate population in year {x_target}")
    
    # Check spacing
    is_equal, h = check_equal_spacing(x_values)
    display_spacing_info(x_values, is_equal, h)
    
    # Select method
    method_name, reason, method_func = select_interpolation_method(x_values, y_values, x_target)
    display_method_selection(method_name, reason)
    
    # Perform interpolation
    result = method_func(x_values, y_values, x_target)
    display_interpolation_result(result)
    
    print(f"\n📊 Result: Estimated population in {x_target} = {result['y_estimated']:.2f} million")


def example_polynomial_data():
    """Test with polynomial data."""
    print("\n" + "="*80)
    print("EXAMPLE: POLYNOMIAL DATA")
    print("="*80)
    
    # Generate data from f(x) = x^3 - 2x^2 + 3x - 1
    x_values = [0, 1, 2, 3, 4]
    y_values = [x**3 - 2*x**2 + 3*x - 1 for x in x_values]
    
    # Target: estimate at x = 2.5
    x_target = 2.5
    
    print("\nDataset: f(x) = x³ - 2x² + 3x - 1")
    display_input_data(x_values, y_values)
    
    print(f"Task: Estimate f({x_target})")
    print(f"True value: f({x_target}) = {x_target**3 - 2*x_target**2 + 3*x_target - 1}")
    
    # Check spacing
    is_equal, h = check_equal_spacing(x_values)
    display_spacing_info(x_values, is_equal, h)
    
    # Select method
    method_name, reason, method_func = select_interpolation_method(x_values, y_values, x_target)
    display_method_selection(method_name, reason)
    
    # Perform interpolation
    result = method_func(x_values, y_values, x_target)
    display_interpolation_result(result)
    
    # Calculate error
    true_value = x_target**3 - 2*x_target**2 + 3*x_target - 1
    error = abs(result['y_estimated'] - true_value)
    print(f"\n📊 Interpolation error: {error:.2e}")


def main():
    """Main program loop."""
    print_header()
    
    while True:
        print_menu()
        
        try:
            choice = input("\nEnter your choice (0-5): ").strip()
            
            if choice == '0':
                print("\n" + "="*80)
                print("Thank you for using the Interpolation Calculator!")
                print("="*80 + "\n")
                sys.exit(0)
            
            elif choice == '1':
                automatic_interpolation()
            
            elif choice == '2':
                manual_interpolation()
            
            elif choice == '3':
                example_population_data()
            
            elif choice == '4':
                example_polynomial_data()
            
            elif choice == '5':
                compare_all_methods()
            
            else:
                print("\n✗ Invalid choice! Please enter a number from 0 to 5.")
            
            input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\n" + "="*80)
            print("Program interrupted by user.")
            print("="*80 + "\n")
            sys.exit(0)
        
        except Exception as e:
            print(f"\n✗ Error: {e}")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
