# Assignment 3: Curve Fitting Models

## Requirements

The project consists of 6 model files and 1 main program:

1. **Straight line** - $y = ax + b$ 
2. **Second degree curve** - $y = ax^2 + bx + c$
3. **Third degree curve** - $y = ax^3 + bx^2 + cx + d$
4. **Exponential curve** - $y = a e^{bx}$
5. **Logarithmic curve** - $y = a + b\ln x$
6. **Power curve** - $y = ax^b$
7. **Main program** - runs all models on a single input dataset

## Overview

The main program processes input data through all available models and calculates the Sum of Squared Errors (SSE) for each, comparing actual values with predicted ones. Based on these calculations, `main` identifies the model with the minimum SSE value and returns it as the best fit for the given dataset.

## Entry data

Inputs are made like a matrix. For example:

| x   | 1   | 2   | 3   | 4   | 5   |
| --- | --- | --- | --- | --- | --- |
| y   | 0.5 | 1.1 | 1.6 | 2.1 | 2.5 |

But the program should accept only matrx, so you must type: \
1 2 3 4 5 \
and then: \
0.5 1.1 1.6 2.1 2.5