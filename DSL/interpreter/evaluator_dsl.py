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
        self.error_handler = ErrorHandler()

    def evaluate(self, node):
        try:
            method_name = 'eval_' + node.__class__.__name__
            evaluator = getattr(self, method_name, self.generic_eval)
            return evaluator(node)
        except Exception as e:
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

    def eval_BalanceStatementNode(self, node):
        try:
            # Evaluate the reaction expression to get reactants and products
            reaction = self.eval_ReactionExpressionNode(node.reaction_expr)

            # Use the balancer to compute coefficients
            coeffs = balancer.balance_reaction(reaction.reactants, reaction.products)

            if coeffs is None:
                return "Could not balance reaction. The reaction may be invalid or too complex."

            # Construct a balanced reaction string
            n_reactants = len(reaction.reactants)
            balanced_reactants = []
            balanced_products = []

            for i, (orig_coeff, compound) in enumerate(reaction.reactants):
                new_coeff = coeffs[i] * orig_coeff
                if new_coeff == 1:
                    balanced_reactants.append(f"{compound.formula}")
                else:
                    balanced_reactants.append(f"{new_coeff}{compound.formula}")

            for j, (orig_coeff, compound) in enumerate(reaction.products):
                new_coeff = coeffs[n_reactants + j] * orig_coeff
                if new_coeff == 1:
                    balanced_products.append(f"{compound.formula}")
                else:
                    balanced_products.append(f"{new_coeff}{compound.formula}")

            reactants_str = " + ".join(balanced_reactants)
            products_str = " + ".join(balanced_products)

            return f"Balanced Reaction: {reactants_str} -> {products_str}"

        except Exception as e:
            self.error_handler.add_error(f"Balance error: {str(e)}")
            return f"Could not balance reaction: {str(e)}"

    def eval_PredictStatementNode(self, node):
        try:
            # Evaluate the reaction expression to get reactants
            reaction = self.eval_ReactionExpressionNode(node.reaction_expr)

            # Extract compounds from reactants (ignoring coefficients)
            reactant_compounds = [r[1] for r in reaction.reactants]

            # Try to predict the products
            predicted = reactions.predict_reaction(reactant_compounds)

            if predicted:
                return f"Predicted Reaction: {predicted}"
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
