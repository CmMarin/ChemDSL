"""
DSL/interpreter/environment.py

Defines the environment for storing variable and function definitions during evaluation.
"""

class Environment:
    def __init__(self, parent=None):
        self.parent = parent
        self.vars = {}

    def define(self, name, value):
        self.vars[name] = value

    def assign(self, name, value):
        if name in self.vars:
            self.vars[name] = value
        elif self.parent:
            self.parent.assign(name, value)
        else:
            raise Exception(f"Undefined variable: {name}")

    def lookup(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            return self.parent.lookup(name)
        else:
            raise Exception(f"Undefined variable: {name}")
