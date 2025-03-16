import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import itertools
import ply.lex as lex
import ply.yacc as yacc

# ------------------------
# DSL Code for ChemDSL
# ------------------------

# Lexer tokens
tokens = (
    'BALANCE', 'PREDICT', 'COMBUSTION', 'SYNTHESIS', 'DECOMPOSITION', 'SINGLE_REPLACEMENT',
    'DOUBLE_REPLACEMENT', 'PRECIPITATION', 'REDOX', 'ACID_BASE', 'OF',
    'ELEMENT_SYMBOL', 'DIGITS', 'PLUS', 'ARROW', 'SEMICOLON'
)

t_BALANCE = r'balance'
t_PREDICT = r'predict'
t_COMBUSTION = r'combustion'
t_SYNTHESIS = r'synthesis'
t_DECOMPOSITION = r'decomposition'
t_SINGLE_REPLACEMENT = r'single_replacement'
t_DOUBLE_REPLACEMENT = r'double_replacement'
t_PRECIPITATION = r'precipitation'
t_REDOX = r'redox'
t_ACID_BASE = r'acid_base'
t_OF = r'of'
t_PLUS = r'\+'
t_ARROW = r'->'
t_SEMICOLON = r';'

def t_ELEMENT_SYMBOL(t):
    r'[A-Z][a-z]?'
    return t

