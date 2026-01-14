"""
Main program for Curve Fitting Models.
Runs all models on input data and finds the best fit.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from methods import StraightLine, Quadratic, Cubic, Exponential, Logarithmic, Power
from table import display_results_table, display_data_table
from graph import plot_all_models
from examples import get_all_examples, get_example


# All available models
ALL_MODELS = [
    ('Straight Line', StraightLine),
    ('Quadratic (2nd degree)', Quadratic),
    ('Cubic (3rd degree)', Cubic),
    ('Exponential', Exponential),
    ('Logarithmic', Logarithmic),
    ('Power', Power)
]


def parse_input(input_str: str) -> list:
    """Parse space-separated numbers from input string."""
    return [float(x) for x in input_str.strip().split()]


def get_models_by_indices(indices: list) -> list:
    """Get model instances by their indices (1-based)."""
    models = []
    for idx in indices:
        if 1 <= idx <= len(ALL_MODELS):
            models.append(ALL_MODELS[idx - 1][1]())  # Create instance
    return models


def fit_models(x_data: list, y_data: list, models: list):
    """
    Fit specified models to the data and return results.
    """
    results = []
    fitted_models = []
    
    for model in models:
        try:
            model.fit(x_data, y_data)
            sse = model.get_sse(x_data, y_data)
            
            results.append({
                'name': model.name,
                'equation': model.get_equation_string(),
                'sse': sse,
                'coefficients': model.get_coefficients()
            })
            fitted_models.append(model)
        except Exception as e:
            print(f"Warning: {model.name} fitting failed: {e}")
            results.append({
                'name': model.name,
                'equation': "N/A (fitting failed)",
                'sse': float('inf'),
                'coefficients': {}
            })
    
    return results, fitted_models


def fit_all_models(x_data: list, y_data: list):
    """
    Fit all models to the data and return results.
    """
    models = [model_class() for _, model_class in ALL_MODELS]
    return fit_models(x_data, y_data, models)


def run_with_data(x_data: list, y_data: list, models: list = None, show_graph: bool = True):
    """
    Run curve fitting with given data.
    If models is None, use all models.
    """
    if len(x_data) != len(y_data):
        print("Error: x and y must have the same number of elements!")
        return
    
    if len(x_data) < 2:
        print("Error: At least 2 data points are required!")
        return
    
    # Display input data
    display_data_table(x_data, y_data)
    
    # Fit models
    if models is None:
        results, fitted_models = fit_all_models(x_data, y_data)
    else:
        results, fitted_models = fit_models(x_data, y_data, models)
    
    # Display results table
    display_results_table(results)
    
    # Show graph
    if show_graph and fitted_models:
        plot_all_models(x_data, y_data, fitted_models)


def interactive_input():
    """
    Get data from user input.
    """
    print("\nEnter x values (space-separated):")
    x_str = input("> ")
    x_data = parse_input(x_str)
    
    print("Enter y values (space-separated):")
    y_str = input("> ")
    y_data = parse_input(y_str)
    
    return x_data, y_data


def select_models_menu():
    """
    Display model selection menu and return selected models.
    """
    print("SELECT MODELS:")
    
    for i, (name, _) in enumerate(ALL_MODELS, 1):
        print(f"  {i}. {name}")
    
    print(f"  A. All models")
    print("Enter model numbers (comma or space separated)")
    print("Example: 1,2,3 or 1 2 3 or A for all")
    
    choice = input("> ").strip().upper()
    
    if choice == 'A':
        return [model_class() for _, model_class in ALL_MODELS]
    
    # Parse indices
    try:
        # Support both comma and space separated
        choice = choice.replace(',', ' ')
        indices = [int(x) for x in choice.split()]
        models = get_models_by_indices(indices)
        
        if not models:
            print("No valid models selected. Using all models.")
            return [model_class() for _, model_class in ALL_MODELS]
        
        print(f"Selected: {', '.join(m.name for m in models)}")
        return models
    except ValueError:
        print("Invalid input. Using all models.")
        return [model_class() for _, model_class in ALL_MODELS]


def show_menu():
    """
    Display main menu and handle user choice.
    """
    while True:
        print("       CURVE FITTING - ASSIGNMENT 3")
        
        examples = get_all_examples()
        for i, ex in enumerate(examples, 1):
            print(f"  {i}. {ex['name']}")
            print(f"     {ex['description']}")
        
        print(f"  {len(examples) + 1}. Enter custom data (all models)")
        print(f"  {len(examples) + 2}. Enter custom data (select models)")
        print(f"  0. Exit")
        
        try:
            choice = int(input("Choose option: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        
        if choice == 0:
            print("Goodbye!")
            break
        elif 1 <= choice <= len(examples):
            ex = get_example(choice)
            print(f"\n>>> Running: {ex['name']}")
            run_with_data(ex['x'], ex['y'])
        elif choice == len(examples) + 1:
            # Custom data with all models
            try:
                x_data, y_data = interactive_input()
                run_with_data(x_data, y_data)
            except Exception as e:
                print(f"Error parsing input: {e}")
        elif choice == len(examples) + 2:
            # Custom data with model selection
            try:
                x_data, y_data = interactive_input()
                models = select_models_menu()
                run_with_data(x_data, y_data, models=models)
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("Invalid option. Please try again.")


def main():
    """
    Main entry point.
    """
    print("\n" + "*" * 46)
    print("*   Curve Fitting Models - Least Squares Method  *")
    print("*" * 46 + "\n")
    
    show_menu()


if __name__ == "__main__":
    main()
