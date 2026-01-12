import numpy as np
from determinant import get_determinant

# Matrix Inverse using Gauss-Jordan Elimination
# To find the inverse, we augment our matrix A with the identity matrix [A | I].
# Then we apply row operations to transform A into the identity matrix.
# Whatever happens to I becomes our inverse: [I | A^(-1)].
# We use partial pivoting to avoid numerical issues.
# Note: the matrix must be square and non-singular (determinant not zero) to have an inverse.

def get_inverse_matrix(matrix):
    if isinstance(matrix, list):
        A = np.array(matrix, dtype=float)
    else:
        A = matrix.astype(float)
    
    n = len(A)
    
    if A.shape[0] != A.shape[1]:
        raise ValueError("Matrix must be square")
    
    det = get_determinant(A.tolist() if isinstance(A, np.ndarray) else A)
    if abs(det) < 1e-10:
        raise ValueError("Matrix is singular (determinant is zero), cannot compute inverse")
    
    augmented = np.hstack([A, np.eye(n)]) # eye is a identify matrix
    
    for i in range(n):
        # Partial pivoting find the row with maximum value in column i
        max_row = i + np.argmax(np.abs(augmented[i:, i]))
        if max_row != i:
            augmented[[i, max_row]] = augmented[[max_row, i]]
        
        # Scale the pivot row
        pivot = augmented[i, i]
        if abs(pivot) < 1e-10:
            raise ValueError("Matrix is singular")
        augmented[i] = augmented[i] / pivot
        
        # Eliminate column i in all other rows
        for j in range(n):
            if i != j:
                factor = augmented[j, i]
                augmented[j] -= factor * augmented[i]
    
    # Extract the inverse matrix from the right half of augmented matrix
    inverse = augmented[:, n:]
    
    return inverse


def print_inverse_matrix(matrix, label=""):
    try:
        inverse = get_inverse_matrix(matrix)
        
        if label:
            print(f"\n{label}")
        else:
            print("\nInverse Matrix:")
        
        # Print with nice formatting
        print(inverse)
        
        return inverse
        
    except ValueError as e:
        print(f"\nError: {e}")
        return None
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        return None


if __name__ == "__main__":  
    # Test 1: 2x2 matrix
    print("\nTest 1: 2x2 Matrix")
    matrix1 = [[4, 7], [2, 6]]
    print("Original Matrix:")
    print(np.array(matrix1))
    print_inverse_matrix(matrix1)
    
    # Test 2: 3x3 matrix
    print("\nTest 2: 3x3 Matrix")
    matrix2 = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
    print("Original Matrix:")
    print(np.array(matrix2))
    print_inverse_matrix(matrix2)
    
    # Test 3: Singular matrix (should fail)
    print("\nTest 3: Singular Matrix (should fail)")
    matrix3 = [[1, 2, 3], [2, 4, 6], [1, 2, 3]]
    print("Original Matrix:")
    print(np.array(matrix3))
    print_inverse_matrix(matrix3)
