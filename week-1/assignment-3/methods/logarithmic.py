"""
Logarithmic Model: y = a + b·ln(x)
Using least squares method.
"""

import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import calculate_sse, solve_2x2


class Logarithmic:
    """
    Logarithmic model: y = a + b·ln(x)
    
    This is already linear in ln(x), so we can use direct least squares.
    Let X = ln(x), then: y = a + bX
    """
    
    def __init__(self):
        self.a = None
        self.b = None
        self.name = "Logarithmic"
        self.equation = "y = a + b·ln(x)"
    
    def fit(self, x_data: list, y_data: list):
        """
        Fit the model to the data using least squares.
        
        Substitution: X = ln(x)
        Then solve: y = a + bX
        """
        # Filter out non-positive x values
        valid_data = [(x, y) for x, y in zip(x_data, y_data) if x > 0]
        if len(valid_data) < 2:
            raise ValueError("Logarithmic model requires positive x values")
        
        x_valid = [d[0] for d in valid_data]
        y_valid = [d[1] for d in valid_data]
        
        # Transform x to ln(x)
        ln_x = [math.log(x) for x in x_valid]
        
        n = len(ln_x)
        sum_ln_x = sum(ln_x)
        sum_y = sum(y_valid)
        sum_ln_x_y = sum(lx * y for lx, y in zip(ln_x, y_valid))
        sum_ln_x2 = sum(lx ** 2 for lx in ln_x)
        
        # Solve for a and b:
        # | n        Σln(x)   | | a |   | Σy       |
        # | Σln(x)   Σln(x)²  | | b | = | Σln(x)·y |
        self.a, self.b = solve_2x2(n, sum_ln_x, sum_y, sum_ln_x, sum_ln_x2, sum_ln_x_y)
        
        return self
    
    def predict(self, x: float) -> float:
        """Predict y for given x."""
        if x <= 0:
            raise ValueError("x must be positive for logarithmic model")
        return self.a + self.b * math.log(x)
    
    def predict_all(self, x_data: list) -> list:
        """Predict y for all x values."""
        return [self.predict(x) for x in x_data]
    
    def get_sse(self, x_data: list, y_data: list) -> float:
        """Calculate SSE for the fitted model."""
        y_pred = self.predict_all(x_data)
        return calculate_sse(y_data, y_pred)
    
    def get_equation_string(self, precision: int = 4) -> str:
        """Return the equation with fitted coefficients."""
        return f"y = {self.a:.{precision}f} + {self.b:.{precision}f}·ln(x)"
    
    def get_coefficients(self) -> dict:
        """Return coefficients as dictionary."""
        return {'a': self.a, 'b': self.b}
