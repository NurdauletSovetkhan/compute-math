"""
Cubic (Third Degree) Model: y = ax³ + bx² + cx + d
Using least squares method.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import calculate_sse, solve_4x4


class Cubic:
    """
    Cubic model: y = ax³ + bx² + cx + d
    """
    
    def __init__(self):
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.name = "Cubic (3rd degree)"
        self.equation = "y = ax³ + bx² + cx + d"
    
    def fit(self, x_data: list, y_data: list):
        """
        Fit the model to the data using least squares.
        
        Normal equations form a 4x4 system.
        """
        n = len(x_data)
        
        sum_x = sum(x_data)
        sum_x2 = sum(x ** 2 for x in x_data)
        sum_x3 = sum(x ** 3 for x in x_data)
        sum_x4 = sum(x ** 4 for x in x_data)
        sum_x5 = sum(x ** 5 for x in x_data)
        sum_x6 = sum(x ** 6 for x in x_data)
        sum_y = sum(y_data)
        sum_xy = sum(x * y for x, y in zip(x_data, y_data))
        sum_x2y = sum((x ** 2) * y for x, y in zip(x_data, y_data))
        sum_x3y = sum((x ** 3) * y for x, y in zip(x_data, y_data))
        
        # System of normal equations:
        # | Σx⁶  Σx⁵  Σx⁴  Σx³ | | a |   | Σx³y |
        # | Σx⁵  Σx⁴  Σx³  Σx² | | b | = | Σx²y |
        # | Σx⁴  Σx³  Σx²  Σx  | | c |   | Σxy  |
        # | Σx³  Σx²  Σx   n   | | d |   | Σy   |
        
        matrix = [
            [sum_x6, sum_x5, sum_x4, sum_x3],
            [sum_x5, sum_x4, sum_x3, sum_x2],
            [sum_x4, sum_x3, sum_x2, sum_x],
            [sum_x3, sum_x2, sum_x, n]
        ]
        constants = [sum_x3y, sum_x2y, sum_xy, sum_y]
        
        solution = solve_4x4(matrix, constants)
        self.a, self.b, self.c, self.d = solution
        
        return self
    
    def predict(self, x: float) -> float:
        """Predict y for given x."""
        return self.a * x**3 + self.b * x**2 + self.c * x + self.d
    
    def predict_all(self, x_data: list) -> list:
        """Predict y for all x values."""
        return [self.predict(x) for x in x_data]
    
    def get_sse(self, x_data: list, y_data: list) -> float:
        """Calculate SSE for the fitted model."""
        y_pred = self.predict_all(x_data)
        return calculate_sse(y_data, y_pred)
    
    def get_equation_string(self, precision: int = 4) -> str:
        """Return the equation with fitted coefficients."""
        return f"y = {self.a:.{precision}f}x³ + {self.b:.{precision}f}x² + {self.c:.{precision}f}x + {self.d:.{precision}f}"
    
    def get_coefficients(self) -> dict:
        """Return coefficients as dictionary."""
        return {'a': self.a, 'b': self.b, 'c': self.c, 'd': self.d}
