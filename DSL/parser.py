"""
DSL/parser.py
Parser for ChemDSL using PLY (Python Lex-Yacc)
"""

import ply.yacc as yacc
from DSL.lexer import tokens
from DSL.ast_nodes import nodes

# Grammar production rules

def p_program(p):
    """program : statement_list"""
    print(f"[Parser] Building ProgramNode with {len(p[1])} statements")
    p[0] = nodes.ProgramNode(p[1])

def p_statement_list(p):
    """statement_list : statement SEMICOLON statement_list
                     | statement SEMICOLON"""
    p[0] = [p[1]] + (p[3] if len(p) > 3 else [])

def p_statement(p):
    """statement : balance_statement
                 | predict_statement
                 | analyze_statement
                 | reaction_type_statement
                 | thermodynamic_statement
                 | chemical_analysis_statement"""
    p[0] = p[1]


def p_balance_statement(p):
    """balance_statement : BALANCE reaction_expr"""
    print(f"[Parser] Building BalanceStatementNode")
    p[0] = nodes.BalanceStatementNode(p[2])

def p_predict_statement(p):
    """predict_statement : PREDICT reaction_expr
                         | PREDICT reaction_expr IF condition
                         | PREDICT reactants_expr
                         | PREDICT reactants_expr IF condition"""
    if len(p) == 3:  # No condition (reactants + products OR reactants only)
        if isinstance(p[2], nodes.ReactionExpressionNode):
            # Explicit reaction (A -> B)
            p[0] = nodes.ConditionalReactionNode(
                reactants=p[2].reactants,
                products=p[2].products,
                condition=None
            )
        else:
            # Reactants only (predict products)
            p[0] = nodes.ConditionalReactionNode(
                reactants=p[2],
                products=[],
                condition=None
            )
    else:  # With condition (len(p) == 5)
        if isinstance(p[2], nodes.ReactionExpressionNode):
            # Explicit reaction with condition (A -> B IF ...)
            p[0] = nodes.ConditionalReactionNode(
                reactants=p[2].reactants,
                products=p[2].products,
                condition=p[4]
            )
        else:
            # Reactants with condition (predict products)
            p[0] = nodes.ConditionalReactionNode(
                reactants=p[2],
                products=[],
                condition=p[4]
            )

def p_condition(p):
    """condition : condition AND condition
                 | condition OR condition
                 | CATALYST LPAREN ELEMENT_SYMBOL RPAREN
                 | TEMPERATURE LPAREN INTEGER IDENTIFIER RPAREN
                 | PRESSURE LPAREN INTEGER IDENTIFIER RPAREN"""
    if len(p) == 5:  # Single condition (e.g., CATALYST(Fe))
        p[0] = nodes.ConditionNode(
            condition_type=p.slice[1].type,  # Use token type, not value
            value=p[3]
        )
    elif len(p) == 6:  # Temperature or pressure condition (e.g., TEMPERATURE(450c))
        p[0] = nodes.ConditionNode(
            condition_type=p.slice[1].type,  # Use token type, not value
            value=f"{p[3]}{p[4]}"
        )
    else:  # Logical operator (e.g., AND, OR)
        operator = p.slice[2].type  # Correctly  get token type (AND/OR)
        p[0] = nodes.ConditionNode(
            condition_type='LOGICAL',
            left=p[1],
            right=p[3],
            operator=operator
        )

def p_analyze_statement(p):
    """analyze_statement : ANALYZE molecule
                         | ANALYZE molecule FOR IDENTIFIER"""
    detail_level = 'basic'
    if len(p) > 3:
        if p[4].lower() == 'all':
            detail_level = 'all'
        else:
            raise SyntaxError(f"Invalid detail specifier: {p[4]}. Use 'all'.")
    p[0] = nodes.AnalyzeStatementNode(target=p[2], detail_level=detail_level)