def t_DIGITS(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_WHITESPACE(t):
    r'\s+'
    pass

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Parser rules
def p_program(p):
    '''program : statement_list'''
    p[0] = p[1]

def p_statement_list_multiple(p):
    '''statement_list : statement SEMICOLON statement_list'''
    p[0] = [p[1]] + p[3]

def p_statement_list_single(p):
    '''statement_list : statement SEMICOLON'''
    p[0] = [p[1]]

def p_predict_statement_combustion(p):
    '''predict_statement : PREDICT COMBUSTION OF reactants_expr'''
    p[0] = ('predict', ('combustion', p[4]))

def p_predict_statement_synthesis(p):
    '''predict_statement : PREDICT SYNTHESIS OF reactants_expr'''
    p[0] = ('predict', ('synthesis', p[4]))

def p_predict_statement_decomposition(p):
    '''predict_statement : PREDICT DECOMPOSITION OF reactants_expr'''
    p[0] = ('predict', ('decomposition', p[4]))

def p_predict_statement_single_replacement(p):
    '''predict_statement : PREDICT SINGLE_REPLACEMENT OF reactants_expr'''
    p[0] = ('predict', ('single_replacement', p[4]))

def p_predict_statement_double_replacement(p):
    '''predict_statement : PREDICT DOUBLE_REPLACEMENT OF reactants_expr'''
    p[0] = ('predict', ('double_replacement', p[4]))

def p_predict_statement_precipitation(p):
    '''predict_statement : PREDICT PRECIPITATION OF reactants_expr'''
    p[0] = ('predict', ('precipitation', p[4]))

def p_predict_statement_redox(p):
    '''predict_statement : PREDICT REDOX OF reactants_expr'''
    p[0] = ('predict', ('redox', p[4]))

def p_predict_statement_acid_base(p):
    '''predict_statement : PREDICT ACID_BASE OF reactants_expr'''
    p[0] = ('predict', ('acid_base', p[4]))

def p_predict_statement(p):
    '''predict_statement : PREDICT reactants_expr'''
    p[0] = ('predict', p[2])

def p_statement(p):
    '''statement : balance_statement
                 | predict_statement'''
    p[0] = p[1]

def p_balance_statement(p):
    '''balance_statement : BALANCE reaction_expr'''
    p[0] = ('balance', p[2])

def p_reaction_expr(p):
    '''reaction_expr : reactants_expr ARROW products_expr'''
    p[0] = ('reaction', p[1], p[3])

def p_reactants_expr(p):
    '''reactants_expr : chemical_term_list'''
    p[0] = p[1]

def p_products_expr(p):
    '''products_expr : chemical_term_list'''
    p[0] = p[1]

def p_chemical_term_list_multiple(p):
    '''chemical_term_list : chemical_term PLUS chemical_term_list'''
    p[0] = [p[1]] + p[3]

def p_chemical_term_list_single(p):
    '''chemical_term_list : chemical_term'''
    p[0] = [p[1]]

def p_chemical_term(p):
    '''chemical_term : coefficient chemical_expr
                     | chemical_expr'''
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = (1, p[1])

def p_coefficient(p):
    '''coefficient : DIGITS'''
    p[0] = p[1]

def p_chemical_expr(p):
    '''chemical_expr : molecule'''
    p[0] = p[1]

def p_molecule_multiple(p):
    '''molecule : molecule element_group'''
    p[0] = p[1] + [p[2]]

def p_molecule_single(p):
    '''molecule : element_group'''
    p[0] = [p[1]]

def p_element_group_with_digits(p):
    '''element_group : ELEMENT_SYMBOL DIGITS'''
    p[0] = (p[1], p[2])

def p_element_group_single(p):
    '''element_group : ELEMENT_SYMBOL'''
    p[0] = (p[1], 1)

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

def parse_input(data):
    return parser.parse(data)

# ------------------------
# Reaction Prediction Logic
# ------------------------

def predict_synthesis(reactants):
    if len(reactants) == 2:
        r1, r2 = reactants
        if r1[1] and r2[1]:
            product = r1[1] + r2[1]
            return [(1, r1[1]), (1, r2[1])], [(1, product)], (1, 1)
    return None

def predict_decomposition(reactants):
    if len(reactants) == 1:
        r1 = reactants[0]
        product1 = r1[1][:len(r1[1])//2]
        product2 = r1[1][len(r1[1])//2:]
        return [(1, r1[1])], [(1, product1), (1, product2)], (1, 1)
    return None

def predict_single_replacement(reactants):
    if len(reactants) == 2:
        r1, r2 = reactants
        if r1[1] and r2[1]:
            product1 = r1[1] + r2[1][:len(r2[1])//2]
            product2 = r2[1][len(r2[1])//2:]
            return [(1, r1[1]), (1, r2[1])], [(1, product1), (1, product2)], (1, 1)
    return None

def predict_double_replacement(reactants):
    if len(reactants) == 2:
        r1, r2 = reactants
        if r1[1] and r2[1]:
            product1 = r1[1][:len(r1[1])//2] + r2[1][:len(r2[1])//2]
            product2 = r1[1][len(r1[1])//2:] + r2[1][len(r2[1])//2:]
            return [(1, r1[1]), (1, r2[1])], [(1, product1), (1, product2)], (1, 1)
    return None

def predict_precipitation(reactants):
    solubility_rules = {
        "Na": "soluble",
        "Cl": "soluble",
        "Ag": "insoluble"
    }
    if len(reactants) == 2:
        r1, r2 = reactants
        product1 = r1[1][:len(r1[1])//2] + r2[1][:len(r2[1])//2]
        product2 = r1[1][len(r1[1])//2:] + r2[1][len(r2[1])//2:]
        if solubility_rules.get(product1[0][0], "soluble") == "insoluble":
            return [(1, r1[1]), (1, r2[1])], [(1, product1)], (1, 1)
    return None

def predict_redox(reactants):
    if len(reactants) == 2:
        r1, r2 = reactants
        if r1[1] and r2[1]:
            return [(1, r1[1]), (1, r2[1])], [(1, r1[1]), (1, r2[1])], (1, 1)
    return None

def predict_acid_base(reactants):
    if len(reactants) == 2:
        acid, base = reactants
        if acid[1] and base[1]:
            salt = acid[1][:len(acid[1])//2] + base[1][:len(base[1])//2]
            return [(1, acid[1]), (1, base[1])], [(1, salt), (1, [("H",2), ("O",1)])], (1, 1)
    return None

def is_balanced(reactants, products, xs):
    """
    Each term's effective coefficient is: given * multiplier.
    xs is a tuple of multipliers (one per term).
    """
    n_reactants = len(reactants)
    elements = set()
    for term in reactants + products:
        for elem, cnt in term[1]:
            elements.add(elem)
    for e in elements:
        left_sum = sum(reactants[i][0] * xs[i] * next((cnt for (el, cnt) in reactants[i][1] if el == e), 0)
                        for i in range(n_reactants))
        right_sum = sum(products[j][0] * xs[n_reactants+j] * next((cnt for (el, cnt) in products[j][1] if el == e), 0)
                         for j in range(len(products)))
        if left_sum != right_sum:
            return False
    return True

def find_balanced_coefficients(reactants, products, max_coeff=10):
    total = len(reactants) + len(products)
    best_xs = None
    for xs in itertools.product(range(1, max_coeff+1), repeat=total):
        if is_balanced(reactants, products, xs):
            if best_xs is None or sum(xs) < sum(best_xs):
                best_xs = xs
    return best_xs

def predict_combustion(reactants):
    """
    For a pure hydrocarbon CxHy, complete combustion is:
      4 CxHy + (4x+y) O2 -> 4x CO2 + 2y H2O
    This function looks for a hydrocarbon (only C and H).
    """
    for given, mol in reactants:
        counts = {}
        for elem, cnt in mol:
            counts[elem] = counts.get(elem, 0) + cnt
        if 'C' in counts and 'H' in counts and set(counts.keys()).issubset({'C','H'}):
            x = counts['C']
            y = counts['H']
            predicted_reactants = [ (1, mol), (1, [("O",2)]) ]
            predicted_products = [ (1, [("C",1), ("O",2)]), (1, [("H",2), ("O",1)]) ]
            coeffs = (4, 4*x+y, 4*x, 2*y)
            return predicted_reactants, predicted_products, coeffs
    return None

# ------------------------
# Output Formatting Functions
# ------------------------

def molecule_to_str(molecule):
    return "".join([elem + (str(cnt) if cnt != 1 else "") for elem, cnt in molecule])

def format_molecule(mol, coeff):
    s = molecule_to_str(mol)
    return f"{coeff}{s}" if coeff != 1 else s

def terms_to_str(terms, effective_coeffs):
    return " + ".join(format_molecule(terms[i][1], effective_coeffs[i]) for i in range(len(terms)))

def ast_to_human_readable(ast):
    results = []
    for stmt in ast:
        if stmt[0] == "balance":
            _, reactants, products = stmt[1]
            xs = find_balanced_coefficients(reactants, products, max_coeff=10)
            if xs is None:
                results.append("Could not balance reaction.")
            else:
                n_reactants = len(reactants)
                effective_left = [reactants[i][0] * xs[i] for i in range(n_reactants)]
                effective_right = [products[j][0] * xs[n_reactants+j] for j in range(len(products))]
                left_str = terms_to_str(reactants, effective_left)
                right_str = terms_to_str(products, effective_right)
                results.append(f"Balanced Reaction:\n{left_str} -> {right_str}")
        elif stmt[0] == "predict":
            pred = stmt[1]
            if isinstance(pred, tuple):
                if pred[0] == "combustion":
                    predicted = predict_combustion(pred[1])
                elif pred[0] == "synthesis":
                    predicted = predict_synthesis(pred[1])
                elif pred[0] == "decomposition":
                    predicted = predict_decomposition(pred[1])
                elif pred[0] == "single_replacement":
                    predicted = predict_single_replacement(pred[1])
                elif pred[0] == "double_replacement":
                    predicted = predict_double_replacement(pred[1])
                elif pred[0] == "precipitation":
                    predicted = predict_precipitation(pred[1])
                elif pred[0] == "redox":
                    predicted = predict_redox(pred[1])
                elif pred[0] == "acid_base":
                    predicted = predict_acid_base(pred[1])
                else:
                    predicted = None

                if predicted:
                    pred_reactants, pred_products, coeffs = predicted
                    n = len(pred_reactants)
                    eff_left = list(coeffs[:n])
                    eff_right = list(coeffs[n:])
                    left_str = terms_to_str(pred_reactants, eff_left)
                    right_str = terms_to_str(pred_products, eff_right)
                    results.append(f"Predicted {pred[0].capitalize()} Reaction:\n{left_str} -> {right_str}")
                else:
                    results.append(f"Prediction not implemented for: {terms_to_str(pred[1], [t[0] for t in pred[1]])}")
            else:
                results.append("Prediction not implemented for: " + terms_to_str(pred, [t[0] for t in pred]))
    return "\n".join(results)

# ------------------------
# GUI Code
# ------------------------

def process_reaction():
    input_text = reaction_entry.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("Input Required", "Please enter a reaction.")
        status_bar.config(text="No input provided.")
        return
    try:
        result = parse_input(input_text)
        human_readable = ast_to_human_readable(result)
        output_text.config(state='normal')
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, human_readable)
        output_text.config(state='disabled')
        status_bar.config(text="Reaction processed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        status_bar.config(text="Error processing reaction.")

def clear_fields():
    reaction_entry.delete("1.0", tk.END)
    output_text.config(state='normal')
    output_text.delete("1.0", tk.END)
    output_text.config(state='disabled')
    status_bar.config(text="Cleared.")

def exit_app():
    root.quit()

# Initialize main window
root = tk.Tk()
root.title("Chemistry Reaction Balancer & Predictor")
root.geometry("900x650")
root.configure(bg="#f5f5f5")

# Configure style for a modern look
style = ttk.Style(root)
style.theme_use('clam')  # Using clam as a base theme
style.configure("TLabel", background="#f5f5f5", foreground="#333333", font=("Segoe UI", 12))
style.configure("TButton", font=("Segoe UI", 11), padding=6)
style.map("TButton", background=[('active', '#4CAF50')])
style.configure("Header.TLabel", font=("Segoe UI", 22, "bold"), foreground="#2C3E50")
style.configure("TLabelframe", background="#ffffff", foreground="#2C3E50", borderwidth=2)
style.configure("TLabelframe.Label", font=("Segoe UI", 14, "bold"), background="#ffffff")

# Menu Bar
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Clear", command=clear_fields)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About",
    "Chemistry Reaction Balancer & Predictor\nVersion 2025\nBuilt with ChemDSL"))
menu_bar.add_cascade(label="Help", menu=help_menu)
root.config(menu=menu_bar)

# Header Section
header_label = ttk.Label(root, text="Chemistry Reaction Balancer & Predictor", style="Header.TLabel")
header_label.grid(row=0, column=0, columnspan=2, pady=(20, 10), padx=20)

# Input Frame
input_frame = ttk.LabelFrame(root, text="Input Reaction")
input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
reaction_entry = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, width=45, height=12, font=("Segoe UI", 12), relief="flat", borderwidth=2)
reaction_entry.pack(fill="both", expand=True, padx=10, pady=10)
example_text = (
    "balance H2 + O2 -> H2O;\n"
    "predict combustion of CH4;\n"
    "predict synthesis of A + B;\n"
    "predict decomposition of AB;\n"
    "predict single_replacement of A + BC;\n"
    "predict double_replacement of AB + CD;\n"
    "predict precipitation of NaCl + AgNO3;\n"
    "predict redox of Fe + CuSO4;\n"
    "predict acid_base of HCl + NaOH;"
)
reaction_entry.insert(tk.END, example_text)

# Output Frame
output_frame = ttk.LabelFrame(root, text="Output")
output_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, width=45, height=12, font=("Segoe UI", 12), state='disabled', relief="flat", borderwidth=2)
output_text.pack(fill="both", expand=True, padx=10, pady=10)

# Control Buttons Frame
button_frame = ttk.Frame(root)
button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 5))
process_button = ttk.Button(button_frame, text="Process Reaction", command=process_reaction)
process_button.grid(row=0, column=0, padx=10)
clear_button = ttk.Button(button_frame, text="Clear", command=clear_fields)
clear_button.grid(row=0, column=1, padx=10)
exit_button = ttk.Button(button_frame, text="Exit", command=exit_app)
exit_button.grid(row=0, column=2, padx=10)

# Status Bar
status_bar = ttk.Label(root, text="Ready", relief="sunken", anchor="w", font=("Segoe UI", 10))
status_bar.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=(0,10))

# Responsive layout configuration
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

root.mainloop()