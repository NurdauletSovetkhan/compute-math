import sys
from methods.forward_difference import forward_difference_table
from methods.backward_difference import backward_difference_table
from table import (
    display_forward_difference_table, 
    display_backward_difference_table,
    display_data_table,
    display_comparison
)
from utils import validate_data, check_equal_spacing
import examples


def print_header():
    print("\n" + "="*80)
    print(" "*20 + "FINITE DIFFERENCES CALCULATOR")
    print(" "*25 + "Assignment 4 - Part 1")
    print("="*80)


def print_menu():
    print("\n" + "-"*80)
    print("SELECT AN OPTION:")
    print("-"*80)
    print("  1. Forward Differences - Manual Input")
    print("  2. Backward Differences - Manual Input")
    print("  3. Compare Forward & Backward - Manual Input")
    print("  4. Example 1: Polynomial f(x) = x³ - 2x² + 3x - 1")
    print("  5. Example 2: Exponential Function f(x) = 2^x")
    print("  6. Run All Examples")
    print("  0. Exit")
    print("-"*80)


def get_manual_input():
    """
    Get manual input from user.
    
    Returns:
    --------
    tuple : (x_values, y_values)
    """
    print("\n" + "="*80)
    print("MANUAL DATA INPUT")
    print("="*80)
    
    try:
        # Get function formula
        print("\nEnter function formula:")
        print("  Examples: 'x**2', '2*x + 3', 'x**3 - 2*x**2 + 3*x - 1', '2**x'")
        formula = input("  f(x) = ").strip()
        
        if not formula:
            print("Error: Function formula cannot be empty!")
            return None, None
        
        # Get number of points
        n = int(input("\nEnter number of data points: "))
        if n < 2:
            print("Error: Need at least 2 data points!")
            return None, None
        
        x_values = []
        y_values = []
        
        print(f"\nEnter {n} x values:")
        for i in range(n):
            x = float(input(f"  x[{i+1}]: "))
            x_values.append(x)
        
        # Calculate y values using the formula
        print("\nCalculating f(x) values...")
        for x in x_values:
            try:
                # Safely evaluate the function
                y = eval(formula, {"__builtins__": {}}, {"x": x, "__builtins__": __builtins__})
                y_values.append(float(y))
            except Exception as e:
                print(f"\nError evaluating f({x}) = {formula}")
                print(f"Error: {e}")
                return None, None
        
        # Display calculated values
        print("\nCalculated values:")
        for x, y in zip(x_values, y_values):
            print(f"  f({x}) = {y}")
        
        # Validate data
        validate_data(x_values, y_values)
        
        # Check spacing
        is_equal, h = check_equal_spacing(x_values)
        if is_equal:
            print(f"\n  Data is equally spaced with h = {h}")
        else:
            print("\n  Warning: Data is not equally spaced!")
            print("  Finite differences work best with equal spacing.")
        
        return x_values, y_values
        
    except ValueError as e:
        print(f"\nError: {e}")
        return None, None
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        return None, None


def manual_forward_differences():
    """Manual input for forward differences."""
    x_values, y_values = get_manual_input()
    
    if x_values is None or y_values is None:
        return
    
    # Display input data
    display_data_table(x_values, y_values, "INPUT DATA")
    
    # Calculate and display forward differences
    result = forward_difference_table(x_values, y_values)
    display_forward_difference_table(result)


def manual_backward_differences():
    """Manual input for backward differences."""
    x_values, y_values = get_manual_input()
    
    if x_values is None or y_values is None:
        return
    
    # Display input data
    display_data_table(x_values, y_values, "INPUT DATA")
    
    # Calculate and display backward differences
    result = backward_difference_table(x_values, y_values)
    display_backward_difference_table(result)


def manual_comparison():
    """Manual input for comparing forward and backward differences."""
    x_values, y_values = get_manual_input()
    
    if x_values is None or y_values is None:
        return
    
    # Display input data
    display_data_table(x_values, y_values, "INPUT DATA")
    
    # Calculate both forward and backward differences
    forward_result = forward_difference_table(x_values, y_values)
    backward_result = backward_difference_table(x_values, y_values)
    
    # Display comparison
    display_comparison(forward_result, backward_result)


def main():
    """Main program loop."""
    print_header()
    
    while True:
        print_menu()
        
        try:
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '0':
                print("Thank you for using Finite Differences Calculator!")
                sys.exit(0)
            
            elif choice == '1':
                manual_forward_differences()
            
            elif choice == '2':
                manual_backward_differences()
            
            elif choice == '3':
                manual_comparison()
            
            elif choice == '4':
                examples.example5_polynomial()
            
            elif choice == '5':
                examples.example6_exponential()
            
            elif choice == '6':
                examples.run_all_examples()
            
            else:
                print("\nInvalid choice! Please enter a number from 0 to 6.")
            
            if choice != '6' and choice != '0':
                input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\n" + "="*80)
            print("Program interrupted by user.")
            print("="*80 + "\n")
            sys.exit(0)
        
        except Exception as e:
            print(f"\nError: {e}")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
