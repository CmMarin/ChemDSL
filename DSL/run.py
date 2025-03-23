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
        self.root.geometry("1300x850")
        self.configure_styles()

        # Main container
        main_pane = ttk.PanedWindow(root, orient=HORIZONTAL)
        main_pane.pack(fill=BOTH, expand=1)

        # Left Panel (Editor)
        left_frame = ttk.Frame(main_pane)
        self.create_editor_ui(left_frame)
        main_pane.add(left_frame)

        # Right Panel (Visualization)
        right_pane = ttk.PanedWindow(main_pane, orient=VERTICAL)
        self.create_visualization_ui(right_pane)
        main_pane.add(right_pane)

        # Status Bar
        self.status_bar = ttk.Label(root, text="Ready", relief=SUNKEN)
        self.status_bar.pack(side=BOTTOM, fill=X)

        self.root.bind('<F5>', lambda e: self.run_code())

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#2d2d30')
        style.configure('TButton', background='#3e3e42', foreground='white', borderwidth=0)
        style.map('TButton', background=[('active', '#007acc')])
        style.configure('TLabel', background='#2d2d30', foreground='white')
        style.configure('TNotebook', background='#2d2d30', borderwidth=0)
        style.configure('TNotebook.Tab', background='#3e3e42', foreground='white', padding=[10, 5])

    def create_editor_ui(self, parent):
        # Toolbar
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill=X, pady=5)

        commands = [
            ("Predict", "predict {};"),
            ("Analyze", "analyze {};"),
            ("Balance", "balance {} -> {};"),
            ("Clear", self.clear_all)
        ]

        for text, cmd in commands:
            btn = ttk.Button(toolbar, text=text,
                             command=lambda c=cmd: self.insert_template(c) if isinstance(c, str) else c())
            btn.pack(side=LEFT, padx=2)

        # Editor
        self.editor = ScrolledText(parent, wrap=WORD, font=('Consolas', 12),
                                   bg='#1e1e1e', fg='white', insertbackground='white')
        self.editor.pack(fill=BOTH, expand=1)

        # Tutorial placeholder
        self.tutorial_text = """/* ChemDSL Quick Guide */

1. Use toolbar buttons to insert commands
2. Press F5 or Run button to execute
3. View results in right panels

Examples:
predict N2 + O2;
analyze H2O;
balance CH4 + O2 -> CO2 + H2O;"""
        self.editor.insert(END, self.tutorial_text)
        self.editor.tag_add("placeholder", "1.0", "end")
        self.editor.tag_config("placeholder", foreground="#808080")
        self.editor.bind("<FocusIn>", self.clear_placeholder)
        self.editor.bind('<KeyRelease>', self.on_editor_change)

    def create_visualization_ui(self, parent):
        notebook = ttk.Notebook(parent)

        # Results Tab
        results_frame = ttk.Frame(notebook)
        self.visualizer = ScrolledText(results_frame, wrap=WORD, font=('Segoe UI', 11),
                                       bg='#2d2d30', fg='white', insertbackground='white')
        self.visualizer.pack(fill=BOTH, expand=1)

        # Steps Tab
        steps_frame = ttk.Frame(notebook)
        self.steps_text = ScrolledText(steps_frame, wrap=WORD, font=('Segoe UI', 11),
                                       bg='#2d2d30', fg='white', insertbackground='white')
        self.steps_text.pack(fill=BOTH, expand=1)

        notebook.add(results_frame, text="Analysis Results")
        notebook.add(steps_frame, text="Execution Steps")
        notebook.pack(fill=BOTH, expand=1)

    def insert_template(self, template):
        self.clear_placeholder()
        self.editor.insert(END, template + "\n")
        self.editor.focus_set()
        self.status_bar.config(text=f"Inserted template: {template}")

    def clear_placeholder(self, event=None):
        if "placeholder" in self.editor.tag_names("1.0"):
            self.editor.delete("1.0", "end")
            self.editor.tag_remove("placeholder", "1.0", "end")

    def clear_all(self):
        self.editor.delete("1.0", END)
        self.visualizer.delete("1.0", END)
        self.steps_text.delete("1.0", END)
        self.editor.insert(END, self.tutorial_text)
        self.editor.tag_add("placeholder", "1.0", "end")
        self.status_bar.config(text="Cleared all content")

    def on_editor_change(self, event):
        self.highlight_syntax()

    def highlight_syntax(self):
        code = self.editor.get("1.0", END)
        self.editor.tag_remove('keyword', "1.0", END)
        self.editor.tag_remove('comment', "1.0", END)

        keywords = ['predict', 'balance', 'analyze']
        for word in keywords:
            start = "1.0"
            while True:
                start = self.editor.search(r'\y%s\y' % word, start, stopindex=END, regexp=True)
                if not start:
                    break
                end = "%s+%dc" % (start, len(word))
                self.editor.tag_add('keyword', start, end)
                start = end

        # Highlight comments
        start = "1.0"
        while True:
            start = self.editor.search(r'/\*.*?\*/', start, stopindex=END, regexp=True)
            if not start:
                break
            end = self.editor.search(r'\*/', start, stopindex=END, regexp=True)
            if end:
                end += "+2c"
                self.editor.tag_add('comment', start, end)
                start = end
            else:
                break

        self.editor.tag_configure('keyword', foreground='#569cd6')
        self.editor.tag_configure('comment', foreground='#608b4e')

    # Keep original run_code and _format_analysis_result methods unchanged
    def run_code(self):
        # Original run_code implementation from user's code
        code = self.editor.get("1.0", END).strip()
        self.steps_text.delete('1.0', END)
        self.visualizer.delete('1.0', END)

        # Redirect stdout to capture steps
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            self.status_bar.config(text="Executing...")
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
            elif isinstance(result, str) and '{' in result and '}' in result:
                self.steps_text.insert(END, "Trying to parse dictionary string...\n")
                try:
                    import ast as python_ast
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
            self.status_bar.config(text=f"Error: {str(e)}")
        finally:
            captured_output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            self.steps_text.insert(END, captured_output)
            self.status_bar.config(text="Execution completed")

    def _format_analysis_result(self, analysis):
        # Original _format_analysis_result implementation from user's code
        self.visualizer.tag_configure('header', font=('Helvetica', 12, 'bold'), foreground='#569cd6')
        self.visualizer.tag_configure('subheader', font=('Helvetica', 11, 'bold'), foreground='#dcdcaa')
        self.visualizer.tag_configure('bold', font=('Helvetica', 10, 'bold'), foreground='white')

        if 'element' in analysis:
            self.visualizer.insert(END, "=== Element Analysis ===\n", 'header')
            self.visualizer.insert(END, f"Symbol: {analysis['element']}\n", 'bold')
            self.visualizer.insert(END, f"Name: {analysis['name']}\n")
            self.visualizer.insert(END, f"Atomic Weight: {analysis['atomic_weight']}\n")
            self.visualizer.insert(END, f"State at STP: {analysis['state']}\n")
            self.visualizer.insert(END, f"Group: {analysis['group']}\n")
            self.visualizer.insert(END, f"Electronegativity: {analysis['electronegativity']}\n")

            self.visualizer.insert(END, "\nCommon Compounds:\n", 'subheader')
            for compound in analysis['common_compounds']:
                self.visualizer.insert(END, f"  - {compound}\n")

            self.visualizer.insert(END, "\nCommon Reactions:\n", 'subheader')
            for reaction in analysis['common_reactions']:
                self.visualizer.insert(END, f"  - {reaction}\n")

        elif 'compound' in analysis:
            self.visualizer.insert(END, "=== Compound Analysis ===\n", 'header')
            self.visualizer.insert(END, f"Formula: {analysis['compound']}\n", 'bold')

            if 'name' in analysis:
                self.visualizer.insert(END, f"Name: {analysis['name']}\n")

            self.visualizer.insert(END, f"Molar Mass: {analysis['molar_mass']:.2f} g/mol\n")

            if 'state' in analysis:
                self.visualizer.insert(END, f"State at STP: {analysis['state']}\n")

            if 'classification' in analysis:
                self.visualizer.insert(END, f"Classification: {analysis['classification']}\n")

            self.visualizer.insert(END, "\nComposition:\n", 'subheader')
            for element, count in analysis['composition'].items():
                self.visualizer.insert(END, f"  - {element}: {count}\n")

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

        if 'detail_level' in analysis:
            self.visualizer.insert(END, f"\nDetail Level: {analysis['detail_level']}\n")


if __name__ == "__main__":
    root = Tk()
    app = ChemDSL_GUI(root)
    root.mainloop()