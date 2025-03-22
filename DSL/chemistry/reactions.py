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
            metal = base_formula.split("OH")[0]
            nonmetal = acid_formula[1:]
            salt = Compound(f"{metal}{nonmetal}")
            water = Compound("H2O")

            # Balance the reaction (e.g., 1 Ca(OH)2 + 2 HCl → 1 CaCl2 + 2 H2O)
            acid_coeff = 2 if base.formula.count("OH") > 1 else 1  # Handle bases like Ca(OH)2
            return Reaction(
                reactants=[(acid_coeff, acid), (1, base)],
                products=[(1, salt), (acid_coeff, water)]  # Match coefficients
            )

    # 3. Metal + Oxygen -> Metal oxide
    if _contains_metal_and_oxygen(reactants):
        metal, oxygen = _get_metal_and_oxygen(reactants)
        metal_oxide = Compound(f"{metal.formula}O")
        # Balance the reaction: 2Mg + O2 → 2MgO
        return Reaction(
            reactants=[(2, metal), (1, oxygen)],  # Changed coefficients
            products=[(2, metal_oxide)]  # Changed coefficients
        )

    # 3.1 Decomposition of water
    if len(reactants) == 1 and reactants[0].formula == "H2O":
        H2 = Compound("H2")
        O2 = Compound("O2")
        return Reaction(
            reactants=[(2, reactants[0])],  # 2H2O
            products=[(2, H2), (1, O2)]  # → 2H2 + O2
        )

    # 4. Simple synthesis reaction: A + B -> AB
    #    Validated Synthesis Reactions
    if len(reactants) == 2:
        # Check if both reactants are elements (e.g., Na + Cl)
        if all(len(parse_formula(r.formula)) == 1 for r in reactants):
            elem1 = list(parse_formula(reactants[0].formula).keys())[0]  # e.g., "Na"
            elem2 = list(parse_formula(reactants[1].formula).keys())[0]  # e.g., "Cl"

            # Get valencies from a predefined dictionary (add this to elements.py)
            valency = {
                'Na': +1, 'K': +1, 'Mg': +2, 'Al': +3,
                'Cl': -1, 'O': -2, 'S': -2, 'N': -3
            }

            # Determine formula based on valency (e.g., Na+ + Cl- → NaCl)
            if elem1 in valency and elem2 in valency:
                ratio = (abs(valency[elem2]), abs(valency[elem1]))  # Simplify ratio
                formula = f"{elem1}{ratio[0]}{elem2}{ratio[1]}" if ratio != (1, 1) else f"{elem1}{elem2}"
                try:
                    product = Compound(formula)
                    return Reaction(reactants=[(1, reactants[0]), (1, reactants[1])],
                                    products=[(1, product)])
                except ValueError:
                    pass  # Fall through to other reaction types

        # If not elements, check for valid compound combinations
    REACTIVITY_SERIES = ["K", "Na", "Li", "Ca", "Mg", "Al", "Zn", "Fe", "Pb", "Cu", "Ag"]
    # 5. Metal oxide reduction with H2
    def _is_metal(formula: str) -> bool:
        """Check if the formula represents a pure metal (e.g., "Cu", "Zn")"""
        return formula in REACTIVITY_SERIES

    if len(reactants) == 2:
        # Check if one reactant is a metal and the other is a compound
        metal = None
        compound = None
        for r in reactants:
            if _is_metal(r.formula):  # Helper function to check if formula is a pure metal
                metal = r
            else:
                compound = r

        if metal and compound:
            # Extract metal from compound (e.g., "Cu" from "CuSO4")
            compound_elements = parse_formula(compound.formula)
            displaced_metal = next((elem for elem in compound_elements if _is_metal(elem)), None)

            # Check reactivity
            if displaced_metal and REACTIVITY_SERIES.index(metal.formula) < REACTIVITY_SERIES.index(displaced_metal):
                # Create new compound (e.g., ZnSO4)
                new_compound_formula = compound.formula.replace(displaced_metal, metal.formula)
                try:
                    new_compound = Compound(new_compound_formula)
                    displaced = Compound(displaced_metal)
                    return Reaction(
                        reactants=[(1, metal), (1, compound)],
                        products=[(1, new_compound), (1, displaced)]
                    )
                except ValueError:
                    pass
    # 6. Acid + Carbonate → Salt + CO2 + H2O
    if len(reactants) == 2:
        # Find acid (starts with H) and carbonate (ends with CO3)
        acid = next((r for r in reactants if r.formula.startswith("H")), None)
        carbonate = next((r for r in reactants if "CO3" in r.formula), None)

        if acid and carbonate:
            # Extract metal from carbonate (e.g., "Ca" from "CaCO3")
            metal = carbonate.formula.split("CO3")[0]
            salt = Compound(f"{metal}Cl")  # Assumes acid is HCl (generalize if needed)
            return Reaction(
                reactants=[(1, acid), (1, carbonate)],
                products=[(1, salt), (1, Compound("CO2")), (1, Compound("H2O"))]
            )

    # 7. Ammonia Combustion: 4NH3 + 5O2 → 4NO + 6H2O
    if _contains_compounds(reactants, ["NH3", "O2"]):
        NH3 = _find_compound(reactants, "NH3")
        O2 = _find_compound(reactants, "O2")
        return Reaction(
            reactants=[(4, NH3), (5, O2)],
            products=[(4, Compound("NO")), (6, Compound("H2O"))]
        )

    # 8. Active Metal + Water → Metal Hydroxide + H2
    if len(reactants) == 2 and any(r.formula == "H2O" for r in reactants):
        metal = next((r for r in reactants if _is_metal(r.formula)), None)
        if metal and metal.formula in ["Na", "K", "Ca"]:  # Highly reactive metals
            hydroxide = Compound(f"{metal.formula}OH")
            return Reaction(
                reactants=[(2, metal), (2, Compound("H2O"))],
                products=[(2, hydroxide), (1, Compound("H2"))]
            )


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