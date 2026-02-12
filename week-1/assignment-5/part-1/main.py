"""
NUMERICAL DIFFERENTIATION - Assignment 5
Main program that integrates all sections:
- Section 2: Derivatives using equally spaced values
- Section 3: Derivatives using unequally spaced values  
- Section 4: Analysis of tabulated functions (extrema)
"""

import math
import sys
import os

# Import section modules
from section2_equally_spaced import run_section2
from section3_unequally_spaced import run_section3
from section4_extrema_analysis import run_section4

def display_menu():
    """Display main menu"""
    print("\n" + "="*70)
    print("NUMERICAL DIFFERENTIATION - MAIN MENU")
    print("="*70)
    print("\n1. Run All Sections (Complete Analysis)")
    print("2. Section 2: Equally Spaced Differentiation")
    print("3. Section 3: Unequally Spaced Differentiation")
    print("4. Section 4: Extrema Analysis")
    print("5. Exit")
    print("\n" + "="*70)

def get_input_data():
    """Get input data from user"""
    print("\n" + "="*70)
    print("DATA INPUT")
    print("="*70)
    
    # Input x values
    x_input = input("\nEnter x values separated by spaces: ")
    x_values = [float(val) for val in x_input.split()]
    n = len(x_values)
    
    if n < 3:
        print("Error: Need at least 3 data points for numerical differentiation")
        return None, None, None
    
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
            return None, None, None
    else:
        # Compute f(x) values from function
        f_values = []
        for x in x_values:
            tool["x"] = x
            try:
                f_values.append(eval(f, {"__builtins__": None}, tool))
            except Exception as e:
                print(f"Error evaluating function at x={x}: {e}")
                return None, None, None
    
    # Check if spacing is equal
    h = x_values[1] - x_values[0]
    is_equally_spaced = True
    
    for i in range(n - 1):
        current_spacing = x_values[i + 1] - x_values[i]
        if not math.isclose(h, current_spacing, rel_tol=1e-7):
            is_equally_spaced = False
            break
    
    return x_values, f_values, is_equally_spaced

def display_data_table(x_values, f_values):
    """Display input data in table format"""
    print("\n" + "="*70)
    print("DATA TABLE")
    print("="*70)
    print(f"{'i':<5} {'x':<15} {'f(x)':<15}")
    print("-" * 40)
    for i in range(len(x_values)):
        print(f"{i:<5} {x_values[i]:<15.6f} {f_values[i]:<15.6f}")
    print("="*70)

def run_all_sections(x_values, f_values, is_equally_spaced):
    """Run complete analysis (all sections)"""
    n = len(x_values)
    h = x_values[1] - x_values[0] if is_equally_spaced else None
    
    print("\n" + "="*70)
    print("COMPLETE NUMERICAL DIFFERENTIATION ANALYSIS")
    print("="*70)
    
    if is_equally_spaced:
        print(f"\n✓ Data points are EQUALLY SPACED with h = {h:.6f}")
        run_section2(x_values, f_values, h)
    else:
        print("\n✓ Data points are UNEQUALLY SPACED")
        run_section3(x_values, f_values)
    
    # Always run extrema analysis
    run_section4(x_values, f_values, h if is_equally_spaced else None, is_equally_spaced)

def main():
    """Main program loop"""
    print("="*70)
    print("NUMERICAL DIFFERENTIATION CALCULATOR")
    print("Based on Textbook Sections 2, 3, and 4")
    print("="*70)
    
    x_values = None
    f_values = None
    is_equally_spaced = None
    
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '5':
            print("\n" + "="*70)
            print("Thank you for using Numerical Differentiation Calculator!")
            print("="*70)
            break
        
        # Get data if not already loaded or if user wants to input new data
        if x_values is None or choice == '0':  # Hidden option to reload data
            result = get_input_data()
            if result[0] is None:
                continue
            x_values, f_values, is_equally_spaced = result
            display_data_table(x_values, f_values)
        
        # Calculate h for equally spaced data
        h = x_values[1] - x_values[0] if is_equally_spaced else None
        
        # Execute selected section
        if choice == '1':
            run_all_sections(x_values, f_values, is_equally_spaced)
        
        elif choice == '2':
            if not is_equally_spaced:
                print("\n⚠ Warning: Data is not equally spaced!")
                proceed = input("Do you want to proceed anyway? (y/n): ")
                if proceed.lower() != 'y':
                    continue
                # Calculate average spacing
                h = sum(x_values[i+1] - x_values[i] for i in range(len(x_values)-1)) / (len(x_values)-1)
                print(f"Using average spacing h = {h:.6f}")
            
            run_section2(x_values, f_values, h)
        
        elif choice == '3':
            if is_equally_spaced:
                print("\n✓ Note: Data is equally spaced, but Section 3 methods will still work.")
            run_section3(x_values, f_values)
        
        elif choice == '4':
            run_section4(x_values, f_values, h if is_equally_spaced else None, is_equally_spaced)
        
        else:
            print("\n❌ Invalid choice. Please enter 1-5.")
            continue
        
        print("\n" + "="*70)
        print("SECTION COMPLETE")
        print("="*70)
        
        # Ask if user wants to continue
        cont = input("\nPress Enter to return to menu, or 'r' to reload data, or 'q' to quit: ").strip().lower()
        if cont == 'q':
            print("\n" + "="*70)
            print("Thank you for using Numerical Differentiation Calculator!")
            print("="*70)
            break
        elif cont == 'r':
            x_values = None  # Force data reload on next iteration

if __name__ == "__main__":
    main()
