# Assignment 2: Solving Systems of Linear Equations

## Overview
This assignment implements and compares two methods for solving systems of linear equations:
- **Direct Method**: Gaussian Elimination (provides true/exact value)
- **Iterative Method**: Gauss-Seidel (provides approximate value)

## Methods Implemented

### 1. Gaussian Elimination (Direct Method)
- Solves the system Ax = b directly using forward elimination and back substitution
- Includes partial pivoting for numerical stability
- Provides the "true value" for comparison
- File: `gaussian_elimination.py`

### 2. Gauss-Seidel (Iterative Method)
- Iteratively refines the solution starting from an initial guess (zeros by default)
- Uses updated values as soon as they become available
- Shows convergence through iterations
- Provides approximate value with error tracking
- File: `gauss_seidel.py`

## Files Structure

```
assignment-2/
├── main.py                   # Main program to run all tests
├── gaussian_elimination.py   # Direct method implementation
├── gauss_seidel.py          # Iterative method implementation
├── test_systems.py          # Test systems of equations
└── README.md                # This file
```

## Test Systems

The program solves 4 different systems of linear equations:

1. **System 1**: 3x3 Diagonally Dominant
2. **System 2**: 3x3 Tridiagonal
3. **System 3**: 4x4 Diagonally Dominant
4. **System 4**: 2x2 Simple System

All systems are chosen to be diagonally dominant or well-conditioned to ensure convergence of the Gauss-Seidel method.

## How to Run

```bash
cd assignment-2
python main.py
```

## Output Format

For each system, the program displays:

1. **System Description**: Shows the coefficient matrix A and constant vector b
2. **Direct Method Solution**: Exact solution from Gaussian Elimination (10 decimal places)
3. **Iteration Table**: Shows the value of each variable at each iteration, including:
   - Iteration number
   - Values of all variables (x1, x2, x3, ...)
   - Maximum error between consecutive iterations
   - Error compared to the true value
4. **Comparison**: Final comparison showing:
   - Direct vs iterative solution for each variable
   - Absolute error for each variable
   - Maximum absolute error
   - Convergence status

## Key Features

- ✅ Implements one direct method (Gaussian Elimination)
- ✅ Implements one iterative method (Gauss-Seidel)
- ✅ Solves multiple systems of equations
- ✅ Displays iteration table showing variable values at each step
- ✅ Uses direct method as true value
- ✅ Iterative method provides approximate value
- ✅ Tracks convergence and error at each iteration
- ✅ Compares final solutions

## Requirements

- Python 3.x
- NumPy

## Notes

- The Gauss-Seidel method requires the system to be diagonally dominant or to satisfy certain convergence criteria
- The program uses a tolerance of 1e-6 and maximum of 50 iterations by default
- All test systems are carefully chosen to ensure convergence
