"""
DSL/chemistry/reactions.py

Defines the Reaction class and functions for predicting reactions.
"""

from DSL.chemistry.compounds import Compound, parse_formula

class Reaction:
    def __init__(self, reactants: list, products: list):
        # Each of reactants and products is a tuple (coefficient, compound)
        self.reactants = reactants
        self.products = products

    def __repr__(self):
        reactants_str = " + ".join(f"{coeff if coeff > 1 else ''}{comp.formula}"
                                   for coeff, comp in self.reactants)
        products_str = " + ".join(f"{coeff if coeff > 1 else ''}{comp.formula}"
                                  for coeff, comp in self.products)
        return f"{reactants_str} -> {products_str}"

    def is_balanced(self):
        """Check if the reaction is balanced."""
        # Get all elements involved in the reaction
        elements = set()
        for _, comp in self.reactants + self.products:
            elements.update(parse_formula(comp.formula).keys())

        # For each element, check if it's balanced
        for element in elements:
            left_count = sum(coeff * parse_formula(comp.formula).get(element, 0)
                             for coeff, comp in self.reactants)
            right_count = sum(coeff * parse_formula(comp.formula).get(element, 0)
                              for coeff, comp in self.products)

            if left_count != right_count:
                return False

        return True

def predict_reaction(reactants: list):
    """
    Predicts the product for a given reaction.
    Handles several reaction types including:
    - Hydrogen combustion
    - Metal oxide formation
    - Acids and bases
    - Simple synthesis reactions
    """
    # Check for specific reaction patterns and handle them

    # 1. Hydrogen combustion: 2H2 + O2 -> 2H2O
    if _contains_compounds(reactants, ["H2", "O2"]):
        H2 = _find_compound(reactants, "H2")
        O2 = _find_compound(reactants, "O2")
        H2O = Compound("H2O")
        return Reaction(reactants=[(2, H2), (1, O2)], products=[(2, H2O)])

    # 2. Simple acid-base neutralization: HCl + NaOH -> NaCl + H2O
    if _contains_acid_base_pair(reactants):
        acid, base = _get_acid_base_pair(reactants)

        # Extract elements from acid and base to predict products
        acid_formula = acid.formula
        base_formula = base.formula

        # Better handling of acid-base reactions
        if acid_formula.startswith("H") and "OH" in base_formula:
            # Get the metal part of the base (e.g., Na from NaOH)
            metal = base_formula.replace("OH", "")

            # Get the non-metal part of the acid (e.g., Cl from HCl)
            nonmetal = acid_formula[1:] if len(acid_formula) > 1 else ""

            # Create salt and water products
            salt = Compound(f"{metal}{nonmetal}")
            water = Compound("H2O")

            return Reaction(reactants=[(1, acid), (1, base)],
                           products=[(1, salt), (1, water)])

    # 3. Metal + Oxygen -> Metal oxide
    if _contains_metal_and_oxygen(reactants):
        metal, oxygen = _get_metal_and_oxygen(reactants)
        metal_formula = metal.formula

        # Create metal oxide product
        metal_oxide = Compound(f"{metal_formula}O")

        return Reaction(reactants=[(1, metal), (1, oxygen)],
                       products=[(1, metal_oxide)])

    # 4. Simple synthesis reaction: A + B -> AB
    if len(reactants) == 2:
        comp1, comp2 = reactants[0], reactants[1]
        # This is still simplified but a bit more realistic
        try:
            # Try to create a compound from the combined formulas
            product = Compound(f"{comp1.formula}{comp2.formula}")
            return Reaction(reactants=[(1, comp1), (1, comp2)], products=[(1, product)])
        except ValueError:
            # If the combined formula isn't valid, try a different approach
            try:
                # Try the other way around
                product = Compound(f"{comp2.formula}{comp1.formula}")
                return Reaction(reactants=[(1, comp1), (1, comp2)], products=[(1, product)])
            except ValueError:
                pass

    raise Exception("Reaction prediction not implemented for given reactants.")

def _contains_compounds(compounds, formulas):
    """Check if the list of compounds contains all the specified formulas."""
    return all(any(c.formula == f for c in compounds) for f in formulas)

def _find_compound(compounds, formula):
    """Find a compound with the given formula in the list."""
    for c in compounds:
        if c.formula == formula:
            return c
    return None

def _contains_acid_base_pair(compounds):
    """Check for acid-base pairs using a more robust method."""
    acids = [c for c in compounds if c.formula.startswith("H") and len(c.formula) > 1]
    bases = [c for c in compounds if "OH" in c.formula]
    return len(acids) > 0 and len(bases) > 0

def _get_acid_base_pair(compounds):
    """Find an acid-base pair in the list of compounds."""
    acid = next((c for c in compounds if c.formula.startswith("H") and len(c.formula) > 1), None)
    base = next((c for c in compounds if "OH" in c.formula), None)
    return acid, base

def _contains_metal_and_oxygen(compounds):
    """Check if the compounds contain a metal and oxygen."""
    metals = ["Li", "Na", "K", "Rb", "Cs", "Fr", "Be", "Mg", "Ca", "Sr", "Ba", "Ra",
              "Al", "Ga", "In", "Sn", "Tl", "Pb", "Fe", "Co", "Ni", "Cu", "Zn"]
    has_metal = any(c.formula in metals for c in compounds)
    has_oxygen = any(c.formula == "O2" for c in compounds)
    return has_metal and has_oxygen

def _get_metal_and_oxygen(compounds):
    """Find a metal and oxygen in the list of compounds."""
    metals = ["Li", "Na", "K", "Rb", "Cs", "Fr", "Be", "Mg", "Ca", "Sr", "Ba", "Ra",
              "Al", "Ga", "In", "Sn", "Tl", "Pb", "Fe", "Co", "Ni", "Cu", "Zn"]
    metal = next((c for c in compounds if c.formula in metals), None)
    oxygen = next((c for c in compounds if c.formula == "O2"), None)
    return metal, oxygen