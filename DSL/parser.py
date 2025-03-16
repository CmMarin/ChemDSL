"""
DSL/parser.py
Parser for ChemDSL using PLY (Python Lex-Yacc)

This module uses the tokens from lexer.py and builds an abstract syntax tree (AST)
using production rules. The AST nodes are defined in DSL/ast_nodes/nodes.py.
"""

import ply.yacc as yacc
from DSL.lexer import tokens
from DSL.ast_nodes import nodes


# Grammar production rules

def p_program(p):
    """program : statement_list"""
    p[0] = nodes.ProgramNode(p[1])


def p_statement_list_multiple(p):
    """statement_list : statement SEMICOLON statement_list"""
    p[0] = [p[1]] + p[3]


def p_statement_list_single(p):
    """statement_list : statement SEMICOLON"""
    p[0] = [p[1]]


def p_statement_balance(p):
    """statement : balance_statement"""
    p[0] = p[1]


def p_statement_predict(p):
    """statement : predict_statement"""
    p[0] = p[1]


def p_balance_statement(p):
    """balance_statement : BALANCE reaction_expr"""
    p[0] = nodes.BalanceStatementNode(p[2])


def p_predict_statement(p):
    """predict_statement : PREDICT reaction_expr"""
    p[0] = nodes.PredictStatementNode(p[2])


def p_reaction_expr(p):
    """reaction_expr : reactants_expr ARROW products_expr"""
    p[0] = nodes.ReactionExpressionNode(p[1], p[3])


def p_reactants_expr(p):
    """reactants_expr : chemical_term_list"""
    p[0] = p[1]


def p_products_expr(p):
    """products_expr : chemical_term_list"""
    p[0] = p[1]


def p_chemical_term_list_multiple(p):
    """chemical_term_list : chemical_term PLUS chemical_term_list"""
    p[0] = [p[1]] + p[3]


def p_chemical_term_list_single(p):
    """chemical_term_list : chemical_term"""
    p[0] = [p[1]]


def p_chemical_term_with_coeff(p):
    """chemical_term : INTEGER molecule"""
    p[0] = nodes.ChemicalTermNode(coefficient=p[1], molecule=p[2])


def p_chemical_term_without_coeff(p):
    """chemical_term : molecule"""
    p[0] = nodes.ChemicalTermNode(coefficient=1, molecule=p[1])


def p_molecule_paren(p):
    """molecule : LPAREN molecule RPAREN INTEGER"""
    # Multiply counts inside parentheses by the trailing integer
    p[0] = nodes.MoleculeNode(p[2].elements, multiplier=p[4])


def p_molecule_simple(p):
    """molecule : molecule element_group"""
    # Append element group to molecule
    p[1].elements.append(p[2])
    p[0] = p[1]


def p_molecule_single(p):
    """molecule : element_group"""
    p[0] = nodes.MoleculeNode([p[1]])


def p_element_group_with_count(p):
    """element_group : ELEMENT_SYMBOL INTEGER"""
    p[0] = nodes.ElementGroupNode(symbol=p[1], count=p[2])


def p_element_group_single(p):
    """element_group : ELEMENT_SYMBOL"""
    p[0] = nodes.ElementGroupNode(symbol=p[1], count=1)


def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lineno})")
    else:
        print("Syntax error at EOF")


parser = yacc.yacc()


def parse(data: str):
    """
    Parse the input ChemDSL code and return the AST.
    """
    return parser.parse(data, lexer=__import__("DSL.lexer", fromlist=["lexer"]).lexer)
