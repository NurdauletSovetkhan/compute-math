# Assignment 2: Solution of Systems of Linear Algebraic Equations

A comprehensive implementation of direct and iterative methods for solving systems of linear equations with an interactive equation parser.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Methods Explained](#methods-explained)
- [Project Structure](#project-structure)
- [Examples](#examples)
- [Features](#features)

## Overview

This project implements six different numerical methods for solving systems of linear equations of the form **Ax = b**, where:
- **A** is an n×n coefficient matrix
- **x** is the solution vector
- **b** is the constants vector

The methods are divided into two categories:
- **Direct Methods**: Compute exact solution (within numerical precision) in finite steps
- **Iterative Methods**: Approach the solution through successive approximations

## Installation

### Requirements
- Python 3.7+
- NumPy
- tabulate

### Install Dependencies
```bash
pip install numpy tabulate
```

## Usage

### Interactive Mode

Run the program and choose from the menu:

```bash
python main.py
```

**Menu Options:**
1. **Run predefined examples** - Test with built-in example systems
2. **Enter custom system** - Input your own equations interactively
3. **Run string input example** - See demonstration with parsed equations
4. **Run all** - Execute both examples and demonstrations

### Option 2: Interactive Input

Enter equations one per line in natural format:

```
Enter system of equations (one per line)
Example format: 4x + y + z = 7
Press Enter twice to finish:

4x + y + z = 7
x + 5y + 2z = 10
x + 2y + 6z = 14
```

**Supported formats:**
- Standard form: `4x + y + z = 7`
- Negative coefficients: `2x - 3y + z = 5`
- Leading negative: `-x + 4y - 2z = 3`
- Any variable names: `a`, `b`, `c`, `x1`, `x2`, etc.

### Programmatic Usage

```python
from solver import solve_system
from input_handler import read_system_from_string

# Parse equations from string
system_str = """
4x + y + z = 7
x + 5y + 2z = 10
x + 2y + 6z = 14
"""

A, b, variables = read_system_from_string(system_str)
solve_system(A, b)
```

Or directly with matrices:

```python
from solver import solve_system

A = [
    [4, 1, 1],
    [1, 5, 2],
    [1, 2, 6]
]
b = [7, 10, 14]

solve_system(A, b)
```

## Methods Explained

### Direct Methods

Direct methods solve the system in a finite number of steps by transforming the coefficient matrix.

#### 1. Cramer's Method

**Algorithm:**
Uses determinants to find each variable individually.

For a system Ax = b, each variable is computed as:

```
x_i = det(A_i) / det(A)
```

where A_i is matrix A with column i replaced by vector b.

**When to use:**
- Small systems (2×2 or 3×3)
- When determinants are needed anyway
- Educational purposes

**Limitations:**
- Computationally expensive for n > 3 (O(n! × n))
- Fails if det(A) = 0 (singular matrix)

**Implementation:** [cramer.py](methods/direct/cramer.py)

---

#### 2. Gaussian Elimination

**Algorithm:**
Two-phase approach:
1. **Forward Elimination**: Transform A into upper triangular form using row operations
2. **Back Substitution**: Solve for variables starting from the last equation

**Process:**
```
[A|b] → [U|b'] → solve from bottom up
```

**Features:**
- Partial pivoting for numerical stability
- Handles most systems efficiently
- O(n³) complexity

**When to use:**
- General purpose solution
- Medium to large systems
- Most reliable direct method

**Implementation:** [gaussian.py](methods/direct/gaussian.py)

---

#### 3. Gauss-Jordan Method

**Algorithm:**
Extended elimination that reduces A to diagonal form (reduced row echelon form).

**Process:**
```
[A|b] → [D|x]  (D is diagonal, solution appears directly)
```

**Difference from Gaussian:**
- Eliminates both above AND below the pivot
- Produces diagonal matrix instead of triangular
- Solution is obtained directly without back substitution

**When to use:**
- When you need the inverse of A
- For educational clarity
- Small to medium systems

**Complexity:** O(n³) but with larger constant than Gaussian

**Implementation:** [gauss_jordan.py](methods/direct/gauss_jordan.py)

---

### Iterative Methods

Iterative methods start with an initial guess and refine it through repeated iterations.

#### 4. Jacobi Method

**Algorithm:**
Simultaneous update of all variables based on the previous iteration.

**Formula:**
For each equation i:
```
x_i^(k+1) = (1/a_ii) * (b_i - sum(a_ij * x_j^(k)) for j ≠ i)
```

**Process:**
- Each variable is updated using OLD values of all other variables
- All updates happen simultaneously
- Requires diagonal dominance for guaranteed convergence

**Convergence condition:**
System is diagonally dominant if:
```
|a_ii| > sum(|a_ij|) for all j ≠ i
```
for all rows i.

**When to use:**
- Large sparse systems
- Parallel computation (updates are independent)
- When diagonal dominance is present

**Implementation:** [jacobi.py](methods/iterative/jacobi.py)

---

#### 5. Gauss-Seidel Method

**Algorithm:**
Sequential update using the most recent values immediately.

**Formula:**
For each equation i:
```
x_i^(k+1) = (1/a_ii) * (b_i - sum(a_ij * x_j^(k+1)) for j < i 
                             - sum(a_ij * x_j^(k)) for j > i)
```

**Key difference from Jacobi:**
- Uses NEW values as soon as they're computed
- Generally converges faster than Jacobi
- Cannot be parallelized easily

**When to use:**
- When faster convergence is needed
- Systems with diagonal dominance
- Sequential computation

**Implementation:** [gauss_seidel.py](methods/iterative/gauss_seidel.py)

---

#### 6. Successive Over-Relaxation (SOR)

**Algorithm:**
Accelerated version of Gauss-Seidel using a relaxation parameter ω.

**Formula:**
```
x_i^(k+1) = (1-ω) * x_i^(k) + ω * x_i^(GS)
```

where x_i^(GS) is the Gauss-Seidel update.

**Relaxation parameter ω:**
- **ω = 1**: Reduces to Gauss-Seidel
- **1 < ω < 2**: Over-relaxation (faster convergence)
- **0 < ω < 1**: Under-relaxation (more stable)
- **Default**: ω = 1.25 (good general choice)

**When to use:**
- When Gauss-Seidel converges but slowly
- Large systems requiring fast convergence
- When optimal ω is known or can be estimated

**Implementation:** [relaxation.py](methods/iterative/relaxation.py)

---

## Project Structure

```
assignment-2/
├── main.py                    # Main program with interactive menu
├── solver.py                  # Core solving logic and result display
├── input_handler.py           # Equation parser for text input
├── methods/
│   ├── direct/
│   │   ├── __init__.py
│   │   ├── cramer.py          # Cramer's method implementation
│   │   ├── gaussian.py        # Gaussian elimination
│   │   └── gauss_jordan.py    # Gauss-Jordan elimination
│   └── iterative/
│       ├── __init__.py
│       ├── jacobi.py          # Jacobi iteration
│       ├── gauss_seidel.py    # Gauss-Seidel method
│       └── relaxation.py      # SOR method
└── README.md                  # This file
```

## Examples

### Example 1: Diagonally Dominant System

**Input:**
```
10x - y + 2z = 6
-x + 11y - z = 25
2x - y + 10z = -11
```

**Results:**
- All methods converge successfully
- Direct methods: exact solution
- Gauss-Seidel: fastest convergence (~10 iterations)
- Jacobi: slower but stable (~19 iterations)

### Example 2: Singular System

**Input:**
```
4x + 123123y - 123z = 1238
4x + 123123y - 123z = 1233
4x + 123123y - 123z = 12332123
```

**Results:**
- Direct methods: Correctly identify singular matrix
- Iterative methods: Diverge (displayed as "Diverged")
- System has no unique solution (rows are identical)

## Output Format

The program provides:

1. **System Display**: Equations in readable format
2. **Method Results**: Individual solutions and iteration counts
3. **Summary Table**: Compact comparison with smart formatting
   - Regular values: 6 decimal places
   - Large/small values: Scientific notation (e.g., `1.2345e+08`)
   - Failed methods: "Failed" status
   - Diverged methods: "Diverged" status
4. **Verification**: Residual calculation (A·x - b) for validation

**Example Output:**
```
================================================================================
SUMMARY TABLE
================================================================================
+----------------------+---------+---------+---------+--------------+
| Method               |      x1 |      x2 |      x3 | Iterations   |
+======================+=========+=========+=========+==============+
| Cramer's Method      | 1.03093 | 1.07217 | 1.80412 | -            |
+----------------------+---------+---------+---------+--------------+
| Gaussian Elimination | 1.03093 | 1.07217 | 1.80412 | -            |
+----------------------+---------+---------+---------+--------------+
| Gauss-Jordan         | 1.03093 | 1.07217 | 1.80412 | -            |
+----------------------+---------+---------+---------+--------------+
| Jacobi               | 1.03093 | 1.07217 | 1.80412 | 40           |
+----------------------+---------+---------+---------+--------------+
| Gauss-Seidel         | 1.03093 | 1.07217 | 1.80412 | 14           |
+----------------------+---------+---------+---------+--------------+
| Relaxation (ω=1.25)  | 1.03093 | 1.07217 | 1.80412 | 22           |
+----------------------+---------+---------+---------+--------------+
```

## Features

### Smart Formatting
- **Adaptive precision**: Automatically chooses best format for values
- **Scientific notation**: For values > 10⁶ or < 10⁻³
- **Clean tables**: No overflow or wrapping issues
- **Clear status**: Failed/Diverged/Success indicators

### Robust Parsing
- **Flexible input**: Handles various equation formats
- **Error detection**: Validates equation syntax
- **Variable detection**: Automatically identifies variable names
- **Whitespace tolerant**: Ignores extra spaces

### Comprehensive Analysis
- **Multiple methods**: Compare 6 different approaches
- **Convergence tracking**: Monitor iterative method performance
- **Error handling**: Graceful handling of singular/ill-conditioned systems
- **Verification**: Residual calculation confirms accuracy

### Numerical Stability
- **Partial pivoting**: Prevents division by small numbers
- **Convergence checking**: Stops when tolerance is met (10⁻¹⁰)
- **Max iterations**: Safety limit (1000 iterations)
- **Finite check**: Detects overflow/NaN values

## Method Comparison

| Method | Time Complexity | Space | Stability | Best For |
|--------|----------------|-------|-----------|----------|
| Cramer's | O(n! × n) | O(n²) | Poor | n ≤ 3 |
| Gaussian | O(n³) | O(n²) | Good | General purpose |
| Gauss-Jordan | O(n³) | O(n²) | Good | Matrix inverse |
| Jacobi | O(k × n²) | O(n) | Fair | Sparse, parallel |
| Gauss-Seidel | O(k × n²) | O(n) | Good | Fast convergence |
| SOR | O(k × n²) | O(n) | Good | Optimized speed |

*k = number of iterations needed

## Limitations

- **Matrix size**: Cramer's method not recommended for n > 4
- **Convergence**: Iterative methods require diagonal dominance
- **Singular systems**: No method can solve singular systems
- **Numerical precision**: Limited to ~15 decimal digits (float64)
- **Iteration limit**: Iterative methods stop after 1000 iterations

## Notes

- Direct methods work best for small to medium systems (n < 1000)
- Iterative methods excel with large sparse systems
- Always check the residual to verify solution accuracy
- For ill-conditioned systems, results may be unreliable
- The relaxation parameter (ω) can be tuned for specific problems
- Diagonal dominance is key for iterative method convergence

## Troubleshooting

**Q: All methods show "Failed"**
- System is likely singular (no unique solution)
- Check if equations are linearly dependent

**Q: Iterative methods show "Diverged"**
- System lacks diagonal dominance
- Try reordering equations to increase diagonal values
- Use a direct method instead

**Q: Results are inaccurate**
- System may be ill-conditioned
- Check residual values in verification section
- Try increasing precision or using a different method

## References

- Burden, R. L., & Faires, J. D. (2010). *Numerical Analysis*
- Press, W. H., et al. (2007). *Numerical Recipes*
- Golub, G. H., & Van Loan, C. F. (2013). *Matrix Computations*
