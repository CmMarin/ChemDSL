"""
DSL/semantic/type_checker.py

Implements type checking and semantic analysis for ChemDSL.
"""

from DSL.semantic.symbol_table import SymbolTable
from DSL.ast_nodes import nodes

class TypeChecker:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def check(self, ast):
        # Walk the AST and perform type checking.
        # For example, check that chemical expressions have proper structure.
        self.visit(ast)

    def visit(self, node):
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        # Default visit method
        for attr in dir(node):
            value = getattr(node, attr)
            if isinstance(value, list):
                for item in value:
                    if hasattr(item, "accept"):
                        self.visit(item)
            elif hasattr(value, "accept"):
                self.visit(value)

    def visit_ProgramNode(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_BalanceStatementNode(self, node):
        # Add type checking for balance statements (e.g., check reaction format)
        self.visit(node.reaction_expr)

    def visit_PredictStatementNode(self, node):
        self.visit(node.reaction_expr)

    def visit_ReactionExpressionNode(self, node):
        # Check reactants and products (for instance, non-empty lists)
        if not node.reactants or not node.products:
            raise Exception("A reaction must have both reactants and products.")
        for term in node.reactants + node.products:
            self.visit(term)

    def visit_ChemicalTermNode(self, node):
        # Could check that coefficient is positive, etc.
        if node.coefficient <= 0:
            raise Exception("Coefficient must be a positive integer.")
        self.visit(node.molecule)

    def visit_MoleculeNode(self, node):
        if not node.elements:
            raise Exception("Molecule must contain at least one element.")
        for elem in node.elements:
            self.visit(elem)

    def visit_ElementGroupNode(self, node):
        # Here, you might check that the element symbol is valid.
        # For simplicity, assume lexer has done basic validation.
        pass
