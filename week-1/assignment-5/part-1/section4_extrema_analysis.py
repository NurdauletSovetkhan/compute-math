"""
Section 4: Analysis of tabulated functions
- 4.1 Maxima and Minima of a tabulated function
- 4.2 First derivative test for Maxima and Minima
- 4.3 Second derivative test for Maxima and Minima
"""

import sys
import os

# Import needed functions from other sections
sys.path.append(os.path.dirname(__file__))
from section2_equally_spaced import central_difference
from section3_unequally_spaced import unequally_spaced_central

def find_extrema(x_values, f_values, h=None, is_equally_spaced=True):
    """
    4.1: Find local maxima and minima in tabulated function data
    
    Parameters:
    - x_values: list of x values
    - f_values: list of function values
    - h: step size (for equally spaced data)
    - is_equally_spaced: whether data points are equally spaced
    
    Returns:
    - list of dictionaries containing extrema information
    """
    n = len(f_values)
    extrema = []
    
    # Check interior points for potential extrema
    for i in range(1, n - 1):
        # Check if it's a local maximum or minimum
        if f_values[i] > f_values[i-1] and f_values[i] > f_values[i+1]:
            extrema_type = "Maximum"
        elif f_values[i] < f_values[i-1] and f_values[i] < f_values[i+1]:
            extrema_type = "Minimum"
        else:
            continue
        
        # Calculate first derivative at this point
        if is_equally_spaced and h is not None:
            f_prime = central_difference(f_values, h, i, order=1)
            f_double_prime = central_difference(f_values, h, i, order=2)
        else:
            f_prime = unequally_spaced_central(x_values, f_values, i)
            # For second derivative, use finite difference approximation
            if i > 1 and i < n - 2:
                h_left = x_values[i] - x_values[i-1]
                h_right = x_values[i+1] - x_values[i]
                f_double_prime = (f_values[i+1] - 2*f_values[i] + f_values[i-1]) / ((h_left + h_right) / 2)**2
            else:
                f_double_prime = None
        
        extrema.append({
            'index': i,
            'x': x_values[i],
            'f(x)': f_values[i],
            'type': extrema_type,
            'f_prime': f_prime,
            'f_double_prime': f_double_prime
        })
    
    return extrema

def first_derivative_test(extrema):
    """
    4.2: Apply first derivative test to classify extrema
    
    The first derivative test states:
    - If f'(x) changes from positive to negative, x is a local maximum
    - If f'(x) changes from negative to positive, x is a local minimum
    
    Parameters:
    - extrema: list of extrema dictionaries from find_extrema
    
    Returns:
    - Updated extrema list with first derivative test results
    """
    for ext in extrema:
        f_prime = ext['f_prime']
        
        # Classification based on first derivative
        if abs(f_prime) < 1e-6:  # Close to zero
            if ext['type'] == "Maximum":
                ext['first_derivative_test'] = "Critical point (f'≈0), likely Maximum"
            else:
                ext['first_derivative_test'] = "Critical point (f'≈0), likely Minimum"
        else:
            ext['first_derivative_test'] = f"f' = {f_prime:.6f} (not exactly zero, approximate extremum)"
    
    return extrema

def second_derivative_test(extrema):
    """
    4.3: Apply second derivative test to classify extrema
    
    The second derivative test states:
    - If f''(x) > 0 at a critical point, x is a local minimum (concave up)
    - If f''(x) < 0 at a critical point, x is a local maximum (concave down)
    - If f''(x) = 0, the test is inconclusive
    
    Parameters:
    - extrema: list of extrema dictionaries from find_extrema
    
    Returns:
    - Updated extrema list with second derivative test results
    """
    for ext in extrema:
        f_double_prime = ext['f_double_prime']
        
        if f_double_prime is None:
            ext['second_derivative_test'] = "Unable to compute (insufficient data)"
            ext['concavity'] = "Unknown"
        elif f_double_prime > 1e-6:
            ext['second_derivative_test'] = f"f'' = {f_double_prime:.6f} > 0 → Local Minimum"
            ext['concavity'] = "Concave up"
        elif f_double_prime < -1e-6:
            ext['second_derivative_test'] = f"f'' = {f_double_prime:.6f} < 0 → Local Maximum"
            ext['concavity'] = "Concave down"
        else:
            ext['second_derivative_test'] = f"f'' ≈ 0 → Test inconclusive"
            ext['concavity'] = "Inflection point"
    
    return extrema

