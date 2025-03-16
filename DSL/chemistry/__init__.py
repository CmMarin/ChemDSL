"""
DSL/chemistry/__init__.py

This package provides domain-specific chemical data and functions for ChemDSL,
including element definitions, compound representation, reaction prediction,
and equation balancing.
"""
from .elements import ELEMENTS
from .compounds import Compound, parse_formula
from .reactions import Reaction, predict_reaction
from .balancer import balance_reaction
