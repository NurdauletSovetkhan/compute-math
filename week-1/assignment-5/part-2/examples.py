"""
Examples demonstrating the use of numerical integration methods
"""

import math
from methods.trapezoidal import trapezoidal_rule
from methods.simpson_one_third import simpson_one_third_rule
from methods.simpson_three_eighth import simpson_three_eighth_rule
from utils import compare_methods, calculate_error_metrics
from table import display_integration_result, display_comparison


def example_1_polynomial():
    """Example: Integrate x² from 0 to 1."""
    print("\n" + "="*80)
    print("EXAMPLE 1: ∫[0,1] x² dx")
    print("="*80)
    print("Exact value: 1/3 ≈ 0.333333")
    print()
    
    func = lambda x: x**2
    a, b = 0, 1
    exact = 1/3
    
    # Test with different methods
    print("\n--- Trapezoidal Rule (n=10) ---")
    result1 = trapezoidal_rule(func, a, b, 10)
    display_integration_result(result1)
    print(f"Error: {abs(result1['result'] - exact):.10e}")
    
    print("\n--- Simpson's 1/3 Rule (n=10) ---")
    result2 = simpson_one_third_rule(func, a, b, 10)
    display_integration_result(result2)
    print(f"Error: {abs(result2['result'] - exact):.10e}")
    
    print("\n--- Simpson's 3/8 Rule (n=9) ---")
    result3 = simpson_three_eighth_rule(func, a, b, 9)
    display_integration_result(result3)
    print(f"Error: {abs(result3['result'] - exact):.10e}")


def example_2_trigonometric():
    """Example: Integrate sin(x) from 0 to π."""
    print("\n" + "="*80)
    print("EXAMPLE 2: ∫[0,π] sin(x) dx")
    print("="*80)
    print("Exact value: 2.0")
    print()
    
    func = math.sin
    a, b = 0, math.pi
    exact = 2.0
    
    # Compare all methods
    results = compare_methods(func, a, b, exact)
    display_comparison(results)


def example_3_exponential():
    """Example: Integrate e^x from 0 to 1."""
    print("\n" + "="*80)
    print("EXAMPLE 3: ∫[0,1] e^x dx")
    print("="*80)
    print(f"Exact value: e - 1 ≈ {math.e - 1:.10f}")
    print()
    
    func = math.exp
    a, b = 0, 1
    exact = math.e - 1
    
    # Test with increasing n
    print("\nTesting with increasing number of intervals:")
    print("-" * 80)
    
    for n in [10, 50, 100]:
        result = simpson_one_third_rule(func, a, b, n)
        error = abs(result['result'] - exact)
        print(f"n = {n:3d}: Result = {result['result']:.10f}, Error = {error:.10e}")


def example_4_rational():
    """Example: Integrate 1/(1+x²) from 0 to 1."""
    print("\n" + "="*80)
    print("EXAMPLE 4: ∫[0,1] 1/(1+x²) dx")
    print("="*80)
    print(f"Exact value: π/4 ≈ {math.pi/4:.10f}")
    print()
    
    func = lambda x: 1 / (1 + x**2)
    a, b = 0, 1
    exact = math.pi / 4
    
    # Compare all methods
    results = compare_methods(func, a, b, exact)
    display_comparison(results)


