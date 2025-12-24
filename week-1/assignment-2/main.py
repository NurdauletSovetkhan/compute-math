from solver import solve_system
from input_handler import read_system_from_input, read_system_from_string


def run_examples():
    """Run predefined example systems."""
    print("RUNNING PREDEFINED EXAMPLES")
    
    # Example 1: 4x4 system
    print("\n\nExample 1: 4x4 System")
    A1 = [
        [4, -1,  0,  1],
        [-1, 4, -1,  0],
        [0, -1,  4, -1],
        [1,  0, -1,  4]
    ]
    b1 = [2, 1, 3, 2]
    solve_system(A1, b1)
    

    
    # # Example 3: 3x3 system
    # print("\n\n" + "="*80)
    # print("\nExample 3: 3x3 System")
    # A3 = [
    #     [10, -1,  2],
    #     [-1, 11, -1],
    #     [2, -1,  10]
    # ]
    # b3 = [6, 25, -11]
    # solve_system(A3, b3)


def run_custom_input():
    """Run solver with user input."""
    print("="*80)
    print("CUSTOM INPUT MODE")
    print("="*80)
    
    try:
        A, b, variables = read_system_from_input()
        print(f"\nDetected variables: {', '.join(variables)}")
        print(f"System size: {len(A)}x{len(variables)}")
        solve_system(A, b)
    except Exception as e:
        print(f"\nError parsing input: {e}")


def run_string_input():
    """Run solver with predefined string input."""
    print("="*80)
    print("STRING INPUT EXAMPLE")
    print("="*80)
    
    system_str = """
    4x + y + z = 7
    x + 5y + 2z = 10
    x + 2y + 6z = 14
    """
    
    print("\nParsing system:")
    print(system_str)
    
    try:
        A, b, variables = read_system_from_string(system_str)
        print(f"Detected variables: {', '.join(variables)}")
        solve_system(A, b)
    except Exception as e:
        print(f"\nError parsing input: {e}")


if __name__ == "__main__":
    print("SOLUTION OF SYSTEM OF LINEAR ALGEBRAIC EQUATIONS\n")
    print("\nChoose mode:")
    print("1. Run predefined examples")
    print("2. Enter custom system")
    print("3. Run string input example")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == '1':
        run_examples()
    elif choice == '2':
        run_custom_input()
    elif choice == '3':
        run_string_input()
    else:
        print("Invalid choice. Running string input example...")
        run_string_input()