def run_section4(x_values, f_values, h=None, is_equally_spaced=True):
    """
    Execute Section 4: Analysis of tabulated functions
    """
    print("\n" + "="*70)
    print("SECTION 4: ANALYSIS OF TABULATED FUNCTIONS")
    print("="*70)
    
    # 4.1: Find potential extrema
    extrema = find_extrema(x_values, f_values, h, is_equally_spaced)
    
    if not extrema:
        print("\nNo local maxima or minima found in the data.")
        return
    
    print(f"\n✓ Found {len(extrema)} potential extrema")
    
    # 4.2: Apply first derivative test
    extrema = first_derivative_test(extrema)
    
    # 4.3: Apply second derivative test
    extrema = second_derivative_test(extrema)
    
    # Display results
    print("\n" + "="*70)
    print("4.1 MAXIMA AND MINIMA OF TABULATED FUNCTION")
    print("="*70)
    
    for i, ext in enumerate(extrema, 1):
        print(f"\nExtremum #{i}:")
        print(f"  Location: x = {ext['x']:.6f} (index {ext['index']})")
        print(f"  Value: f(x) = {ext['f(x)']:.6f}")
        print(f"  Type: {ext['type']}")
    
    print("\n" + "="*70)
    print("4.2 FIRST DERIVATIVE TEST FOR MAXIMA AND MINIMA")
    print("="*70)
    print("\nTheory: At a local extremum, f'(x) = 0 (or very close to 0)")
    
    for i, ext in enumerate(extrema, 1):
        print(f"\nExtremum #{i} at x = {ext['x']:.6f}:")
        print(f"  {ext['first_derivative_test']}")
    
    print("\n" + "="*70)
    print("4.3 SECOND DERIVATIVE TEST FOR MAXIMA AND MINIMA")
    print("="*70)
    print("\nTheory:")
    print("  • If f''(x) > 0 → Local Minimum (concave up)")
    print("  • If f''(x) < 0 → Local Maximum (concave down)")
    print("  • If f''(x) = 0 → Test inconclusive")
    
    for i, ext in enumerate(extrema, 1):
        print(f"\nExtremum #{i} at x = {ext['x']:.6f}:")
        print(f"  {ext['second_derivative_test']}")
        print(f"  Concavity: {ext['concavity']}")
        
        # Verify consistency
        if ext['type'] == "Maximum" and ext['concavity'] == "Concave down":
            print(f"  ✓ Verification: Confirmed as Maximum")
        elif ext['type'] == "Minimum" and ext['concavity'] == "Concave up":
            print(f"  ✓ Verification: Confirmed as Minimum")
        elif ext['concavity'] != "Unknown" and ext['concavity'] != "Inflection point":
            print(f"  ⚠ Warning: Type mismatch - review data")
    
    print("\n" + "="*70)
    print("SUMMARY OF EXTREMA")
    print("="*70)
    
    maxima = [ext for ext in extrema if ext['type'] == "Maximum"]
    minima = [ext for ext in extrema if ext['type'] == "Minimum"]
    
    if maxima:
        print("\nLocal Maxima:")
        for ext in maxima:
            print(f"  x = {ext['x']:.6f}, f(x) = {ext['f(x)']:.6f}")
    
    if minima:
        print("\nLocal Minima:")
        for ext in minima:
            print(f"  x = {ext['x']:.6f}, f(x) = {ext['f(x)']:.6f}")
