"""
DSL/chemistry/compounds.py

Defines a Compound class for representing chemical compounds and provides
a basic formula parser.
"""

import re
from DSL.chemistry.elements import get_element, ELEMENTS

class Compound:
    def __init__(self, formula: str):
        self.formula = formula
        self.composition = parse_formula(formula)  # Dict of element: count

    def __repr__(self):
        return f"Compound('{self.formula}')"

    def molar_mass(self):
        """Calculate the molar mass of the compound based on its composition."""
        mass = 0
        for element, count in self.composition.items():
            if element in ELEMENTS:
                mass += ELEMENTS[element]['atomic_weight'] * count
            else:
                raise ValueError(f"Unknown element: {element}")
        return mass


def parse_formula(formula: str) -> dict:
    """
    Parse a chemical formula string into a dictionary of elements and their counts.
    Handles nested parentheses, e.g., "Ca(NO3)2" or "H2O" or "((CH3)3C)2NH".
    """
    # Use regex to find elements, subscripts, and handle parentheses
    pattern = r'(?:\(([^()]*)\)|([A-Z][a-z]?))(\d*)'

    def parse_recursive(form):
        composition = {}
        matches = re.findall(pattern, form)

        for group, elem, count in matches:
            if group:  # Parenthesized group
                subcomp = parse_recursive(group)
                mult = int(count) if count else 1
                for e, c in subcomp.items():
                    composition[e] = composition.get(e, 0) + c * mult
            elif elem:  # Single element
                if elem not in ELEMENTS:
                    raise ValueError(f"Unknown element symbol: {elem}")
                mult = int(count) if count else 1
                composition[elem] = composition.get(elem, 0) + mult

        return composition

    # Remove any whitespace and validate the formula
    formula = formula.strip()
    if not formula:
        raise ValueError("Empty formula")

    # If formula is a compound object, extract its formula string
    if hasattr(formula, 'formula'):
        formula = formula.formula

    try:
        return parse_recursive(formula)
    except Exception as e:
        raise ValueError(f"Invalid formula: {formula}. {str(e)}")
