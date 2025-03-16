"""
DSL/semantic/symbol_table.py

Defines a symbol table for storing variable and compound definitions.
"""

class SymbolTable:
    def __init__(self, parent=None):
        self.parent = parent
        self.symbols = {}

    def define(self, name, value):
        if name in self.symbols:
            raise Exception(f"Symbol '{name}' already defined in current scope.")
        self.symbols[name] = value

    def assign(self, name, value):
        if name in self.symbols:
            self.symbols[name] = value
        elif self.parent:
            self.parent.assign(name, value)
        else:
            raise Exception(f"Symbol '{name}' is not defined.")

    def lookup(self, name):
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.lookup(name)
        else:
            raise Exception(f"Symbol '{name}' is not defined.")
