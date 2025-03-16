"""
DSL/chemistry/elements.py

Provides definitions and data for chemical elements.
"""

# A minimal periodic table dictionary.
ELEMENTS = {
    'H': {'name': 'Hydrogen', 'atomic_weight': 1.008},
    'He': {'name': 'Helium', 'atomic_weight': 4.0026},
    'C': {'name': 'Carbon', 'atomic_weight': 12.011},
    'O': {'name': 'Oxygen', 'atomic_weight': 15.999},
    'N': {'name': 'Nitrogen', 'atomic_weight': 14.007},
    # Extend this dictionary with more elements as needed.
}

def get_element(symbol: str):
    return ELEMENTS.get(symbol, None)
