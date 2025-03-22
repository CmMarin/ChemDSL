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
    p[0] = nodes.ProgramNode(p[1])

def p_statement_list(p):
    """statement_list : statement SEMICOLON statement_list
                     | statement SEMICOLON"""
    p[0] = [p[1]] + (p[3] if len(p) > 3 else [])

def p_statement(p):
    """statement : balance_statement
                 | predict_statement"""
    p[0] = p[1]

def p_balance_statement(p):
    """balance_statement : BALANCE reaction_expr"""
    p[0] = nodes.BalanceStatementNode(p[2])

def p_predict_statement(p):
    """predict_statement : PREDICT reactants_expr"""
    # Create a ReactionExpressionNode with reactants and empty products
    reaction_expr = nodes.ReactionExpressionNode(reactants=p[2], products=[])
    p[0] = nodes.PredictStatementNode(reaction_expr)

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