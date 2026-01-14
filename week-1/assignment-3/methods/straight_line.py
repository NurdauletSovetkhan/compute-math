"""
Straight Line Model: y = ax + b
Using least squares method.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import calculate_sse, solve_2x2


class StraightLine:
    """
    Straight line model: y = ax + b
    """
    
    def __init__(self):
        self.a = None
        self.b = None
        self.name = "Straight Line"
        self.equation = "y = ax + b"
    
    def fit(self, x_data: list, y_data: list):
        """
        Fit the model to the data using least squares.
        
        Normal equations:
        Σy = a·Σx + b·n
        Σxy = a·Σx² + b·Σx
        """
        n = len(x_data)
        
        sum_x = sum(x_data)
        sum_y = sum(y_data)
        sum_xy = sum(x * y for x, y in zip(x_data, y_data))
        sum_x2 = sum(x ** 2 for x in x_data)
        
        # Solve system:
        # | sum_x2  sum_x | | a |   | sum_xy |
        # | sum_x   n     | | b | = | sum_y  |
        self.a, self.b = solve_2x2(sum_x2, sum_x, sum_xy, sum_x, n, sum_y)
        
        return self
    
    def predict(self, x: float) -> float:
        """Predict y for given x."""
        return self.a * x + self.b
    
    def predict_all(self, x_data: list) -> list:
        """Predict y for all x values."""
        return [self.predict(x) for x in x_data]
    
    def get_sse(self, x_data: list, y_data: list) -> float:
        """Calculate SSE for the fitted model."""
        y_pred = self.predict_all(x_data)
        return calculate_sse(y_data, y_pred)
    
    def get_equation_string(self, precision: int = 4) -> str:
        """Return the equation with fitted coefficients."""
        return f"y = {self.a:.{precision}f}x + {self.b:.{precision}f}"
    
    def get_coefficients(self) -> dict:
        """Return coefficients as dictionary."""
        return {'a': self.a, 'b': self.b}
