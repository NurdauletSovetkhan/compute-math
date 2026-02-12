"""
Curve fitting methods module.
"""

from .straight_line import StraightLine
from .quadratic import Quadratic
from .cubic import Cubic
from .exponential import Exponential
from .exponential_abx import ExponentialABx
from .logarithmic import Logarithmic
from .power import Power

__all__ = [
    'StraightLine',
    'Quadratic', 
    'Cubic',
    'Exponential',
    'ExponentialABx',
    'Logarithmic',
    'Power'
]
