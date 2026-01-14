"""
Power Model: y = a * x^b
Using least squares method with linearization.
"""

import sys
import os
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import calculate_sse, solve_2x2


class Power:
    """
    Power model: y = a * x^b
    
    Linearization: ln(y) = ln(a) + b·ln(x)
    Let Y = ln(y), X = ln(x), A = ln(a)
    Then: Y = A + bX (straight line)
    """
    
    def __init__(self):
        self.a = None
        self.b = None
        self.name = "Power"
        self.equation = "y = a·x^b"
    
    def fit(self, x_data: list, y_data: list):
        """
        Fit the model to the data using least squares with linearization.
        
        Linearized form: ln(y) = ln(a) + b·ln(x)
        """
        # Filter out non-positive values
        valid_data = [(x, y) for x, y in zip(x_data, y_data) if x > 0 and y > 0]
        if len(valid_data) < 2:
            raise ValueError("Power model requires positive x and y values")
        
        x_valid = [d[0] for d in valid_data]
        y_valid = [d[1] for d in valid_data]
        
        # Transform to logarithms
        ln_x = [math.log(x) for x in x_valid]
        ln_y = [math.log(y) for y in y_valid]
        
        n = len(ln_x)
        sum_ln_x = sum(ln_x)
        sum_ln_y = sum(ln_y)
        sum_ln_x_ln_y = sum(lx * ly for lx, ly in zip(ln_x, ln_y))
        sum_ln_x2 = sum(lx ** 2 for lx in ln_x)
        
        # Solve for b and ln(a):
        # | Σln(x)²  Σln(x) | | b    |   | Σln(x)·ln(y) |
        # | Σln(x)   n      | | ln(a)| = | Σln(y)       |
        self.b, ln_a = solve_2x2(sum_ln_x2, sum_ln_x, sum_ln_x_ln_y, sum_ln_x, n, sum_ln_y)
        self.a = math.exp(ln_a)
        
        return self
    
    def predict(self, x: float) -> float:
        """Predict y for given x."""
        if x <= 0:
            raise ValueError("x must be positive for power model")
        return self.a * (x ** self.b)
    
    def predict_all(self, x_data: list) -> list:
        """Predict y for all x values."""
        return [self.predict(x) for x in x_data]
    
    def get_sse(self, x_data: list, y_data: list) -> float:
        """Calculate SSE for the fitted model."""
        y_pred = self.predict_all(x_data)
        return calculate_sse(y_data, y_pred)
    
    def get_equation_string(self, precision: int = 4) -> str:
        """Return the equation with fitted coefficients."""
        return f"y = {self.a:.{precision}f}·x^{self.b:.{precision}f}"
    
    def get_coefficients(self) -> dict:
        """Return coefficients as dictionary."""
        return {'a': self.a, 'b': self.b}
