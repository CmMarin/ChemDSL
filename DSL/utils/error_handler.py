# File: DSL/utils/error_handler.py
"""
DSL/utils/error_handler.py

Implements error handling for the DSL.
"""

class ChemDSLError(Exception):
    """Base exception class for ChemDSL errors."""
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self.format_message())
    
    def format_message(self):
        """Format the error message with line and column information if available."""
        location = ""
        if self.line is not None:
            location = f" at line {self.line}"
            if self.column is not None:
                location += f", column {self.column}"
        return f"ChemDSL Error{location}: {self.message}"

class ErrorHandler:
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def add_error(self, message, line=None, column=None):
        """Add an error message to the error list."""
        error = {
            'message': message,
            'line': line,
            'column': column
        }
        self.errors.append(error)
    
    def add_warning(self, message, line=None, column=None):
        """Add a warning message to the warning list."""
        warning = {
            'message': message,
            'line': line,
            'column': column
        }
        self.warnings.append(warning)
    
    def has_errors(self):
        """Check if there are any errors."""
        return len(self.errors) > 0
    
    def has_warnings(self):
        """Check if there are any warnings."""
        return len(self.warnings) > 0
    
    def get_errors(self):
        """Get all error messages."""
        return self.errors
    
    def get_warnings(self):
        """Get all warning messages."""
        return self.warnings
    
    def clear(self):
        """Clear all errors and warnings."""
        self.errors = []
        self.warnings = []
    
    def report_errors(self):
        """Format and return all error messages."""
        if not self.has_errors():
            return "No errors."
        
        result = "Errors:\n"
        for error in self.errors:
            location = ""
            if error['line'] is not None:
                location = f" at line {error['line']}"
                if error['column'] is not None:
                    location += f", column {error['column']}"
            result += f"- {error['message']}{location}\n"
        return result
    
    def report_warnings(self):
        """Format and return all warning messages."""
        if not self.has_warnings():
            return "No warnings."
        
        result = "Warnings:\n"
        for warning in self.warnings:
            location = ""
            if warning['line'] is not None:
                location = f" at line {warning['line']}"
                if warning['column'] is not None:
                    location += f", column {warning['column']}"
            result += f"- {warning['message']}{location}\n"
        return result