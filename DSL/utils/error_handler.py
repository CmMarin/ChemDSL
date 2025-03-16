"""
DSL/utils/error_handler.py

Provides error handling utilities for ChemDSL.
"""

class ChemDSLError(Exception):
    def __init__(self, message, lineno=None, lexpos=None):
        self.message = message
        self.lineno = lineno
        self.lexpos = lexpos
        super().__init__(self.__str__())

    def __str__(self):
        loc = f" at line {self.lineno}, pos {self.lexpos}" if self.lineno is not None else ""
        return f"ChemDSLError: {self.message}{loc}"

class ErrorHandler:
    @staticmethod
    def report_error(message, lineno=None, lexpos=None):
        error = ChemDSLError(message, lineno, lexpos)
        print(error)
        # Optionally, log the error or raise exception
        raise error
