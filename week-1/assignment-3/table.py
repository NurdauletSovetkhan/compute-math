"""
Table display for curve fitting results.
"""

from tabulate import tabulate


def display_results_table(results: list, precision: int = 4):
    """
    Display results table with all models.
    
    results: list of dicts with keys:
        - name: model name
        - equation: fitted equation string
        - sse: sum of squared errors
        - coefficients: dict of coefficients
    """
    headers = ["#", "Model", "Fitted Equation", "SSE"]
    
    table_data = []
    for i, result in enumerate(results, 1):
        table_data.append([
            i,
            result['name'],
            result['equation'],
            f"{result['sse']:.{precision}f}"
        ])
    
    print("\n")
    print("CURVE FITTING RESULTS")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Find best model
    best = min(results, key=lambda x: x['sse'])
    print("\n")
    print(f"  BEST FIT: {best['name']}")
    print(f"  Equation: {best['equation']}")
    print(f"  SSE: {best['sse']:.{precision}f}")
    print("\n")

def display_data_table(x_data: list, y_data: list):
    """
    Display input data as a table.
    """
    headers = ["i", "x", "y"]
    table_data = [[i+1, x, y] for i, (x, y) in enumerate(zip(x_data, y_data))]
    
    print("\n" + "=" * 40)
    print("INPUT DATA")
    print("=" * 40)
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print()


def display_predictions_table(x_data: list, y_data: list, models_predictions: dict, precision: int = 4):
    """
    Display predictions from all models side by side.
    
    models_predictions: dict with model names as keys and predicted y values as values
    """
    headers = ["x", "y (actual)"] + list(models_predictions.keys())
    
    table_data = []
    for i, (x, y) in enumerate(zip(x_data, y_data)):
        row = [f"{x:.{precision}f}", f"{y:.{precision}f}"]
        for model_name in models_predictions:
            row.append(f"{models_predictions[model_name][i]:.{precision}f}")
        table_data.append(row)
    
    print("\n")
    print("PREDICTIONS COMPARISON")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print()
