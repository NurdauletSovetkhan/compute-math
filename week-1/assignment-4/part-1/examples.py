"""
Example tasks for finite differences.
Based on the task description images.
"""

from methods.forward_difference import forward_difference_table
from methods.backward_difference import backward_difference_table
from table import display_forward_difference_table, display_backward_difference_table, display_comparison


def example5_polynomial():
    """
    Example 1: Polynomial f(x) = x³ - 2x² + 3x - 1
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: Polynomial f(x) = x³ - 2x² + 3x - 1")
    print("="*80)
    
    x_values = list(range(0, 6))
    y_values = [x**3 - 2*x**2 + 3*x - 1 for x in x_values]
    
    print(f"\nFunction: f(x) = x³ - 2x² + 3x - 1")
    print(f"Data points:")
    for x, y in zip(x_values, y_values):
        print(f"  f({x}) = {y}")
    
    print("\n--- Forward Differences ---")
    forward_result = forward_difference_table(x_values, y_values)
    display_forward_difference_table(forward_result)
    
    return forward_result


def example6_exponential():
    """
    Example 2: Exponential function f(x) = 2^x
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: Exponential Function f(x) = 2^x")
    print("="*80)
    
    x_values = [0, 1, 2, 3, 4, 5]
    y_values = [2**x for x in x_values]
    
    print(f"\nFunction: f(x) = 2^x")
    print(f"Data points:")
    for x, y in zip(x_values, y_values):
        print(f"  f({x}) = {y}")
    
    print("\n--- Forward Differences ---")
    forward_result = forward_difference_table(x_values, y_values)
    display_forward_difference_table(forward_result)
    
    print("\nNote: For exponential functions, differences don't become constant.")
    
    return forward_result


def run_all_examples():
    """
    Run all examples.
    """
    examples = [
        example5_polynomial,
        example6_exponential
    ]
    
    for example in examples:
        try:
            example()
            input("\nPress Enter to continue to next example...")
        except Exception as e:
            print(f"\nError in example: {e}")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    run_all_examples()
