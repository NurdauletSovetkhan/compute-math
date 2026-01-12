import numpy as np
from test_systems import get_systems
from inverse_matrix import print_inverse_matrix

print("=" * 80)
print("TESTING INVERSE MATRICES FOR ALL SYSTEMS")
print("=" * 80)

systems = get_systems()

for A, b, description in systems:
    print(f"\n{description}")
    print("Original Matrix:")
    print(A)
    print_inverse_matrix(A, label="")
    print("=" * 80)
