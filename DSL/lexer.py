"""
DSL/lexer.py
Lexical analyzer for ChemDSL

This module defines the lexical analysis component of the ChemDSL interpreter.
It tokenizes input strings according to the ChemDSL grammar.
"""

import re
import ply.lex as lex
from typing import List, Dict, Any

# Token names
tokens = (
    # Keywords
    'BALANCE', 'PREDICT', 'ANALYZE', 'QUERY',
    'ELEMENT', 'COMPOUND', 'REACTION', 'YIELD',
    'WITH', 'FOR', 'OF', 'INFO', 'IF', 'AND', 'OR',
    'REDOX', 'ALGEBRAIC', 'HALF_REACTION', 'OXIDATION_NUMBER',

    # Reaction types
    'REACTION_TYPE','COMBUSTION', 'DECOMPOSITION', 'SINGLE_REPLACEMENT', 'DOUBLE_REPLACEMENT',
    'ACID_BASE', 'PRECIPITATION', 'GAS_FORMATION',

    # Analysis options
    'ENTHALPY', 'ENTROPY', 'GIBBS_ENERGY', 'EQUILIBRIUM',
    'OXIDATION_STATES', 'LIMITING_REAGENT', 'PERCENT_YIELD',
    'EMPIRICAL_FORMULA', 'MOLECULAR_FORMULA', 'MOLAR_MASS',

    # State specifiers
    'AQUEOUS', 'SOLID', 'LIQUID', 'GAS',

    # Condition types
    'CATALYST', 'HEAT', 'PRESSURE', 'PH', 'TEMPERATURE',
    'MOLARITY', 'NORMALITY', 'TIME',

    # Identifiers and literals
    'ELEMENT_SYMBOL', 'IDENTIFIER', 'INTEGER', 'FLOAT', 'STRING',

    # Operators and punctuation
    'PLUS', 'ARROW', 'REVERSIBLE_ARROW', 'RESONANCE_ARROW',
    'EQUALS', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
    'LBRACE', 'RBRACE', 'COMMA', 'SEMICOLON',
    'CARET', 'ASSIGN',

    # Special tokens for charge notation
    'POSITIVE', 'NEGATIVE',
)

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_ARROW = r'->'
t_REVERSIBLE_ARROW = r'<->'
t_RESONANCE_ARROW = r'<==>'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'
t_CARET = r'\^'
t_ASSIGN = r'='
t_POSITIVE = r'\+'
t_NEGATIVE = r'-'

# Keywords mapping (case-insensitive)
keywords = {
    'balance': 'BALANCE',
    'predict': 'PREDICT',
    'analyze': 'ANALYZE',
    'query': 'QUERY',
    'element': 'ELEMENT',
    'compound': 'COMPOUND',
    'reaction': 'REACTION',
    'yield': 'YIELD',
    'with': 'WITH',
    'for': 'FOR',
    'of': 'OF',
    'and': 'AND',
    'if': 'IF',
    'info': 'INFO',
    'redox': 'REDOX',
    'algebraic': 'ALGEBRAIC',
    'half-reaction': 'HALF_REACTION',
    'oxidation-number': 'OXIDATION_NUMBER',
    'combustion': 'COMBUSTION',
    'decomposition': 'DECOMPOSITION',
    'single_replacement': 'SINGLE_REPLACEMENT',
    'double_replacement': 'DOUBLE_REPLACEMENT',
    'acid_base': 'ACID_BASE',
    'precipitation': 'PRECIPITATION',
    'gas_formation': 'GAS_FORMATION',
    'enthalpy': 'ENTHALPY',
    'entropy': 'ENTROPY',
    'gibbs_energy': 'GIBBS_ENERGY',
    'equilibrium': 'EQUILIBRIUM',
    'oxidation_states': 'OXIDATION_STATES',
    'limiting_reagent': 'LIMITING_REAGENT',
    'percent_yield': 'PERCENT_YIELD',
    'empirical_formula': 'EMPIRICAL_FORMULA',
    'molecular_formula': 'MOLECULAR_FORMULA',
    'molar_mass': 'MOLAR_MASS',
    'aq': 'AQUEOUS',
    's': 'SOLID',
    'l': 'LIQUID',
    'g': 'GAS',
    'soln': 'AQUEOUS',
    'solid': 'SOLID',
    'liquid': 'LIQUID',
    'gas': 'GAS',
    'aqueous': 'AQUEOUS',
    'catalyst': 'CATALYST',
    'heat': 'HEAT',
    'pressure': 'PRESSURE',
    'ph': 'PH',
    'temperature': 'TEMPERATURE',
    'molarity': 'MOLARITY',
    'normality': 'NORMALITY',
    'time': 'TIME',
}

# Valid element symbols – a set for quick lookup
ELEMENT_SYMBOLS = {
    'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
    'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca',
    'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
    'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr',
    'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn',
    'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd',
    'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb',
    'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',
    'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th',
    'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm',
    'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds',
    'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og'
}

def t_ELEMENT_SYMBOL(t):
    r'[A-Z][a-z]?'
    if t.value not in ELEMENT_SYMBOLS:
        raise SyntaxError(f"Invalid element symbol: {t.value}")
    t.type = 'ELEMENT_SYMBOL'
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.value = t.value.lower()  # Normalize to lowercase
    t.type = keywords.get(t.value, 'IDENTIFIER')  # Look up in keywords dictionary
    return t

def t_FLOAT(t):
    r'\d+\.\d*'
    t.value = float(t.value)
    return t

def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]  # Remove quotes
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignore spaces and tabs
t_ignore = ' \t'

def t_error(t):
    raise SyntaxError(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")

# Build the lexer
lexer = lex.lex()

def tokenize(data: str) -> List[Dict[str, Any]]:
    """
    Tokenize input string according to ChemDSL grammar.
    """
    lexer.input(data)
    result = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        result.append({
            'type': tok.type,
            'value': tok.value,
            'line': tok.lineno,
            'position': tok.lexpos
        })
    return result

# Test function (for debugging)
def test_lexer(data: str) -> None:
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

def tokenize(data: str) -> List[Dict[str, Any]]:
    """Tokenize input strings with logging"""
    print("=== LEXER TOKENIZATION ===")
    lexer.input(data)
    result = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"Token: Type='{tok.type}', Value='{tok.value}', Position={tok.lexpos}")
        result.append({'type': tok.type, 'value': tok.value})
    return result