# Assignment 5 - Part 2: Numerical Integration

Implementation of three numerical integration methods:
- **Trapezoidal Rule**
- **Simpson's 1/3 Rule**
- **Simpson's 3/8 Rule**

## 📁 Project Structure

```
assignment-5/part-2/
├── main.py                          # Main program with interactive menu
├── utils.py                         # Utility functions for validation and comparison
├── table.py                         # Display utilities for formatted output
├── README.md                        # This file
└── methods/
    ├── __init__.py                  # Module initialization
    ├── trapezoidal.py              # Trapezoidal rule implementation
    ├── simpson_one_third.py        # Simpson's 1/3 rule implementation
    └── simpson_three_eighth.py     # Simpson's 3/8 rule implementation
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Optional: `tabulate` library for better table formatting

```bash
pip install tabulate
```

### Running the Program

```bash
python main.py
```

## 📊 Methods Overview

### 1. Trapezoidal Rule

Approximates the integral by dividing the area under the curve into trapezoids.

**Formula:**
```
∫[a,b] f(x)dx ≈ h/2 * [f(a) + 2*Σf(xᵢ) + f(b)]
```

**Requirements:**
- n ≥ 1 (number of intervals)

**Error:** O(h²) or O(1/n²)

**Best for:** Quick approximations, linear functions

### 2. Simpson's 1/3 Rule

Uses quadratic polynomials to approximate the curve. More accurate than trapezoidal rule.

**Formula:**
```
∫[a,b] f(x)dx ≈ h/3 * [f(a) + 4*Σf(x_odd) + 2*Σf(x_even) + f(b)]
```

**Requirements:**
- n must be even
- n ≥ 2

**Error:** O(h⁴) or O(1/n⁴)

**Best for:** Smooth functions, higher accuracy needs

### 3. Simpson's 3/8 Rule

Uses cubic polynomials to approximate the curve. Similar accuracy to 1/3 rule but with different interval requirements.

**Formula:**
```
∫[a,b] f(x)dx ≈ 3h/8 * [f(a) + 3*Σf(x_i) + 3*Σf(x_j) + 2*Σf(x_k) + f(b)]
```

**Requirements:**
- n must be divisible by 3
- n ≥ 3

**Error:** O(h⁴) or O(1/n⁴)

**Best for:** Smooth functions when n is divisible by 3

## 💡 Features

### Interactive Menu
1. **Individual Method Testing**: Test each method separately with custom functions
2. **Method Comparison**: Compare all three methods on the same function
3. **Predefined Test Examples**: Test with common functions with known exact values
4. **Method Information**: View detailed information about each method
5. **Error Analysis**: Calculate and display various error metrics

### Test Examples Included
- ∫[0,1] x² dx = 1/3
- ∫[0,2] x³ dx = 4
- ∫[0,π] sin(x) dx = 2
- ∫[0,π/2] cos(x) dx = 1
- ∫[0,1] e^x dx = e - 1
- ∫[0,4] √x dx = 16/3
- ∫[1,2] 1/x dx = ln(2)
- ∫[0,1] 1/(1+x²) dx = π/4

## 📝 Usage Examples

### Example 1: Using Trapezoidal Rule

```python
from methods.trapezoidal import trapezoidal_rule
import math

# Integrate sin(x) from 0 to π
result = trapezoidal_rule(math.sin, 0, math.pi, 100)
print(f"Result: {result['result']:.10f}")
print(f"Exact: 2.0000000000")
```

### Example 2: Using Simpson's 1/3 Rule

```python
from methods.simpson_one_third import simpson_one_third_rule

# Integrate x² from 0 to 1
result = simpson_one_third_rule(lambda x: x**2, 0, 1, 10)
print(f"Result: {result['result']:.10f}")
print(f"Exact: {1/3:.10f}")
```

### Example 3: Comparing All Methods

```python
from utils import compare_methods
import math

# Compare methods for e^x from 0 to 1
results = compare_methods(math.exp, 0, 1, exact_value=math.e - 1)
for method, result in results.items():
    if method != 'exact_value':
        print(f"{method}: {result['result']:.10f}")
```

## 🧪 Testing Individual Methods

Each method file can be run standalone to see examples:

```bash
python methods/trapezoidal.py
python methods/simpson_one_third.py
python methods/simpson_three_eighth.py
```

## 📐 Mathematical Background

### Trapezoidal Rule
The trapezoidal rule works by approximating the region under the graph of f(x) as a trapezoid and calculating its area. The more intervals used, the better the approximation.

### Simpson's Rules
Simpson's rules fit parabolas (1/3 rule) or cubic polynomials (3/8 rule) through groups of points. These higher-order approximations generally provide better accuracy than the trapezoidal rule, especially for smooth functions.

### Error Estimates
- **Trapezoidal**: |E| ≤ (b-a)³/(12n²) * max|f''(x)|
- **Simpson's 1/3**: |E| ≤ (b-a)⁵/(180n⁴) * max|f⁽⁴⁾(x)|
- **Simpson's 3/8**: |E| ≤ (b-a)⁵/(80n⁴) * max|f⁽⁴⁾(x)|

## 🎯 Key Functions

### `trapezoidal_rule(func, a, b, n)`
Calculates integral using trapezoidal rule.

**Parameters:**
- `func`: Function to integrate
- `a`: Lower bound
- `b`: Upper bound
- `n`: Number of intervals

**Returns:** Dictionary with result and computation details

### `simpson_one_third_rule(func, a, b, n)`
Calculates integral using Simpson's 1/3 rule.

**Parameters:**
- `func`: Function to integrate
- `a`: Lower bound
- `b`: Upper bound
- `n`: Number of intervals (must be even)

**Returns:** Dictionary with result and computation details

### `simpson_three_eighth_rule(func, a, b, n)`
Calculates integral using Simpson's 3/8 rule.

**Parameters:**
- `func`: Function to integrate
- `a`: Lower bound
- `b`: Upper bound
- `n`: Number of intervals (must be divisible by 3)

**Returns:** Dictionary with result and computation details

## 📊 Output Format

The program provides detailed output including:
- Integral value (result)
- Integration interval [a, b]
- Number of intervals (n)
- Step size (h)
- Number of function evaluations
- Error metrics (if exact value is known)
- Computation points (optional)

## 🔍 Error Analysis

When an exact value is provided, the program calculates:
- **Absolute Error**: |approximate - exact|
- **Relative Error**: |approximate - exact| / |exact|
- **Percentage Error**: Relative error × 100%
- **Significant Digits**: -log₁₀(relative error)

## 🎓 Educational Value

This implementation is designed for educational purposes and includes:
- Clear documentation and comments
- Step-by-step computation details
- Visual formatting of results
- Comparison capabilities
- Error analysis tools

## 👨‍💻 Author

Assignment 5 - Part 2  
Computational Mathematics Course

## 📄 License

This is an educational project for academic purposes.

## 🙏 Acknowledgments

Based on standard numerical integration algorithms as described in computational mathematics textbooks.
