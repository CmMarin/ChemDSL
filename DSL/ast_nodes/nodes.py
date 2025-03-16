"""
DSL/ast_nodes/nodes.py
AST node definitions for ChemDSL.
"""

class Node:
    def accept(self, visitor):
        method_name = 'visit_' + self.__class__.__name__
        visitor_method = getattr(visitor, method_name, visitor.generic_visit)
        return visitor_method(self)


class ProgramNode(Node):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"ProgramNode(statements={self.statements})"


class BalanceStatementNode(Node):
    def __init__(self, reaction_expr):
        self.reaction_expr = reaction_expr

    def __repr__(self):
        return f"BalanceStatementNode({self.reaction_expr})"


class PredictStatementNode(Node):
    def __init__(self, reaction_expr):
        self.reaction_expr = reaction_expr

    def __repr__(self):
        return f"PredictStatementNode({self.reaction_expr})"


class ReactionExpressionNode(Node):
    def __init__(self, reactants, products):
        self.reactants = reactants  # list of ChemicalTermNode
        self.products = products    # list of ChemicalTermNode

    def __repr__(self):
        return f"ReactionExpressionNode(reactants={self.reactants}, products={self.products})"


class ChemicalTermNode(Node):
    def __init__(self, coefficient, molecule):
        self.coefficient = coefficient
        self.molecule = molecule  # MoleculeNode

    def __repr__(self):
        return f"ChemicalTermNode({self.coefficient} * {self.molecule})"


class MoleculeNode(Node):
    def __init__(self, elements, multiplier=1):
        # elements is a list of ElementGroupNode
        self.elements = elements
        self.multiplier = multiplier

    def __repr__(self):
        return f"MoleculeNode(elements={self.elements}, multiplier={self.multiplier})"


class ElementGroupNode(Node):
    def __init__(self, symbol, count):
        self.symbol = symbol
        self.count = count

    def __repr__(self):
        return f"ElementGroupNode(symbol='{self.symbol}', count={self.count})"
