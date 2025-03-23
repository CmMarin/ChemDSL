from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, messagebox
import sys
import io
from DSL.parser import parse
from DSL.interpreter.evaluator_dsl import Evaluator
from DSL.lexer import tokenize


class ChemDSL_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ChemDSL IDE")
        self.root.geometry("1200x800")

        # Create main panes
        main_pane = PanedWindow(root, orient=HORIZONTAL)
        main_pane.pack(fill=BOTH, expand=1)

        # Left pane (Code Editor)
        left_frame = Frame(main_pane)
        self.create_editor(left_frame)
        main_pane.add(left_frame)

        # Right pane (Visualization and Steps)
        right_pane = PanedWindow(main_pane, orient=VERTICAL)

        # Reaction Visualizer
        self.visualizer = ScrolledText(right_pane, height=15, wrap=WORD)
        right_pane.add(self.visualizer)

        # Execution Steps
        self.steps_text = ScrolledText(right_pane, height=15, wrap=WORD)
        right_pane.add(self.steps_text)

        main_pane.add(right_pane)

        # Run button
        Button(root, text="Run (F5)", command=self.run_code).pack(side=BOTTOM, pady=5)

        # Configure tags for syntax highlighting
        self.editor.tag_configure('keyword', foreground='blue')
        self.editor.tag_configure('error', foreground='red')

        # Bind F5 key
        self.root.bind('<F5>', lambda e: self.run_code())

    def create_editor(self, parent):
        self.editor = ScrolledText(parent, wrap=WORD, font=('Consolas', 12))
        self.editor.pack(fill=BOTH, expand=1)

        # Add sample code
        self.editor.insert(END, "predict N2 + O2;\n")
        self.editor.insert(END, "analyze HCl;\n")
        self.editor.insert(END, "balance H2 + O2 -> H2O;\n")
        self.editor.bind('<KeyRelease>', self.on_editor_change)

    def on_editor_change(self, event):
        self.highlight_syntax()

    def highlight_syntax(self):
        code = self.editor.get("1.0", END)
        self.editor.tag_remove('keyword', "1.0", END)

        keywords = ['predict', 'balance']
        for word in keywords:
            start = "1.0"
            while True:
                start = self.editor.search(r'\y%s\y' % word, start, stopindex=END, regexp=True)
                if not start:
                    break
                end = "%s+%dc" % (start, len(word))
                self.editor.tag_add('keyword', start, end)
                start = end

    def run_code(self):
        code = self.editor.get("1.0", END).strip()
        self.steps_text.delete('1.0', END)
        self.visualizer.delete('1.0', END)

        # Redirect stdout to capture steps
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            # Show lexer tokens
            self.steps_text.insert(END, "=== LEXER TOKENS ===\n")
            tokens = tokenize(code)
            for token in tokens:
                self.steps_text.insert(END, f"Type: {token['type']:15} Value: {token['value']}\n")

            # Parse code
            self.steps_text.insert(END, "\n=== PARSER OUTPUT ===\n")
            ast = parse(code)
            self.steps_text.insert(END, str(ast) + "\n")

            # Evaluate code
            self.steps_text.insert(END, "\n=== EVALUATION STEPS ===\n")
            evaluator = Evaluator()
            result = evaluator.evaluate(ast)

            # Add diagnostics
            self.steps_text.insert(END, f"\nResult type: {type(result)}\n")

            # Check if result is a dictionary with our marker
            if isinstance(result, dict) and result.get('is_analysis_result', False):
                self.steps_text.insert(END, "Processing analysis result...\n")
                self._format_analysis_result(result)
            # Try to convert string representation of dict to actual dict
            elif isinstance(result, str) and '{' in result and '}' in result:
                self.steps_text.insert(END, "Trying to parse dictionary string...\n")
                try:
                    import ast as python_ast
                    # Try to evaluate the string as a Python literal
                    dict_result = python_ast.literal_eval(result)
                    if isinstance(dict_result, dict) and dict_result.get('is_analysis_result', False):
                        self.steps_text.insert(END, "Successfully parsed as analysis result dictionary.\n")
                        self._format_analysis_result(dict_result)
                    else:
                        self.steps_text.insert(END, "String could not be parsed as an analysis result.\n")
                        self.visualizer.insert(END, result)
                except:
                    self.steps_text.insert(END, "Failed to parse as dictionary.\n")
                    self.visualizer.insert(END, result)
            else:
                self.steps_text.insert(END, "Not an analysis result, displaying as is.\n")
                self.visualizer.insert(END, str(result))

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.steps_text.insert(END, f"\nERROR: {str(e)}", 'error')
        finally:
            # Restore stdout and get captured output
            captured_output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            self.steps_text.insert(END, captured_output)

    # Add this to the ChemDSL_GUI class
    def _format_analysis_result(self, analysis):
        # # Clear previous content
        # self.visualizer.delete('1.0', END)

        # Configure tags for formatting
        self.visualizer.tag_configure('header', font=('Helvetica', 12, 'bold'), foreground='blue')
        self.visualizer.tag_configure('subheader', font=('Helvetica', 11, 'bold'))
        self.visualizer.tag_configure('bold', font=('Helvetica', 10, 'bold'))

        if 'element' in analysis:
            # Format element analysis
            self.visualizer.insert(END, "=== Element Analysis ===\n", 'header')
            self.visualizer.insert(END, f"Symbol: {analysis['element']}\n", 'bold')
            self.visualizer.insert(END, f"Name: {analysis['name']}\n")
            self.visualizer.insert(END, f"Atomic Weight: {analysis['atomic_weight']}\n")
            self.visualizer.insert(END, f"State at STP: {analysis['state']}\n")
            self.visualizer.insert(END, f"Group: {analysis['group']}\n")
            self.visualizer.insert(END, f"Electronegativity: {analysis['electronegativity']}\n")

            # Common Compounds
            self.visualizer.insert(END, "\nCommon Compounds:\n", 'subheader')
            for compound in analysis['common_compounds']:
                self.visualizer.insert(END, f"  - {compound}\n")

            # Common Reactions
            self.visualizer.insert(END, "\nCommon Reactions:\n", 'subheader')
            for reaction in analysis['common_reactions']:
                self.visualizer.insert(END, f"  - {reaction}\n")


        elif 'compound' in analysis:

            # Compound analysis formatting

            self.visualizer.insert(END, "=== Compound Analysis ===\n", 'header')

            self.visualizer.insert(END, f"Formula: {analysis['compound']}\n", 'bold')

            if 'name' in analysis:
                self.visualizer.insert(END, f"Name: {analysis['name']}\n")

            self.visualizer.insert(END, f"Molar Mass: {analysis['molar_mass']:.2f} g/mol\n")

            if 'state' in analysis:
                self.visualizer.insert(END, f"State at STP: {analysis['state']}\n")

            if 'classification' in analysis:
                self.visualizer.insert(END, f"Classification: {analysis['classification']}\n")

            # Composition

            self.visualizer.insert(END, "\nComposition:\n", 'subheader')

            for element, count in analysis['composition'].items():
                self.visualizer.insert(END, f"  - {element}: {count}\n")

            # Additional detailed information (if available)

            if analysis.get('detail_level') == 'all':

                if 'density' in analysis:
                    self.visualizer.insert(END, f"\nDensity: {analysis['density']}\n")

                if 'melting_point' in analysis:
                    self.visualizer.insert(END, f"Melting Point: {analysis['melting_point']} °C\n")

                if 'boiling_point' in analysis:
                    self.visualizer.insert(END, f"Boiling Point: {analysis['boiling_point']} °C\n")

                if 'solubility' in analysis:
                    self.visualizer.insert(END, f"Solubility: {analysis['solubility']}\n")

                if 'acidity' in analysis:
                    self.visualizer.insert(END, f"Acidity: {analysis['acidity']}\n")

                if 'common_uses' in analysis:

                    self.visualizer.insert(END, "\nCommon Uses:\n", 'subheader')

                    for use in analysis['common_uses']:
                        self.visualizer.insert(END, f"  - {use}\n")

                if 'hazards' in analysis:

                    self.visualizer.insert(END, "\nHazards:\n", 'subheader')

                    for hazard in analysis['hazards']:
                        self.visualizer.insert(END, f"  - {hazard}\n")

        else:
            # Generic handling for other dictionary results
            self.visualizer.insert(END, "=== Analysis Results ===\n", 'header')
            for key, value in analysis.items():
                if isinstance(value, dict):
                    self.visualizer.insert(END, f"\n{key.title()}:\n", 'subheader')
                    for sub_key, sub_value in value.items():
                        self.visualizer.insert(END, f"  - {sub_key}: {sub_value}\n")
                elif isinstance(value, list):
                    self.visualizer.insert(END, f"\n{key.title()}:\n", 'subheader')
                    for item in value:
                        self.visualizer.insert(END, f"  - {item}\n")
                else:
                    self.visualizer.insert(END, f"{key.title()}: {value}\n")

        # Display detail level if present
        if 'detail_level' in analysis:
            self.visualizer.insert(END, f"\nDetail Level: {analysis['detail_level']}\n")


if __name__ == "__main__":
    root = Tk()
    app = ChemDSL_GUI(root)
    root.mainloop()