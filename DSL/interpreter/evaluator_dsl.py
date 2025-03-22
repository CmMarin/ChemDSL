"""
DSL/interpreter/evaluator.py

Implements the Evaluator that traverses the AST and executes the ChemDSL program.
"""

from DSL.ast_nodes import nodes
from DSL.chemistry import balancer, reactions, compounds
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
