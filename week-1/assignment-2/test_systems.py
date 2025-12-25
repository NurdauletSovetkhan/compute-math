import numpy as np


def get_systems():
    """
    Returns a list of test systems of linear equations.
    Each system is a tuple (A, b, description)
    """
    
    systems = []
    
    # System 1: Simple 3x3 diagonally dominant system
    A1 = np.array([
        [10, -1, 2],
        [-1, 11, -1],
        [2, -1, 10]
    ], dtype=float)
    b1 = np.array([6, 25, -11], dtype=float)
    systems.append((A1, b1, "System 1: 3x3 Diagonally Dominant"))
    
    # System 2: Another 3x3 system
    A2 = np.array([
        [4, -1, 0],
        [-1, 4, -1],
        [0, -1, 4]
    ], dtype=float)
    b2 = np.array([15, 10, 10], dtype=float)
    systems.append((A2, b2, "System 2: 3x3 Tridiagonal"))
    
    # System 3: 4x4 diagonally dominant system
    A3 = np.array([
        [10, 1, 0, 1],
        [1, 10, 2, 0],
        [0, 2, 10, 1],
        [1, 0, 1, 10]
    ], dtype=float)
    b3 = np.array([12, 13, 13, 12], dtype=float)
    systems.append((A3, b3, "System 3: 4x4 Diagonally Dominant"))
    
    # System 4: 2x2 simple system
    A4 = np.array([
        [3, 1],
        [1, 2]
    ], dtype=float)
    b4 = np.array([9, 8], dtype=float)
    systems.append((A4, b4, "System 4: 2x2 Simple"))
    
    return systems
