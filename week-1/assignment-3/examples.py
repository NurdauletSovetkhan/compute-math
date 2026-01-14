"""
Example datasets for curve fitting demonstration.
"""


# Example 1: Nearly linear data (from README)
EXAMPLE_1 = {
    'name': 'Linear Dataset',
    'description': 'Nearly linear relationship between x and y',
    'x': [1, 2, 3, 4, 5],
    'y': [0.5, 1.1, 1.6, 2.1, 2.5]
}


# Example 2: Exponential growth data
EXAMPLE_2 = {
    'name': 'Exponential Dataset',
    'description': 'Exponential growth pattern',
    'x': [1, 2, 3, 4, 5, 6],
    'y': [2.7, 7.4, 20.1, 54.6, 148.4, 403.4]
}


# Example 3: Logarithmic data
EXAMPLE_3 = {
    'name': 'Logarithmic Dataset', 
    'description': 'Logarithmic growth pattern',
    'x': [1, 2, 3, 4, 5, 6, 7, 8],
    'y': [1.0, 1.7, 2.1, 2.4, 2.6, 2.8, 2.9, 3.1]
}


def get_all_examples():
    """Return all available examples."""
    return [EXAMPLE_1, EXAMPLE_2, EXAMPLE_3]


def get_example(index: int) -> dict:
    """Get example by index (1-based)."""
    examples = get_all_examples()
    if 1 <= index <= len(examples):
        return examples[index - 1]
    raise ValueError(f"Example {index} not found. Available: 1-{len(examples)}")
