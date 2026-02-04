"""
Test the comparison feature from main.py
"""

import math
import sys

# Simulate the comparison functionality
from methods.trapezoidal import trapezoidal_rule
from methods.simpson_one_third import simpson_one_third_rule
from methods.simpson_three_eighth import simpson_three_eighth_rule
from utils import compare_methods

# Test function: sin(x) from 0 to π
func = math.sin
a = 0
b = math.pi
exact_value = 2.0

print("\n" + "="*80)
print("TESTING COMPARISON FEATURE")
print("="*80)
print(f"\nFunction: sin(x)")
print(f"Interval: [{a}, {b}]")
print(f"Exact value: {exact_value}")

# Get results
results = compare_methods(func, a, b, exact_value)

# Display detailed results for each method
print("\n" + "="*80)
print("DETAILED RESULTS FOR EACH METHOD")
print("="*80)

method_order = [('trapezoidal', 'TRAPEZOIDAL RULE', 'n ≥ 1'),
                ('simpson_1/3', "SIMPSON'S 1/3 RULE", 'n must be even'),
                ('simpson_3/8', "SIMPSON'S 3/8 RULE", 'n must be divisible by 3')]

for i, (method_key, method_name, constraint) in enumerate(method_order, 1):
    if method_key in results:
        result = results[method_key]
        if 'error' in result and isinstance(result['error'], str):
            print(f"\n{i}. {method_name} - ERROR")
            print(f"   {result['error']}")
        else:
            n = result.get('n', 'N/A')
            h = result.get('h', 0)
            value = result.get('result', 0)
            
            print(f"\n{i}. {method_name} (n={n}, {constraint}):")
            print(f"   h = {h:.10f}")
            print(f"   Result = {value:.10f}")
            
            if exact_value is not None:
                error = abs(value - exact_value)
                print(f"   Error = {error:.10e}")

# Display comparison table
from table import display_comparison
display_comparison(results)

print("\n✓ Comparison feature working correctly!")