def p_reaction_type_statement(p):
    """reaction_type_statement : COMBUSTION
                               | DECOMPOSITION
                               | SINGLE_REPLACEMENT
                               | DOUBLE_REPLACEMENT
                               | ACID_BASE
                               | PRECIPITATION
                               | GAS_FORMATION
                               | COMBUSTION OF molecule
                               | DECOMPOSITION OF molecule
                               | SINGLE_REPLACEMENT OF molecule
                               | DOUBLE_REPLACEMENT OF molecule
                               | ACID_BASE OF molecule
                               | PRECIPITATION OF molecule
                               | GAS_FORMATION OF molecule"""
    if len(p) == 2:
        p[0] = nodes.ReactionTypeNode(p[1].upper(), None)  # e.g., p[1] = 'COMBUSTION'
    else:
        p[0] = nodes.ReactionTypeNode(p[1].upper(), p[3])  # e.g., p[1] = 'DECOMPOSITION', p[3] = molecule

def p_thermodynamic_statement(p):
    """thermodynamic_statement : ENTHALPY OF reaction_expr
                               | ENTROPY OF reaction_expr
                               | GIBBS_ENERGY OF reaction_expr
                               | EQUILIBRIUM OF reaction_expr
                               | ENTHALPY INFO reaction_expr
                               | ENTROPY INFO reaction_expr
                               | GIBBS_ENERGY INFO reaction_expr
                               | EQUILIBRIUM INFO reaction_expr"""
    if p[2] == 'of':
        p[0] = nodes.ThermodynamicNode(p[1].upper(), p[3], info=False)
    elif p[2] == 'info':
        p[0] = nodes.ThermodynamicNode(p[1].upper(), p[3], info=True)


def p_chemical_analysis_statement(p):
    """chemical_analysis_statement : OXIDATION_STATES OF molecule
                                   | LIMITING_REAGENT OF reaction_expr
                                   | PERCENT_YIELD OF reaction_expr
                                   | EMPIRICAL_FORMULA OF molecule
                                   | MOLECULAR_FORMULA OF molecule
                                   | MOLAR_MASS OF molecule"""
    p[0] = nodes.ChemicalAnalysisNode(p[1].upper(), p[3])

def p_reaction_expr(p):
    """reaction_expr : reactants_expr ARROW products_expr"""
    p[0] = nodes.ReactionExpressionNode(reactants=p[1], products=p[3])

def p_reactants_expr(p):
    """reactants_expr : chemical_term_list"""
    p[0] = p[1]

def p_products_expr(p):
    """products_expr : chemical_term_list"""
    p[0] = p[1]

def p_chemical_term_list(p):
    """chemical_term_list : chemical_term PLUS chemical_term_list
                          | chemical_term"""
    p[0] = [p[1]] + (p[3] if len(p) > 3 else [])

def p_chemical_term(p):
    """chemical_term : INTEGER molecule
                     | molecule"""
    if len(p) == 3:
        if p[1] <= 0:
            raise SyntaxError("Coefficient must be a positive integer.")
        p[0] = nodes.ChemicalTermNode(coefficient=p[1], molecule=p[2])
    else:
        p[0] = nodes.ChemicalTermNode(coefficient=1, molecule=p[1])

def p_molecule(p):
    """molecule : molecule_part molecule
                | molecule_part"""
    if len(p) == 3:
        # Combine elements from both parts
        combined_elements = p[1].elements + p[2].elements
        p[0] = nodes.MoleculeNode(elements=combined_elements)
    else:
        p[0] = p[1]

def p_molecule_part(p):
    """molecule_part : element_group
                     | LPAREN molecule RPAREN INTEGER"""
    if len(p) == 5:
        # Handle parentheses: e.g., (NO3)2
        multiplied_elements = [
            nodes.ElementGroupNode(elem.symbol, elem.count * p[4])
            for elem in p[2].elements
        ]
        p[0] = nodes.MoleculeNode(elements=multiplied_elements)
    else:
        # Single element group
        p[0] = nodes.MoleculeNode(elements=[p[1]])

def p_element_group(p):
    """element_group : ELEMENT_SYMBOL INTEGER
                     | ELEMENT_SYMBOL"""
    if len(p) == 3:
        p[0] = nodes.ElementGroupNode(symbol=p[1], count=p[2])
    else:
        p[0] = nodes.ElementGroupNode(symbol=p[1], count=1)

def p_error(p):
    if p:
        raise SyntaxError(f"Syntax error at '{p.value}' (line {p.lineno})")
    else:
        raise SyntaxError("Syntax error at end of input.")

# Build the parser
parser = yacc.yacc()

def parse(data: str):
    """Parse input and return AST."""
    return parser.parse(data, lexer=__import__("DSL.lexer", fromlist=["lexer"]).lexer)