"""
Graph visualization for curve fitting models.
"""

import numpy as np
import matplotlib.pyplot as plt


def plot_all_models(x_data: list, y_data: list, models: list, title: str = "Curve Fitting Comparison"):
    """
    Plot all fitted models on a single graph.
    
    x_data: original x values
    y_data: original y values
    models: list of fitted model objects
    """
    # Create figure
    plt.figure(figsize=(12, 8))
    
    # Plot original data points
    plt.scatter(x_data, y_data, color='black', s=100, zorder=5, label='Data points', marker='o')
    
    # Generate smooth x values for plotting curves
    x_min, x_max = min(x_data), max(x_data)
    margin = (x_max - x_min) * 0.1
    x_smooth = np.linspace(max(0.01, x_min - margin), x_max + margin, 200)
    
    # Colors for different models
    colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#a65628']
    
    # Plot each model
    for i, model in enumerate(models):
        try:
            y_smooth = [model.predict(x) for x in x_smooth]
            plt.plot(x_smooth, y_smooth, color=colors[i % len(colors)], 
                    linewidth=2, label=f"{model.name}: {model.get_equation_string()}")
        except Exception as e:
            # Some models may fail for certain x values (e.g., log of negative)
            # Try with filtered x values
            try:
                x_filtered = [x for x in x_smooth if x > 0]
                y_filtered = [model.predict(x) for x in x_filtered]
                plt.plot(x_filtered, y_filtered, color=colors[i % len(colors)], 
                        linewidth=2, label=f"{model.name}: {model.get_equation_string()}")
            except:
                print(f"Warning: Could not plot {model.name}")
    
    # Customize plot
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=9)
    plt.grid(True, alpha=0.3)
    
    # Set reasonable y limits
    y_min, y_max = min(y_data), max(y_data)
    y_margin = (y_max - y_min) * 0.3
    plt.ylim(y_min - y_margin, y_max + y_margin)
    
    plt.tight_layout()
    plt.show()


def plot_best_model(x_data: list, y_data: list, model, title: str = "Best Fit Model"):
    """
    Plot only the best fitting model.
    
    x_data: original x values
    y_data: original y values
    model: the best fitted model object
    """
    plt.figure(figsize=(10, 6))
    
    # Plot original data points
    plt.scatter(x_data, y_data, color='blue', s=100, zorder=5, label='Data points', marker='o')
    
    # Generate smooth x values for plotting curve
    x_min, x_max = min(x_data), max(x_data)
    margin = (x_max - x_min) * 0.1
    x_smooth = np.linspace(max(0.01, x_min - margin), x_max + margin, 200)
    
    try:
        y_smooth = [model.predict(x) for x in x_smooth]
        plt.plot(x_smooth, y_smooth, color='red', linewidth=2.5, 
                label=f"{model.name}\n{model.get_equation_string()}")
    except:
        x_filtered = [x for x in x_smooth if x > 0]
        y_filtered = [model.predict(x) for x in x_filtered]
        plt.plot(x_filtered, y_filtered, color='red', linewidth=2.5, 
                label=f"{model.name}\n{model.get_equation_string()}")
    
    plt.xlabel('x', fontsize=12)
    plt.ylabel('y', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
