"""
DSL/chemistry/compounds.py

Defines a Compound class for representing chemical compounds and provides
a basic formula parser.
"""

import re
from DSL.chemistry.elements import ELEMENTS

class Compound:
    def __init__(self, formula: str):
        self.formula = formula
        try:
            self.composition = parse_formula(formula)  # Dict of element: count
        except ValueError as e:
            raise ValueError(f"Invalid compound formula '{formula}': {str(e)}")

    def __repr__(self):
        return f"Compound('{self.formula}')"

    def __str__(self):
        return self.formula

    def __eq__(self, other):
        if isinstance(other, str):
            return self.formula == other
        if isinstance(other, Compound):
            return self.formula == other.formula
        return False

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
    # If the formula is already a Compound object, extract its formula string
    if hasattr(formula, 'formula'):
        formula = formula.formula

    # Remove any whitespace and validate the formula
    formula = formula.strip()
    if not formula:
        raise ValueError("Empty formula")

    # Simple regex for element counting, works for basic formulas
    composition = {}

    # Handle parentheses recursively
    def parse_part(part, multiplier=1):
        # Match elements with optional subscripts
        i = 0
        while i < len(part):
            # Match an element (capital letter followed by optional lowercase)
            if i < len(part) and 'A' <= part[i] <= 'Z':
                # Get the element symbol
                symbol = part[i]
                i += 1
                # Check for lowercase letter
                if i < len(part) and 'a' <= part[i] <= 'z':
                    symbol += part[i]
                    i += 1

                # Check if the element is valid
                if symbol not in ELEMENTS:
                    raise ValueError(f"Unknown element symbol: {symbol}")

                # Get the subscript
                count = ""
                while i < len(part) and '0' <= part[i] <= '9':
                    count += part[i]
                    i += 1

                # Convert count to integer, default to 1 if no count
                count = int(count) if count else 1
                count *= multiplier

                # Add to composition
                composition[symbol] = composition.get(symbol, 0) + count

            # Handle parentheses
            elif i < len(part) and part[i] == '(':
                # Find the matching closing parenthesis
                paren_level = 1
                start = i + 1
                i += 1
                while i < len(part) and paren_level > 0:
                    if part[i] == '(':
                        paren_level += 1
                    elif part[i] == ')':
                        paren_level -= 1
                    i += 1

                if paren_level != 0:
                    raise ValueError("Mismatched parentheses in formula")

                # Get the subscript for the parenthesized group
                group_multiplier = ""
                while i < len(part) and '0' <= part[i] <= '9':
                    group_multiplier += part[i]
                    i += 1

                group_multiplier = int(group_multiplier) if group_multiplier else 1
                group_multiplier *= multiplier

                # Parse the contents of the parentheses
                parse_part(part[start:i-1], group_multiplier)

            else:
                # Skip any other character
                i += 1

    # Parse the entire formula
    parse_part(formula)



    return composition