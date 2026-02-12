"""
Exponential Model (a·b^x): y = a * b^x
Using least squares method with linearization.
"""

import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import calculate_sse, solve_2x2


class ExponentialABx:
    """
    Exponential model: y = a * b^x
    
    Linearization: ln(y) = ln(a) + x·ln(b)
    Let Y = ln(y), A = ln(a), B = ln(b)
    Then: Y = A + Bx (straight line)
    """
    
    def __init__(self):
        self.a = None
        self.b = None
        self.name = "Exponential (a·b^x)"
        self.equation = "y = a·b^x"
    
    def fit(self, x_data: list, y_data: list):
        """
        Fit the model to the data using least squares with linearization.
        
        Linearized form: ln(y) = ln(a) + x·ln(b)
        """
        # Filter out non-positive y values
        valid_data = [(x, y) for x, y in zip(x_data, y_data) if y > 0]
        if len(valid_data) < 2:
            raise ValueError("Exponential (a·b^x) model requires positive y values")
        
        x_valid = [d[0] for d in valid_data]
        y_valid = [d[1] for d in valid_data]
        ln_y = [math.log(y) for y in y_valid]
        
        n = len(x_valid)
        sum_x = sum(x_valid)
        sum_ln_y = sum(ln_y)
        sum_x_ln_y = sum(x * ly for x, ly in zip(x_valid, ln_y))
        sum_x2 = sum(x ** 2 for x in x_valid)
        
        # Solve for B and ln(a):
        # | Σx²  Σx | | B    |   | Σx·ln(y) |
        # | Σx   n  | | ln(a)| = | Σln(y)   |
        B, ln_a = solve_2x2(sum_x2, sum_x, sum_x_ln_y, sum_x, n, sum_ln_y)
        
        self.a = math.exp(ln_a)
        self.b = math.exp(B)
        
        return self
    
    def predict(self, x: float) -> float:
        """Predict y for given x."""
        return self.a * (self.b ** x)
    
    def predict_all(self, x_data: list) -> list:
        """Predict y for all x values."""
        return [self.predict(x) for x in x_data]
    
    def get_sse(self, x_data: list, y_data: list) -> float:
        """Calculate SSE for the fitted model."""
        y_pred = self.predict_all(x_data)
        return calculate_sse(y_data, y_pred)
    
    def get_equation_string(self, precision: int = 4) -> str:
        """Return the equation with fitted coefficients."""
        return f"y = {self.a:.{precision}f}·{self.b:.{precision}f}^x"
    
    def get_coefficients(self) -> dict:
        """Return coefficients as dictionary."""
        return {'a': self.a, 'b': self.b}
