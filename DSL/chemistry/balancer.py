"""
DSL/chemistry/balancer.py

Provides a simple algorithm to balance chemical reactions.
For demonstration purposes, this implementation uses a brute-force search.
In production, you might use linear algebra or other methods.
"""

import itertools
from DSL.chemistry.compounds import parse_formula


def is_balanced(reactants, products, coeffs):
    """
    Check if reaction is balanced given lists of (coefficient, formula) and a coefficient vector.
    reactants and products are lists of tuples: (coefficient, compound)
    coeffs: tuple of integers, first part for reactants, second for products.
    """
    element_set = set()
    # Extract all elements from both sides of the reaction
    for _, compound in reactants + products:
        # Ensure we're using the formula attribute if compound is a Compound object
        formula = compound.formula if hasattr(compound, 'formula') else compound
        element_set.update(parse_formula(formula).keys())

    # Check if each element is balanced on both sides
    for element in element_set:
        # Sum the count of each element on the reactant side
        left = sum(coeffs[i] * parse_formula(reactants[i][1].formula).get(element, 0) * reactants[i][0]
                   for i in range(len(reactants)))
        # Sum the count of each element on the product side
        right = sum(coeffs[len(reactants) + j] * parse_formula(products[j][1].formula).get(element, 0) * products[j][0]
                    for j in range(len(products)))

        if left != right:
            return False
    return True

def balance_reaction(reactants, products, max_coeff=10):
    """
    reactants and products: lists of tuples (coefficient, Compound) where Compound has a .formula attribute.
    Returns the balanced coefficients if found.
    """
    n = len(reactants)
    m = len(products)
    total = n + m

    # Start with the simplest coefficients
    for coeffs in itertools.product(range(1, max_coeff+1), repeat=total):
        if coeffs[0] != 1:  # Convention: first coefficient should be 1
            continue

        if is_balanced(reactants, products, coeffs):
            # Reduce to smallest whole-number coefficient set
            gcd = find_gcd(coeffs)
            if gcd > 1:
                return tuple(c // gcd for c in coeffs)
            return coeffs

    return None

def find_gcd(numbers):
    """Find the greatest common divisor of a list of numbers."""
    from math import gcd
    from functools import reduce

    def gcd_pair(a, b):
        while b:
            a, b = b, a % b
        return a

    return reduce(gcd_pair, numbers)