def example_5_accuracy_comparison():
    """Example: Compare accuracy of methods for x³."""
    print("\n" + "="*80)
    print("EXAMPLE 5: Accuracy Comparison for ∫[0,2] x³ dx")
    print("="*80)
    print("Exact value: 4.0")
    print()
    
    func = lambda x: x**3
    a, b = 0, 2
    exact = 4.0
    
    print("\nAccuracy vs Number of Intervals:")
    print("-" * 80)
    print(f"{'n':<10} {'Trapezoidal':<20} {'Simpson 1/3':<20} {'Simpson 3/8':<20}")
    print("-" * 80)
    
    for n_base in [6, 12, 24, 48]:
        # n for trapezoidal
        n_trap = n_base
        result_trap = trapezoidal_rule(func, a, b, n_trap)
        error_trap = abs(result_trap['result'] - exact)
        
        # n for simpson 1/3 (must be even)
        n_simp13 = n_base if n_base % 2 == 0 else n_base + 1
        result_simp13 = simpson_one_third_rule(func, a, b, n_simp13)
        error_simp13 = abs(result_simp13['result'] - exact)
        
        # n for simpson 3/8 (must be divisible by 3)
        n_simp38 = n_base if n_base % 3 == 0 else n_base + (3 - n_base % 3)
        result_simp38 = simpson_three_eighth_rule(func, a, b, n_simp38)
        error_simp38 = abs(result_simp38['result'] - exact)
        
        print(f"{n_base:<10} {error_trap:<20.10e} {error_simp13:<20.10e} {error_simp38:<20.10e}")


def example_6_custom_function():
    """Example: User-defined complex function."""
    print("\n" + "="*80)
    print("EXAMPLE 6: ∫[0,1] (x² + sin(x)) dx")
    print("="*80)
    
    func = lambda x: x**2 + math.sin(x)
    a, b = 0, 1
    
    # Calculate exact value analytically: [x³/3 - cos(x)]₀¹
    # = (1/3 - cos(1)) - (0 - cos(0))
    # = 1/3 - cos(1) + 1
    exact = 1/3 - math.cos(1) + 1
    print(f"Exact value: {exact:.10f}")
    print()
    
    # Compare methods
    results = compare_methods(func, a, b, exact)
    display_comparison(results)


def example_7_convergence():
    """Example: Show convergence as n increases."""
    print("\n" + "="*80)
    print("EXAMPLE 7: Convergence Study for ∫[0,1] √x dx")
    print("="*80)
    print(f"Exact value: 2/3 ≈ {2/3:.10f}")
    print()
    
    func = math.sqrt
    a, b = 0, 1
    exact = 2/3
    
    print("\nConvergence of Simpson's 1/3 Rule:")
    print("-" * 80)
    print(f"{'n':<10} {'Result':<20} {'Error':<20} {'Error Ratio':<20}")
    print("-" * 80)
    
    prev_error = None
    for n in [2, 4, 8, 16, 32, 64]:
        result = simpson_one_third_rule(func, a, b, n)
        error = abs(result['result'] - exact)
        
        if prev_error is not None:
            ratio = prev_error / error
            print(f"{n:<10} {result['result']:<20.10f} {error:<20.10e} {ratio:<20.2f}")
        else:
            print(f"{n:<10} {result['result']:<20.10f} {error:<20.10e} {'N/A':<20}")
        
        prev_error = error


def main():
    """Run all examples."""
    print("\n" + "="*80)
    print(" "*20 + "NUMERICAL INTEGRATION EXAMPLES")
    print(" "*25 + "Assignment 5 - Part 2")
    print("="*80)
    
    examples = [
        ("Polynomial Integration", example_1_polynomial),
        ("Trigonometric Integration", example_2_trigonometric),
        ("Exponential Integration", example_3_exponential),
        ("Rational Function Integration", example_4_rational),
        ("Accuracy Comparison", example_5_accuracy_comparison),
        ("Custom Function", example_6_custom_function),
        ("Convergence Study", example_7_convergence),
    ]
    
    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    print(f"  8. Run all examples")
    print(f"  0. Exit")
    
    try:
        choice = int(input("\nSelect example (0-8): "))
        
        if choice == 0:
            print("Goodbye!")
            return
        elif choice == 8:
            for name, func in examples:
                func()
                input("\nPress Enter to continue to next example...")
        elif 1 <= choice <= len(examples):
            examples[choice - 1][1]()
        else:
            print("Invalid choice.")
    
    except ValueError:
        print("Invalid input.")
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")


if __name__ == "__main__":
    main()
