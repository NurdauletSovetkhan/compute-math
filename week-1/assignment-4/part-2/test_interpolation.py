"""
Test script to demonstrate all interpolation methods
"""

from lagrange import lagrange_interpolation
from newton_forward import newton_forward_interpolation
from newton_backward import newton_backward_interpolation
from utils import format_polynomial_pretty, check_equal_spacing
from table import display_input_data, display_interpolation_result, display_comparison_results


def test_population_data():
    """Test with population data from the assignment."""
    print("\n" + "="*80)
    print("TEST 1: POPULATION DATA (2010-2025)")
    print("="*80)
    
    x_values = [2010, 2015, 2020, 2025]
    y_values = [16.5, 17.5, 18.7, 20.0]
    x_target = 2018
    
    display_input_data(x_values, y_values)
    
    print(f"\nTask: Estimate population in year {x_target}\n")
    
    # Test all methods
    results = []
    
    # Lagrange
    result = lagrange_interpolation(x_values, y_values, x_target)
    results.append(result)
    print("✓ Lagrange: y =", result['y_estimated'])
    
    # Newton Forward
    result = newton_forward_interpolation(x_values, y_values, x_target)
    results.append(result)
    print("✓ Newton Forward: y =", result['y_estimated'])
    
    # Newton Backward
    result = newton_backward_interpolation(x_values, y_values, x_target)
    results.append(result)
    print("✓ Newton Backward: y =", result['y_estimated'])
    
    # Display detailed results
    display_comparison_results(results)
    
    # Display polynomial from Lagrange
    print("\nInterpolating Polynomial (Lagrange):")
    coeffs = results[0]['polynomial_coefficients']
    print("P(x) =", format_polynomial_pretty(coeffs, precision=6))
    
    return results


def test_polynomial_data():
    """Test with polynomial data."""
    print("\n" + "="*80)
    print("TEST 2: POLYNOMIAL DATA f(x) = x³ - 2x² + 3x - 1")
    print("="*80)
    
    x_values = [0, 1, 2, 3, 4]
    y_values = [x**3 - 2*x**2 + 3*x - 1 for x in x_values]
    x_target = 2.5
    
    display_input_data(x_values, y_values)
    
    print(f"\nTask: Estimate f({x_target})")
    true_value = x_target**3 - 2*x_target**2 + 3*x_target - 1
    print(f"True value: f({x_target}) = {true_value}\n")
    
    # Test all methods
    results = []
    
    # Lagrange
    result = lagrange_interpolation(x_values, y_values, x_target)
    results.append(result)
    error = abs(result['y_estimated'] - true_value)
    print(f"✓ Lagrange: y = {result['y_estimated']}, error = {error:.2e}")
    
    # Newton Forward
    result = newton_forward_interpolation(x_values, y_values, x_target)
    results.append(result)
    error = abs(result['y_estimated'] - true_value)
    print(f"✓ Newton Forward: y = {result['y_estimated']}, error = {error:.2e}")
    
    # Newton Backward
    result = newton_backward_interpolation(x_values, y_values, x_target)
    results.append(result)
    error = abs(result['y_estimated'] - true_value)
    print(f"✓ Newton Backward: y = {result['y_estimated']}, error = {error:.2e}")
    
    # Display comparison
    display_comparison_results(results)
    
    # Display polynomial (should recover original)
    print("\nRecovered Polynomial (Lagrange):")
    coeffs = results[0]['polynomial_coefficients']
    print("P(x) =", format_polynomial_pretty(coeffs, precision=6))
    print("\nExpected: P(x) = x³ - 2x² + 3x - 1")
    
    return results


def test_unequal_spacing():
    """Test with unequally spaced data."""
    print("\n" + "="*80)
    print("TEST 3: UNEQUALLY SPACED DATA")
    print("="*80)
    
    x_values = [0, 1, 3, 7, 10]
    y_values = [1, 3, 7, 13, 21]
    x_target = 5
    
    display_input_data(x_values, y_values)
    
    # Check spacing
    is_equal, h = check_equal_spacing(x_values)
    print(f"\nData spacing: {'Equal (h=' + str(h) + ')' if is_equal else 'Unequal'}")
    
    print(f"\nTask: Estimate y at x = {x_target}\n")
    
    # Only Lagrange should work
    result = lagrange_interpolation(x_values, y_values, x_target)
    print(f"✓ Lagrange: y = {result['y_estimated']}")
    
    display_interpolation_result(result)
    
    # Try Newton methods (should work since they convert internally)
    try:
        result_fwd = newton_forward_interpolation(x_values, y_values, x_target)
        print(f"\n⚠ Newton Forward worked (shouldn't for unequal spacing): y = {result_fwd['y_estimated']}")
    except ValueError as e:
        print(f"\n✓ Newton Forward correctly rejected unequal spacing: {e}")
    
    try:
        result_bwd = newton_backward_interpolation(x_values, y_values, x_target)
        print(f"\n⚠ Newton Backward worked (shouldn't for unequal spacing): y = {result_bwd['y_estimated']}")
    except ValueError as e:
        print(f"✓ Newton Backward correctly rejected unequal spacing: {e}")
    
    return result


def test_edge_cases():
    """Test edge cases."""
    print("\n" + "="*80)
    print("TEST 4: EDGE CASES")
    print("="*80)
    
    # Test 1: Target at data point
    print("\n--- Case 1: Target at existing data point ---")
    x_values = [0, 1, 2, 3]
    y_values = [1, 2, 4, 8]
    x_target = 2
    
    result = lagrange_interpolation(x_values, y_values, x_target)
    print(f"Target x={x_target} (existing point)")
    print(f"Expected: y = {y_values[2]}")
    print(f"Interpolated: y = {result['y_estimated']}")
    print(f"Error: {abs(result['y_estimated'] - y_values[2]):.2e}")
    
    # Test 2: Extrapolation
    print("\n--- Case 2: Extrapolation (beyond data range) ---")
    x_target = 5
    result = lagrange_interpolation(x_values, y_values, x_target)
    print(f"Target x={x_target} (outside range [0, 3])")
    print(f"Extrapolated: y = {result['y_estimated']}")
    print("Note: Extrapolation is less accurate than interpolation")
    
    # Test 3: Linear data
    print("\n--- Case 3: Linear data ---")
    x_values = [0, 1, 2, 3, 4]
    y_values = [5, 8, 11, 14, 17]  # y = 3x + 5
    x_target = 2.5
    
    result = lagrange_interpolation(x_values, y_values, x_target)
    true_value = 3 * x_target + 5
    print(f"Linear function: y = 3x + 5")
    print(f"Target: x = {x_target}")
    print(f"Expected: y = {true_value}")
    print(f"Interpolated: y = {result['y_estimated']}")
    print(f"Error: {abs(result['y_estimated'] - true_value):.2e}")
    
    print("\nPolynomial representation:")
    coeffs = result['polynomial_coefficients']
    print("P(x) =", format_polynomial_pretty(coeffs, precision=6))


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print(" "*15 + "INTERPOLATION METHODS - TEST SUITE")
    print(" "*20 + "Assignment 4 - Part 2")
    print("="*80)
    
    # Run tests
    test_population_data()
    input("\nPress Enter to continue to next test...")
    
    test_polynomial_data()
    input("\nPress Enter to continue to next test...")
    
    test_unequal_spacing()
    input("\nPress Enter to continue to next test...")
    
    test_edge_cases()
    
    print("\n" + "="*80)
    print("ALL TESTS COMPLETED")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
