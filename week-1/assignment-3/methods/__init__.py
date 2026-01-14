"""
Curve fitting methods module.
"""

from .straight_line import StraightLine
from .quadratic import Quadratic
from .cubic import Cubic
from .exponential import Exponential
from .logarithmic import Logarithmic
from .power import Power

__all__ = [
    'StraightLine',
    'Quadratic', 
    'Cubic',
    'Exponential',
    'Logarithmic',
    'Power'
]
