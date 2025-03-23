"""
DSL/ast_nodes/visitors.py

This module defines visitor classes for traversing or transforming the AST.
For example, you can implement an evaluation visitor, a pretty-printer, or a semantic analyzer.
"""

class Visitor:
    def generic_visit(self, node):
        """
        Called if no explicit visitor function exists for a node.
        """
        for attr in dir(node):
            value = getattr(node, attr)
            if isinstance(value, list):
                for item in value:
                    if hasattr(item, "accept"):
                        item.accept(self)
            elif hasattr(value, "accept"):
                value.accept(self)
        return None

    def visit(self, node):
        return node.accept(self)


class PrettyPrintVisitor(Visitor):
    def visit_ProgramNode(self, node):
        result = ""
        for stmt in node.statements:
            result += self.visit(stmt) + "\n"
        return result

    def visit_BalanceStatementNode(self, node):
        return "Balance: " + self.visit(node.reaction_expr)

    def visit_PredictStatementNode(self, node):
        return "Predict: " + self.visit(node.reaction_expr)

    def visit_ReactionExpressionNode(self, node):
        reactants = " + ".join(self.visit(term) for term in node.reactants)
        products = " + ".join(self.visit(term) for term in node.products)
        return f"{reactants} -> {products}"

    def visit_ChemicalTermNode(self, node):
        coeff = str(node.coefficient) if node.coefficient != 1 else ""
        return coeff + self.visit(node.molecule)

    def visit_MoleculeNode(self, node):
        elems = "".join(self.visit(elem) for elem in node.elements)
        if node.multiplier != 1:
            return f"({elems}){node.multiplier}"
        return elems

    def visit_ElementGroupNode(self, node):
        return f"{node.symbol}{node.count if node.count != 1 else ''}"

    def visit_ConditionNode(self, node):
        if node.operator:
            return f"{self.visit(node.left)} {node.operator} {self.visit(node.right)}"
        return f"{node.condition_type}({node.value})"

    def visit_ConditionalReactionNode(self, node):
        return f"ConditionalReactionNode(reactants={node.reactants}, products={node.products}, condition={self.visit(node.condition)})"
