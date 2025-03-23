"""
DSL/ast_nodes/nodes.py

Defines the AST nodes for the ChemDSL parser.
"""

class ASTNode:
    """Base class for all AST nodes."""
    def accept(self, visitor):
        method_name = 'visit_' + self.__class__.__name__
        visitor_method = getattr(visitor, method_name, visitor.generic_visit)
        return visitor_method(self)


class ProgramNode(ASTNode):
    """Represents a complete ChemDSL program."""
    def __init__(self, statements):
        self.statements = statements or []

    def __repr__(self):
        statements = "\n  ".join(str(stmt) for stmt in self.statements)
        return f"ProgramNode(\n  {statements}\n)"


class BalanceStatementNode(ASTNode):
    """Represents a balance statement."""
    def __init__(self, reaction_expr):
        self.reaction_expr = reaction_expr

    def __repr__(self):
        return f"BalanceStatementNode({self.reaction_expr})"


class PredictStatementNode(ASTNode):
    """Represents a predict statement."""
    def __init__(self, reaction_expr):
        self.reaction_expr = reaction_expr

    def __repr__(self):
        return f"Predict({self.reaction_expr})"

class ReactionTypeNode(ASTNode):
    """Represents a reaction type statement."""
    def __init__(self, reaction_type, target=None):
        self.reaction_type = reaction_type
        self.target = target  # Optional: specific element or compound

    def __repr__(self):
        if self.target:
            return f"ReactionTypeNode(type={self.reaction_type}, target={self.target})"
        return f"ReactionTypeNode(type={self.reaction_type})"

class ThermodynamicNode(ASTNode):
    """Represents a thermodynamic property statement."""
    def __init__(self, property_type, reaction_expr, info=False):
        self.property_type = property_type  # e.g., 'ENTHALPY', 'ENTROPY'
        self.reaction_expr = reaction_expr  # The reaction expression
        self.info = info  # Whether to display info or the property value

    def __repr__(self):
        return f"ThermodynamicNode(property_type={self.property_type}, reaction_expr={self.reaction_expr}, info={self.info})"

class ChemicalAnalysisNode(ASTNode):
    """Represents a chemical analysis statement."""
    def __init__(self, analysis_type, target):
        self.analysis_type = analysis_type  # e.g., 'OXIDATION_STATES', 'MOLAR_MASS'
        self.target = target  # The target compound or reaction

    def __repr__(self):
        return f"ChemicalAnalysisNode(analysis_type={self.analysis_type}, target={self.target})"

class ReactionExpressionNode(ASTNode):
    """Represents a chemical reaction expression (reactants -> products)."""
    def __init__(self, reactants, products):
        self.reactants = reactants or []
        self.products = products or []

    def __repr__(self):
        reactants = ", ".join(str(r) for r in self.reactants)
        products = ", ".join(str(p) for p in self.products)
        return f"ReactionExpressionNode(reactants=[{reactants}], products=[{products}])"

class ConditionNode(ASTNode):
    """Represents a condition in an IF statement."""
    def __init__(self, condition_type, value=None, left=None, right=None, operator=None):
        self.condition_type = condition_type  # e.g., 'CATALYST', 'TEMPERATURE'
        self.value = value  # e.g., 'Fe', '450C'
        self.left = left  # Left operand for logical operators
        self.right = right  # Right operand for logical operators
        self.operator = operator  # Logical operator: 'AND', 'OR'

    def __repr__(self):
        if self.operator:
            return f"ConditionNode({self.left} {self.operator} {self.right})"
        return f"ConditionNode(type={self.condition_type}, value={self.value})"

class ConditionalReactionNode(ASTNode):
    """Represents a reaction with conditional logic."""
    def __init__(self, reactants, products, condition):
        self.reactants = reactants
        self.products = products
        self.condition = condition

    def __repr__(self):
        return f"ConditionalReactionNode(reactants={self.reactants}, products={self.products}, condition={self.condition})"

class ChemicalTermNode(ASTNode):
    """Represents a chemical term (coefficient * molecule)."""
    def __init__(self, coefficient, molecule):
        self.coefficient = coefficient
        self.molecule = molecule

    def __repr__(self):
        return f"ChemicalTermNode(coefficient={self.coefficient}, molecule={self.molecule})"


class MoleculeNode(ASTNode):
    """Represents a molecule (collection of element groups)."""
    def __init__(self, elements, multiplier=1):
        self.elements = elements
        self.multiplier = multiplier

    def __repr__(self):
        elements = ", ".join(str(e) for e in self.elements)
        return f"MoleculeNode(elements=[{elements}])"


class ElementGroupNode(ASTNode):
    """Represents an element group (element symbol with optional count)."""
    def __init__(self, symbol, count=1):
        self.symbol = symbol
        self.count = count

    def __repr__(self):
        return f"ElementGroupNode(symbol='{self.symbol}', count={self.count})"

class AnalyzeStatementNode(ASTNode):
    """Represents an analyze statement."""
    def __init__(self, target, detail_level='basic'):
        self.target = target  # This is a MoleculeNode
        self.detail_level = detail_level

    def __repr__(self):
        return f"AnalyzeStatementNode(target={self.target}, detail_level={self.detail_level})"