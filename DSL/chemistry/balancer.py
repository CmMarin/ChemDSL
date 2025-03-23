"""
DSL/chemistry/balancer.py

Provides a simple algorithm to balance chemical reactions.
For demonstration purposes, this implementation uses a brute-force search.
In production, you might use linear algebra or other methods.
"""

import itertools
import math
from DSL.chemistry.compounds import parse_formula


def find_gcd(numbers):
    """
    Find the greatest common divisor of a list of numbers.
    """
    result = numbers[0]
    for num in numbers[1:]:
        result = math.gcd(result, num)
    return result


def is_balanced(reactants, products, coeffs):
    """
    Check if reaction is balanced given lists of (coefficient, formula) and a coefficient vector.
    reactants and products are lists of tuples: (coefficient, compound)
    coeffs: tuple of integers, first part for reactants, second for products.
    """
    element_set = set()
    # Extract all elements from both sides of the reaction
    for _, compound in reactants + products:
        # Ensure we're accessing the formula attribute correctly
        if hasattr(compound, 'formula'):
            formula = compound.formula
        else:
            formula = compound

        # Parse the formula to get elements
        parsed_formula = parse_formula(formula)
        element_set.update(parsed_formula.keys())

    # Check if each element is balanced on both sides
    for element in element_set:
        # Sum the count of each element on the reactant side
        left = 0
        for i, (orig_coeff, compound) in enumerate(reactants):
            if hasattr(compound, 'formula'):
                formula = compound.formula
            else:
                formula = compound

            parsed_formula = parse_formula(formula)
            element_count = parsed_formula.get(element, 0)
            left += coeffs[i] * element_count * orig_coeff

        # Sum the count of each element on the product side
        right = 0
        for j, (orig_coeff, compound) in enumerate(products):
            if hasattr(compound, 'formula'):
                formula = compound.formula
            else:
                formula = compound

            parsed_formula = parse_formula(formula)
            element_count = parsed_formula.get(element, 0)
            right += coeffs[len(reactants) + j] * element_count * orig_coeff

        if left != right:
            return False
    return True


def balance_reaction(reactants, products, max_coeff=20):
    n = len(reactants)
    m = len(products)
    total = n + m

    for coeffs in itertools.product(range(1, max_coeff + 1), repeat=total):

        if is_balanced(reactants, products, coeffs):
            gcd = find_gcd(coeffs)
            return tuple(c // gcd for c in coeffs)

    return None