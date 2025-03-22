"""
DSL/chemistry/elements.py

Provides definitions and data for chemical elements.
"""

# A more complete periodic table dictionary
ELEMENTS = {
    'H': {'name': 'Hydrogen', 'atomic_weight': 1.008},
    'He': {'name': 'Helium', 'atomic_weight': 4.0026},
    'Li': {'name': 'Lithium', 'atomic_weight': 6.94},
    'Be': {'name': 'Beryllium', 'atomic_weight': 9.0122},
    'B': {'name': 'Boron', 'atomic_weight': 10.81},
    'C': {'name': 'Carbon', 'atomic_weight': 12.011},
    'N': {'name': 'Nitrogen', 'atomic_weight': 14.007},
    'O': {'name': 'Oxygen', 'atomic_weight': 15.999},
    'F': {'name': 'Fluorine', 'atomic_weight': 18.998},
    'Ne': {'name': 'Neon', 'atomic_weight': 20.180},
    'Na': {'name': 'Sodium', 'atomic_weight': 22.990},
    'Mg': {'name': 'Magnesium', 'atomic_weight': 24.305},
    'Al': {'name': 'Aluminum', 'atomic_weight': 26.982},
    'Si': {'name': 'Silicon', 'atomic_weight': 28.085},
    'P': {'name': 'Phosphorus', 'atomic_weight': 30.974},
    'S': {'name': 'Sulfur', 'atomic_weight': 32.06},
    'Cl': {'name': 'Chlorine', 'atomic_weight': 35.45},
    'Ar': {'name': 'Argon', 'atomic_weight': 39.948},
    'K': {'name': 'Potassium', 'atomic_weight': 39.098},
    'Ca': {'name': 'Calcium', 'atomic_weight': 40.078},
    'Fe': {'name': 'Iron', 'atomic_weight': 55.845},
    'Cu': {'name': 'Copper', 'atomic_weight': 63.546},
    'Zn': {'name': 'Zinc', 'atomic_weight': 65.38},
}

def get_element(symbol):
    """
    Get element data for the given symbol.
    Raises ValueError if the element symbol is unknown.
    """
    if symbol not in ELEMENTS:
        raise ValueError(f"Unknown element symbol: {symbol}")
    return ELEMENTS[symbol]