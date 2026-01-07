# Determinant Calculation using Cofactor Expansion (Laplace Expansion)
# The determinant tells us if a matrix is invertible and has geometric meaning (scaling factor).
# For small matrices (1x1, 2x2) we use direct formulas.
# For larger ones, we expand along the first row: pick each element, multiply by its cofactor,
# and recursively calculate the determinant of the smaller matrix (minor).
# Sign alternates: + - + - ... based on position.

def get_determinant(matrix):
    # Base case for 1x1 and 2x2 matrices
    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    # If larger than 2x2, use recursion to calculate determinant
    determinant = 0
    for c in range(len(matrix)):
        minor = [row[:c] + row[c+1:] for row in matrix[1:]]
        
        sign = (-1) ** c
        determinant += sign * matrix[0][c] * get_determinant(minor)
        
    return determinant

if __name__ == "__main__":
    A = [
        [4, 3, 4],
        [6, 3, 2],
        [1, 5, 7]
    ]
    print("Determinant:", get_determinant(A))  