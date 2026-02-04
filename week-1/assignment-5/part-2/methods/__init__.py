"""
Numerical Integration Methods

This module contains implementations of various numerical integration methods:
- Trapezoidal Rule
- Simpson's 1/3 Rule
- Simpson's 3/8 Rule
"""

from .trapezoidal import trapezoidal_rule
from .simpson_one_third import simpson_one_third_rule
from .simpson_three_eighth import simpson_three_eighth_rule

__all__ = [
    'trapezoidal_rule',
    'simpson_one_third_rule',
    'simpson_three_eighth_rule'
]
