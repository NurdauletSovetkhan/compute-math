"""
Examples for testing Numerical Differentiation
Quick test cases for all sections
"""

import math
from section2_equally_spaced import run_section2
from section3_unequally_spaced import run_section3
from section4_extrema_analysis import run_section4

def example1_equally_spaced():
    """
    Example 1: Equally spaced points with quadratic function
    Function: f(x) = x²
    Expected: f'(x) = 2x, f''(x) = 2
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: EQUALLY SPACED - QUADRATIC FUNCTION f(x) = x²")
    print("="*70)
    
    x_values = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    f_values = [x**2 for x in x_values]
    h = 0.5
    
    print(f"\nData points: {len(x_values)}")
    print(f"Range: [{x_values[0]}, {x_values[-1]}]")
    print(f"Step size h = {h}")
    
    run_section2(x_values, f_values, h)
    run_section4(x_values, f_values, h, is_equally_spaced=True)

def example2_equally_spaced_sine():
    """
    Example 2: Equally spaced points with sine function
    Function: f(x) = sin(x)
    Expected: f'(x) = cos(x), f''(x) = -sin(x)
    Has maximum at x ≈ π/2
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: EQUALLY SPACED - SINE FUNCTION f(x) = sin(x)")
    print("="*70)
    
    x_values = [i * 0.3 for i in range(11)]  # 0 to 3.0 with h=0.3
    f_values = [math.sin(x) for x in x_values]
    h = 0.3
    
    print(f"\nData points: {len(x_values)}")
    print(f"Range: [{x_values[0]:.2f}, {x_values[-1]:.2f}]")
    print(f"Step size h = {h}")
    
    run_section2(x_values, f_values, h)
    run_section4(x_values, f_values, h, is_equally_spaced=True)

def example3_unequally_spaced():
    """
    Example 3: Unequally spaced points with exponential function
    Function: f(x) = e^x
    Expected: f'(x) = e^x
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: UNEQUALLY SPACED - EXPONENTIAL FUNCTION f(x) = e^x")
    print("="*70)
    
    x_values = [0, 0.2, 0.5, 1.0, 1.7, 2.1, 2.8]
    f_values = [math.exp(x) for x in x_values]
    
    print(f"\nData points: {len(x_values)}")
    print(f"Range: [{x_values[0]}, {x_values[-1]}]")
    print("Spacing: Unequal")
    
    run_section3(x_values, f_values)
    run_section4(x_values, f_values, h=None, is_equally_spaced=False)

def example4_parabola_with_extremum():
    """
    Example 4: Parabola with clear extremum
    Function: f(x) = -(x-2)² + 4
    Has maximum at x = 2, f(2) = 4
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: PARABOLA WITH EXTREMUM f(x) = -(x-2)² + 4")
    print("="*70)
    print("Expected: Maximum at x = 2, f(2) = 4")
    
    x_values = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    f_values = [-(x-2)**2 + 4 for x in x_values]
    h = 0.5
    
    print(f"\nData points: {len(x_values)}")
    print(f"Range: [{x_values[0]}, {x_values[-1]}]")
    print(f"Step size h = {h}")
    
    run_section2(x_values, f_values, h)
    run_section4(x_values, f_values, h, is_equally_spaced=True)

def example5_cubic_multiple_extrema():
    """
    Example 5: Cubic function with multiple extrema
    Function: f(x) = x³ - 3x² + 2
    Has max at x ≈ 0, min at x ≈ 2
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: CUBIC WITH MULTIPLE EXTREMA f(x) = x³ - 3x² + 2")
    print("="*70)
    print("Expected: Maximum near x = 0, Minimum near x = 2")
    
    x_values = [-1, -0.5, 0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    f_values = [x**3 - 3*x**2 + 2 for x in x_values]
    h = 0.5
    
    print(f"\nData points: {len(x_values)}")
    print(f"Range: [{x_values[0]}, {x_values[-1]}]")
    print(f"Step size h = {h}")
    
    run_section2(x_values, f_values, h)
    run_section4(x_values, f_values, h, is_equally_spaced=True)

def example6_unequally_with_extremum():
    """
    Example 6: Unequally spaced with extremum
    Function: f(x) = cos(x)
    Has maximum at x = 0
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: UNEQUALLY SPACED WITH EXTREMUM f(x) = cos(x)")
    print("="*70)
    
    x_values = [0, 0.3, 0.8, 1.2, 1.8, 2.4, 3.0]
    f_values = [math.cos(x) for x in x_values]
    
    print(f"\nData points: {len(x_values)}")
    print(f"Range: [{x_values[0]}, {x_values[-1]}]")
    print("Spacing: Unequal")
    
    run_section3(x_values, f_values)
    run_section4(x_values, f_values, h=None, is_equally_spaced=False)

def run_all_examples():
    """Run all examples sequentially"""
    examples = [
        ("Example 1: Equally Spaced Quadratic", example1_equally_spaced),
        ("Example 2: Equally Spaced Sine", example2_equally_spaced_sine),
        ("Example 3: Unequally Spaced Exponential", example3_unequally_spaced),
        ("Example 4: Parabola with Extremum", example4_parabola_with_extremum),
        ("Example 5: Cubic Multiple Extrema", example5_cubic_multiple_extrema),
        ("Example 6: Unequally with Extremum", example6_unequally_with_extremum),
    ]
    
    print("\n" + "="*70)
    print("RUNNING ALL EXAMPLES")
    print("="*70)
    
    for i, (name, func) in enumerate(examples, 1):
        print(f"\n\n{'='*70}")
        print(f"Running {i}/{len(examples)}: {name}")
        print('='*70)
        
        try:
            func()
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")
        
        if i < len(examples):
            input("\nPress Enter to continue to next example...")
    
    print("\n" + "="*70)
    print("ALL EXAMPLES COMPLETED")
    print("="*70)

def main():
    """Main menu for examples"""
    while True:
        print("\n" + "="*70)
        print("NUMERICAL DIFFERENTIATION - EXAMPLES MENU")
        print("="*70)
        print("\n1. Example 1: Equally Spaced Quadratic (x²)")
        print("2. Example 2: Equally Spaced Sine (sin(x))")
        print("3. Example 3: Unequally Spaced Exponential (e^x)")
        print("4. Example 4: Parabola with Extremum (-(x-2)² + 4)")
        print("5. Example 5: Cubic Multiple Extrema (x³ - 3x² + 2)")
        print("6. Example 6: Unequally Spaced with Extremum (cos(x))")
        print("7. Run All Examples")
        print("8. Exit")
        print("="*70)
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == '1':
            example1_equally_spaced()
        elif choice == '2':
            example2_equally_spaced_sine()
        elif choice == '3':
            example3_unequally_spaced()
        elif choice == '4':
            example4_parabola_with_extremum()
        elif choice == '5':
            example5_cubic_multiple_extrema()
        elif choice == '6':
            example6_unequally_with_extremum()
        elif choice == '7':
            run_all_examples()
        elif choice == '8':
            print("\n" + "="*70)
            print("Thank you!")
            print("="*70)
            break
        else:
            print("\n❌ Invalid choice. Please enter 1-8.")

if __name__ == "__main__":
    main()
