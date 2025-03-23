"""
DSL/interpreter/evaluator.py

Implements the Evaluator that traverses the AST and executes the ChemDSL program.
"""

from DSL.ast_nodes import nodes
from DSL.chemistry import balancer, reactions, compounds, ELEMENTS
from DSL.chemistry.elements import COMPOUNDS
from DSL.interpreter.enviroment_dsl import Environment
from DSL.utils.error_handler import ErrorHandler

class Evaluator:
    def __init__(self):
        self.env = Environment()
        from DSL.utils.error_handler import ErrorHandler
        self.error_handler = ErrorHandler()

    def evaluate(self, node):
        try:
            # Check if node is None before proceeding
            if node is None:
                return None

            method_name = 'eval_' + node.__class__.__name__
            evaluator = getattr(self, method_name, self.generic_eval)
            return evaluator(node)
        except Exception as e:
            # Use the updated error handler
            self.error_handler.add_error(str(e))
            return f"Evaluation error: {str(e)}"

    def generic_eval(self, node):
        raise Exception(f"No eval method for {node.__class__.__name__}")

    def eval_ProgramNode(self, node):
        results = []
        for stmt in node.statements:
            result = self.evaluate(stmt)
            if result is not None:
                results.append(result)
        return "\n".join(str(r) for r in results)

    # In evaluator_dsl.py
    def format_formula(self, formula: str) -> str:
        """Convert formulas like 'CuN2O6' to 'Cu(NO3)2'."""
        from collections import defaultdict
        import re

        # Split formula into elements and counts (e.g., [('Cu', 1), ('N', 2), ('O', 6)])
        elements = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
        elements = [(elem, int(count) if count else 1) for elem, count in elements]

        # Find the greatest common divisor (GCD) of counts
        counts = [count for _, count in elements[1:]]  # Skip the first element (e.g., Cu)
        if not counts:
            return formula

        from math import gcd
        common_divisor = counts[0]
        for count in counts[1:]:
            common_divisor = gcd(common_divisor, count)

        # If a common divisor exists, format as a subgroup
        if common_divisor > 1:
            subgroup = "".join([f"{elem}{count // common_divisor}" for elem, count in elements[1:]])
            return f"{elements[0][0]}({subgroup}){common_divisor}"
        return formula

    def eval_BalanceStatementNode(self, node):
        try:
            reaction = self.eval_ReactionExpressionNode(node.reaction_expr)
            reactants = [(coeff, compound) for coeff, compound in reaction.reactants]
            products = [(coeff, compound) for coeff, compound in reaction.products]
            coeffs = balancer.balance_reaction(reactants, products)
            if not coeffs:
                return "Could not balance reaction."

            # Format formulas with parentheses
            balanced_reactants = []
            for i, (orig_coeff, compound) in enumerate(reactants):
                new_coeff = coeffs[i] * orig_coeff
                formula = self.format_formula(compound.formula)  # Apply formatting
                balanced_reactants.append(f"{new_coeff if new_coeff != 1 else ''}{formula}")

            balanced_products = []
            for j, (orig_coeff, compound) in enumerate(products):
                new_coeff = coeffs[len(reactants) + j] * orig_coeff
                formula = self.format_formula(compound.formula)  # Apply formatting
                balanced_products.append(f"{new_coeff if new_coeff != 1 else ''}{formula}")

            return f"Balanced Reaction: {' + '.join(balanced_reactants)} → {' + '.join(balanced_products)}"

        except Exception as e:
            self.error_handler.add_error(f"Balance error: {str(e)}")
            return f"Balance failed: {str(e)}"

    def eval_PredictStatementNode(self, node):
        print("\n=== EVALUATION ===")
        print("Evaluating PredictStatementNode")
        print(f"Raw reactants: {node.reaction_expr.reactants}")
        try:
            # Evaluate the reaction expression to get reactants
            reaction_expr = self.eval_ReactionExpressionNode(node.reaction_expr)

            # Extract compounds from reactants (ignoring coefficients)
            reactant_compounds = [r[1] for r in reaction_expr.reactants]

            # Try to predict the products
            predicted_reaction = reactions.predict_reaction(reactant_compounds)

            if predicted_reaction:
                # Store the predicted reaction in the environment for later reference
                reaction_str = str(predicted_reaction)
                self.env.define('last_predicted_reaction', reaction_str)

                return f"Predicted Reaction: {reaction_str}"
            else:
                return "Could not predict reaction products."

        except Exception as e:
            self.error_handler.add_error(f"Prediction error: {str(e)}")
            return f"Prediction Error: {str(e)}"

    def eval_AnalyzeStatementNode(self, node):
        try:
            compound = self.evaluate(node.target)
            formula = compound.formula
            composition = compound.composition
            elements = composition.keys()

            if len(elements) == 1:
                # Element analysis
                element_symbol = list(elements)[0]
                element_data = ELEMENTS.get(element_symbol)
                if not element_data:
                    raise ValueError(f"Element '{element_symbol}' not found.")

                result = {
                    'is_analysis_result': True,
                    'element': element_symbol,
                    'name': element_data['name'],
                    'atomic_weight': element_data['atomic_weight'],
                    'state': element_data['state'],
                    'group': element_data.get('group', 'N/A'),
                    'electronegativity': element_data.get('electronegativity', 'N/A'),
                    'common_compounds': element_data.get('common_compounds', []),
                    'common_reactions': element_data.get('common_reactions', []),
                    'detail_level': node.detail_level
                }
            else:
                # Compound analysis
                molar_mass = compound.molar_mass()
                result = {
                    'is_analysis_result': True,
                    'compound': formula,
                    'molar_mass': molar_mass,
                    'composition': composition,
                    'detail_level': node.detail_level
                }

                # Add additional compound information if available
                if formula in COMPOUNDS:
                    compound_data = COMPOUNDS[formula]
                    # Only add detailed info if detail_level is 'all'
                    if node.detail_level == 'all':
                        result.update({
                            'name': compound_data['name'],
                            'state': compound_data['state'],
                            'classification': compound_data['classification'],
                            'density': compound_data['density'],
                            'melting_point': compound_data['melting_point'],
                            'boiling_point': compound_data['boiling_point'],
                            'solubility': compound_data['solubility'],
                            'acidity': compound_data['acidity'],
                            'common_uses': compound_data['common_uses'],
                            'hazards': compound_data['hazards']
                        })
                    # Always add name and basic info even for basic detail level
                    else:
                        result.update({
                            'name': compound_data['name'],
                            'state': compound_data['state'],
                            'classification': compound_data['classification']
                        })

            return result
        except Exception as e:
            self.error_handler.add_error(f"Analysis error: {str(e)}")
            return f"Analysis Error: {str(e)}"

    def eval_ReactionTypeNode(self, node):
        """Evaluate a reaction type statement."""
        reaction_type = node.reaction_type
        target = node.target

        # Define common examples for each reaction type
        common_examples = {
            'COMBUSTION': {
                'syntax': 'Fuel + O2 -> CO2 + H2O',
                'example': 'CH4 + 2O2 -> CO2 + 2H2O'
            },
            'DECOMPOSITION': {
                'syntax': 'Compound -> Simpler Compounds',
                'example': '2H2O -> 2H2 + O2'
            },
            'SINGLE_REPLACEMENT': {
                'syntax': 'A + BC -> AC + B',
                'example': 'Zn + 2HCl -> ZnCl2 + H2'
            },
            'DOUBLE_REPLACEMENT': {
                'syntax': 'AB + CD -> AD + CB',
                'example': 'AgNO3 + NaCl -> AgCl + NaNO3'
            },
            'ACID_BASE': {
                'syntax': 'Acid + Base -> Salt + Water',
                'example': 'HCl + NaOH -> NaCl + H2O'
            },
            'PRECIPITATION': {
                'syntax': 'Aqueous Solutions -> Solid Precipitate',
                'example': 'Pb(NO3)2 + 2KI -> PbI2 + 2KNO3'
            },
            'GAS_FORMATION': {
                'syntax': 'Reactants -> Gas + Other Products',
                'example': '2HCl + Na2CO3 -> 2NaCl + H2O + CO2'
            }
        }

        # If no target is provided, return the syntax and common example
        if not target:
            if reaction_type in common_examples:
                return f"Reaction Type: {reaction_type}\nSyntax: {common_examples[reaction_type]['syntax']}\nExample: {common_examples[reaction_type]['example']}"
            else:
                return f"Unknown reaction type: {reaction_type}"

        # If a target is provided, try to find an example with that target
        target_formula = self.evaluate(target).formula
        if reaction_type == 'COMBUSTION' and target_formula == 'CH4':
            return "Example with CH4: CH4 + 2O2 -> CO2 + 2H2O"
        elif reaction_type == 'DECOMPOSITION' and target_formula == 'H2O':
            return "Example with H2O: 2H2O -> 2H2 + O2"
        elif reaction_type == 'SINGLE_REPLACEMENT' and target_formula == 'Zn':
            return "Example with Zn: Zn + 2HCl -> ZnCl2 + H2"
        elif reaction_type == 'DOUBLE_REPLACEMENT' and target_formula == 'AgNO3':
            return "Example with AgNO3: AgNO3 + NaCl -> AgCl + NaNO3"
        elif reaction_type == 'ACID_BASE' and target_formula == 'HCl':
            return "Example with HCl: HCl + NaOH -> NaCl + H2O"
        elif reaction_type == 'PRECIPITATION' and target_formula == 'Pb(NO3)2':
            return "Example with Pb(NO3)2: Pb(NO3)2 + 2KI -> PbI2 + 2KNO3"
        elif reaction_type == 'GAS_FORMATION' and target_formula == 'Na2CO3':
            return "Example with Na2CO3: 2HCl + Na2CO3 -> 2NaCl + H2O + CO2"
        else:
            return f"No specific example found for {reaction_type} with {target_formula}. Here's a common example:\n{common_examples[reaction_type]['example']}"

    def eval_ReactionExpressionNode(self, node):
        # Evaluate each term in reactants and products
        reactants = [self.evaluate(term) for term in node.reactants]

        # Products may be empty in a prediction statement
        products = []
        if node.products:
            products = [self.evaluate(term) for term in node.products]

        # Create a reaction object
        class ReactionWrapper:
            def __init__(self, reactants, products):
                self.reactants = reactants
                self.products = products

            def __str__(self):
                reactants_str = " + ".join(f"{c if c != 1 else ''}{cpd.formula}"
                                          for c, cpd in self.reactants)
                products_str = " + ".join(f"{c if c != 1 else ''}{cpd.formula}"
                                         for c, cpd in self.products)
                return f"{reactants_str} -> {products_str}"

        return ReactionWrapper(reactants, products)

    def eval_ThermodynamicNode(self, node):
        """Evaluate a thermodynamic property statement."""
        reaction = self.eval_ReactionExpressionNode(node.reaction_expr)
        reaction_str = str(reaction)  # Get the reaction as a string

        # Define thermodynamic data (for demonstration purposes)
        thermodynamic_data = {
            'ENTHALPY': {
                'H2 + O2 -> H2O': '-285.8 kJ/mol',
                'CH4 + 2O2 -> CO2 + 2H2O': '-890.4 kJ/mol',
                '2H2 + O2 -> 2H2O': '-571.6 kJ/mol',
                'N2 + 3H2 -> 2NH3': '-92.4 kJ/mol',
            },
            'ENTROPY': {
                'H2 + O2 -> H2O': '-163.2 J/(mol·K)',
                'CH4 + 2O2 -> CO2 + 2H2O': '-242.8 J/(mol·K)',
                '2H2 + O2 -> 2H2O': '-326.4 J/(mol·K)',
                'N2 + 3H2 -> 2NH3': '-198.3 J/(mol·K)',
            },
            'GIBBS_ENERGY': {
                'H2 + O2 -> H2O': '-237.1 kJ/mol',
                'CH4 + 2O2 -> CO2 + 2H2O': '-818.3 kJ/mol',
                '2H2 + O2 -> 2H2O': '-474.2 kJ/mol',
                'N2 + 3H2 -> 2NH3': '-33.3 kJ/mol',
            },
            'EQUILIBRIUM': {
                'H2 + O2 -> H2O': '1.0e+40',
                'CH4 + 2O2 -> CO2 + 2H2O': '1.0e+30',
                '2H2 + O2 -> 2H2O': '1.0e+40',
                'N2 + 3H2 -> 2NH3': '1.0e+5',
            }
        }

        # Define explanations for reactions
        reaction_explanations = {
            'H2 + O2 -> H2O': (
                "This is the combustion of hydrogen gas (H2) with oxygen gas (O2) to form water (H2O). "
                "It is a highly exothermic reaction, releasing a large amount of energy."
            ),
            'CH4 + 2O2 -> CO2 + 2H2O': (
                "This is the combustion of methane (CH4) with oxygen gas (O2) to form carbon dioxide (CO2) and water (H2O). "
                "It is a common reaction in natural gas combustion."
            ),
            '2H2 + O2 -> 2H2O': (
                "This is the balanced combustion of hydrogen gas (H2) with oxygen gas (O2) to form water (H2O). "
                "It releases twice the energy of the single-molecule reaction."
            ),
            'N2 + 3H2 -> 2NH3': (
                "This is the Haber process, where nitrogen gas (N2) reacts with hydrogen gas (H2) to form ammonia (NH3). "
                "It is a key reaction in fertilizer production."
            )
        }

        # Get the property type (e.g., 'ENTHALPY', 'ENTROPY')
        property_type = node.property_type

        if node.info:
            # Display explanation of the reaction
            if reaction_str in reaction_explanations:
                return f"Explanation for {reaction_str}:\n{reaction_explanations[reaction_str]}"
            else:
                return f"No explanation available for {reaction_str}."
        else:
            # Display thermodynamic property
            if reaction_str in thermodynamic_data[property_type]:
                value = thermodynamic_data[property_type][reaction_str]
                return f"{property_type.capitalize()} for {reaction_str}: {value}"
            else:
                return f"No thermodynamic data available for {reaction_str}."

    def eval_ChemicalAnalysisNode(self, node):
        """Evaluate a chemical analysis statement."""
        target = self.evaluate(node.target)  # Evaluate the target (compound or reaction)
        analysis_type = node.analysis_type  # e.g., 'OXIDATION_STATES', 'MOLAR_MASS'

        if analysis_type == 'OXIDATION_STATES':
            # Calculate oxidation states for a compound
            if isinstance(target, compounds.Compound):
                oxidation_states = self.calculate_oxidation_states(target)
                return f"Oxidation States in {target.formula}: {oxidation_states}"
            else:
                return f"Oxidation states can only be calculated for compounds."

        elif analysis_type == 'LIMITING_REAGENT':
            # Calculate the limiting reagent in a reaction
            if hasattr(target, 'reactants'):  # Check if target is a ReactionWrapper
                limiting_reagent = self.calculate_limiting_reagent(target)
                return f"Limiting Reagent in {str(target)}: {limiting_reagent}"
            else:
                return f"Limiting reagent can only be calculated for reactions."

        elif analysis_type == 'PERCENT_YIELD':
            # Calculate the percent yield of a reaction
            if hasattr(target, 'reactants'):  # Check if target is a ReactionWrapper
                percent_yield = self.calculate_percent_yield(target)
                return f"Percent Yield of {str(target)}: {percent_yield}%"
            else:
                return f"Percent yield can only be calculated for reactions."

        elif analysis_type == 'EMPIRICAL_FORMULA':
            # Calculate the empirical formula of a compound
            if isinstance(target, compounds.Compound):
                empirical_formula = self.calculate_empirical_formula(target)
                return f"Empirical Formula of {target.formula}: {empirical_formula}"
            else:
                return f"Empirical formula can only be calculated for compounds."

        elif analysis_type == 'MOLECULAR_FORMULA':
            # Display the molecular formula of a compound
            if isinstance(target, compounds.Compound):
                return f"Molecular Formula of {target.formula}: {target.formula}"
            else:
                return f"Molecular formula can only be displayed for compounds."

        elif analysis_type == 'MOLAR_MASS':
            # Calculate the molar mass of a compound
            if isinstance(target, compounds.Compound):
                molar_mass = target.molar_mass()
                return f"Molar Mass of {target.formula}: {molar_mass:.2f} g/mol"
            else:
                return f"Molar mass can only be calculated for compounds."

        else:
            return f"Unknown analysis type: {analysis_type}"

    def calculate_oxidation_states(self, compound):
        """Calculate oxidation states for a compound."""
        # Example implementation (simplified)
        oxidation_states = {}
        for element, count in compound.composition.items():
            if element == 'H':
                oxidation_states[element] = +1
            elif element == 'O':
                oxidation_states[element] = -2
            else:
                oxidation_states[element] = 0  # Default to 0 for simplicity
        return oxidation_states

    def calculate_limiting_reagent(self, reaction):
        """Calculate the limiting reagent in a reaction."""
        # Extract reactants and their coefficients
        reactants = reaction.reactants
        if not reactants:
            return "No reactants found."

        # For simplicity, assume the first reactant is the limiting reagent
        # In a real implementation, you would compare mole ratios
        limiting_reagent = reactants[0][1].formula
        return limiting_reagent

    def calculate_percent_yield(self, reaction):
        """Calculate the percent yield of a reaction."""
        # For demonstration, return a fixed value
        return 95.0  # Default to 95% for demonstration

    def calculate_empirical_formula(self, compound):
        """Calculate the empirical formula of a compound."""
        elements = compound.composition
        counts = list(elements.values())
        gcd = self.find_gcd(counts)

        empirical_formula = ""
        for element, count in elements.items():
            empirical_formula += f"{element}{count // gcd}"
        return empirical_formula

    def find_gcd(self, numbers):
        """Find the greatest common divisor (GCD) of a list of numbers."""
        from math import gcd
        result = numbers[0]
        for num in numbers[1:]:
            result = gcd(result, num)
        return result

    def eval_ChemicalTermNode(self, node):
        # Evaluate the molecule to get a Compound object
        compound = self.evaluate(node.molecule)
        # Return a tuple (coefficient, compound)
        return (node.coefficient, compound)

    def eval_MoleculeNode(self, node):
        # For evaluation, convert molecule AST node to a compound (using its string formula)
        formula = ""
        for elem in node.elements:
            formula += self.evaluate(elem)

        # If there is a multiplier, apply it
        if node.multiplier != 1:
            formula = f"({formula}){node.multiplier}"

        # Create a Compound object
        try:
            return compounds.Compound(formula)
        except ValueError as e:
            self.error_handler.add_error(f"Invalid molecule: {formula}. {str(e)}")
            raise

    def eval_ElementGroupNode(self, node):
        # Check if element exists in the periodic table
        if node.symbol not in compounds.ELEMENTS:
            self.error_handler.add_error(f"Unknown element symbol: {node.symbol}")

        # Return element symbol with count
        return f"{node.symbol}{node.count if node.count != 1 else ''}"


