import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import itertools
import ply.lex as lex
import ply.yacc as yacc
import re

# ------------------------
# DSL Code for ChemDSL
# ------------------------

# Lexer tokens
tokens = (
    'BALANCE', 'PREDICT', 'COMBUSTION', 'SYNTHESIS', 'DECOMPOSITION', 'SINGLE_REPLACEMENT',
    'DOUBLE_REPLACEMENT', 'PRECIPITATION', 'REDOX', 'ACID_BASE', 'OF',
    'ELEMENT_SYMBOL', 'DIGITS', 'PLUS', 'ARROW', 'SEMICOLON', 'LPAREN', 'RPAREN'
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
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_ELEMENT_SYMBOL(t):
    r'[A-Z][a-z]?'
    return t

def t_DIGITS(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_WHITESPACE(t):
    r'[ \t\r\n]+'
    pass

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# ------------------------
# Parser Rules
# ------------------------

def p_program(p):
    '''program : statement_list'''
    p[0] = p[1]

def p_statement_list_multiple(p):
    '''statement_list : statement SEMICOLON statement_list'''
    p[0] = [p[1]] + p[3]

def p_statement_list_single(p):
    '''statement_list : statement SEMICOLON'''
    p[0] = [p[1]]

# Prediction rules
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
    '''chemical_expr : molecule
                     | LPAREN molecule RPAREN DIGITS
                     | LPAREN molecule RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 5:
        result = []
        for elem, count in p[2]:
            result.append((elem, count * p[4]))
        p[0] = result
    else:
        p[0] = p[2]

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

# Helper to convert molecule structure to formula string
def get_molecule_formula(molecule):
    return "".join([elem + (str(cnt) if cnt > 1 else "") for elem, cnt in molecule])

# ------------------------
# Reaction Prediction Logic
# ------------------------

# Common element charges, electronegativity, and activity series for simple predictions
ELEMENT_CHARGES = {
    'H': 1, 'Li': 1, 'Na': 1, 'K': 1, 'Mg': 2, 'Ca': 2,
    'O': -2, 'F': -1, 'Cl': -1, 'Br': -1, 'I': -1, 'N': -3,
    'C': 4, 'P': -3, 'S': -2, 'Fe': 3, 'Cu': 2, 'Zn': 2,
    'Ag': 1, 'Al': 3, 'Ba': 2, 'Pb': 2,
}

ELECTRONEGATIVITY = {
    'H': 2.20, 'Li': 0.98, 'Na': 0.93, 'K': 0.82, 'Mg': 1.31, 'Ca': 1.00,
    'O': 3.44, 'F': 3.98, 'Cl': 3.16, 'Br': 2.96, 'I': 2.66, 'N': 3.04,
    'C': 2.55, 'P': 2.19, 'S': 2.58, 'Fe': 1.83, 'Cu': 1.90, 'Zn': 1.65,
    'Ag': 1.93, 'Al': 1.61, 'Ba': 0.89, 'Pb': 1.87,
}

ACTIVITY_SERIES = {
    'K': 10, 'Na': 9, 'Ca': 8, 'Mg': 7, 'Al': 6,
    'Zn': 5, 'Fe': 4, 'Pb': 3, 'H': 2, 'Cu': 1, 'Ag': 0,
}

def predict_synthesis(reactants):
    if len(reactants) != 2:
        return None
    r1, r2 = reactants
    # If both are simple elements, try to combine using their charges
    if len(r1[1]) == 1 and len(r2[1]) == 1:
        elem1, _ = r1[1][0]
        elem2, _ = r2[1][0]
        if elem1 in ELEMENT_CHARGES and elem2 in ELEMENT_CHARGES:
            charge1 = ELEMENT_CHARGES[elem1]
            charge2 = ELEMENT_CHARGES[elem2]
            if charge1 * charge2 < 0:
                abs1, abs2 = abs(charge1), abs(charge2)
                gcd = abs1
                for i in range(min(abs1, abs2), 0, -1):
                    if abs1 % i == 0 and abs2 % i == 0:
                        gcd = i
                        break
                sub1 = abs2 // gcd
                sub2 = abs1 // gcd
                # Special case for diatomic elements
                if elem2 in ['O', 'H', 'N', 'F', 'Cl', 'Br', 'I']:
                    product = [(elem1, sub1 * 2), (elem2, sub2)]
                    return [(2, r1[1]), (1, [(elem2, 2)])], [(2, product)], (2, 1, 2)
                product = [(elem1, sub1), (elem2, sub2)]
                return [(1, r1[1]), (1, r2[1])], [(1, product)], (1, 1, 1)
    # Default: combine formulas
    product = r1[1] + r2[1]
    return [(1, r1[1]), (1, r2[1])], [(1, product)], (1, 1, 1)

def predict_decomposition(reactants):
    if len(reactants) != 1:
        return None
    r1 = reactants[0]
    mol = r1[1]
    formula = get_molecule_formula(mol)
    carbonate_pattern = r'([A-Z][a-z]*)CO3'
    match = re.match(carbonate_pattern, formula)
    if match:
        metal = match.group(1)
        metal_oxide = [(metal, 1), ('O', 1)]
        co2 = [('C', 1), ('O', 2)]
        return [(1, mol)], [(1, metal_oxide), (1, co2)], (1, 1, 1)
    hydroxide_pattern = r'([A-Z][a-z]*)\(OH\)(\d*)'
    match = re.match(hydroxide_pattern, formula)
    if match:
        metal = match.group(1)
        n = int(match.group(2)) if match.group(2) else 1
        metal_oxide = [(metal, 1), ('O', 1)]
        water = [('H', 2), ('O', 1)]
        return [(1, mol)], [(1, metal_oxide), (n, water)], (1, 1, n)
    if formula == "H2O2":
        water = [('H', 2), ('O', 1)]
        oxygen = [('O', 2)]
        return [(2, mol)], [(2, water), (1, oxygen)], (2, 2, 1)
    mid = len(mol) // 2
    product1 = mol[:mid]
    product2 = mol[mid:]
    if not product1:
        product1 = [mol[0]]
        product2 = mol[1:]
    elif not product2:
        product1 = mol[:-1]
        product2 = [mol[-1]]
    return [(1, mol)], [(1, product1), (1, product2)], (1, 1, 1)

def predict_single_replacement(reactants):
    if len(reactants) != 2:
        return None
    r1, r2 = reactants
    # Handle acid special case
    r2_formula = get_molecule_formula(r2[1])
    if r2_formula.startswith('H') and len(r2[1]) >= 2:
        metal = r1[1][0][0]
        for i, (elem, _) in enumerate(r2[1]):
            if elem == 'H':
                new_compound = r2[1].copy()
                new_compound[i] = (metal, 1)
                h2 = [('H', 2)]
                return [(1, r1[1]), (1, r2[1])], [(1, new_compound), (1, h2)], (1, 1, 1, 1)
    # General single replacement: A + BC → AC + B
    if len(r1[1]) == 1 and len(r2[1]) > 1:
        element = r1[1][0][0]
        element_charge = ELEMENT_CHARGES.get(element)
        if element_charge is not None:
            for i, (comp_element, count) in enumerate(r2[1]):
                comp_charge = ELEMENT_CHARGES.get(comp_element)
                if comp_charge is not None and (comp_charge * element_charge > 0):
                    if element in ACTIVITY_SERIES and comp_element in ACTIVITY_SERIES:
                        if ACTIVITY_SERIES[element] > ACTIVITY_SERIES[comp_element]:
                            new_compound = r2[1].copy()
                            new_compound[i] = (element, count)
                            displaced = [(comp_element, 1)]
                            return [(1, r1[1]), (1, r2[1])], [(1, new_compound), (1, displaced)], (1, 1, 1, 1)
    product1 = r1[1][:1] + r2[1][1:]
    product2 = [r2[1][0]]
    return [(1, r1[1]), (1, r2[1])], [(1, product1), (1, product2)], (1, 1, 1, 1)

def predict_double_replacement(reactants):
    if len(reactants) != 2:
        return None
    r1, r2 = reactants
    if len(r1[1]) == 2 and len(r2[1]) == 2:
        A, B = r1[1][0][0], r1[1][1][0]
        C, D = r2[1][0][0], r2[1][1][0]
        countA, countB = r1[1][0][1], r1[1][1][1]
        countC, countD = r2[1][0][1], r2[1][1][1]
        product1 = [(A, countA), (D, countD)]
        product2 = [(C, countC), (B, countB)]
        return [(1, r1[1]), (1, r2[1])], [(1, product1), (1, product2)], (1, 1, 1, 1)
    mid1 = len(r1[1]) // 2
    mid2 = len(r2[1]) // 2
    product1 = r1[1][:mid1] + r2[1][mid2:]
    product2 = r2[1][:mid2] + r1[1][mid1:]
    return [(1, r1[1]), (1, r2[1])], [(1, product1), (1, product2)], (1, 1, 1, 1)

def predict_precipitation(reactants):
    solubility_rules = {
        "Na": "soluble", "K": "soluble", "NH4": "soluble",
        "Cl": "soluble", "NO3": "soluble", "SO4": "soluble",
        "CO3": "insoluble", "PO4": "insoluble", "S": "insoluble",
        "OH": "insoluble", "Ag": "insoluble", "Pb": "insoluble",
        "Ba": "insoluble",
    }
    if len(reactants) != 2:
        return None
    r1, r2 = reactants
    predicted = predict_double_replacement(reactants)
    if predicted:
        _, products, _ = predicted
        product1, product2 = products
        p1_formula = get_molecule_formula(product1[1])
        p2_formula = get_molecule_formula(product2[1])
        # Special case for AgCl
        if "AgCl" in p1_formula or "AgCl" in p2_formula:
            if "AgCl" in p1_formula:
                return [(1, r1[1]), (1, r2[1])], [product1, product2], (1, 1, 1, 1)
            else:
                return [(1, r1[1]), (1, r2[1])], [product2, product1], (1, 1, 1, 1)
        precip_product = None
        other_product = None
        for product, formula in [(product1, p1_formula), (product2, p2_formula)]:
            for ion, sol in solubility_rules.items():
                if ion in formula and sol == "insoluble":
                    precip_product = product
                    other_product = product2 if product == product1 else product1
                    break
            if precip_product:
                break
        if precip_product:
            return [(1, r1[1]), (1, r2[1])], [precip_product, other_product], (1, 1, 1, 1)
    return predicted

def predict_redox(reactants):
    if len(reactants) != 2:
        return None
    r1, r2 = reactants
    if len(r1[1]) == 1 and r1[1][0][0] in ELEMENT_CHARGES:
        metal1 = r1[1][0][0]
        if metal1 in ACTIVITY_SERIES:
            for i, (element, count) in enumerate(r2[1]):
                if element in ACTIVITY_SERIES:
                    if ACTIVITY_SERIES[metal1] > ACTIVITY_SERIES[element]:
                        new_compound = r2[1].copy()
                        new_compound[i] = (metal1, count)
                        displaced = [(element, 1)]
                        return [(1, r1[1]), (1, r2[1])], [(1, new_compound), (1, displaced)], (1, 1, 1, 1)
    return predict_single_replacement(reactants)

def predict_acid_base(reactants):
    if len(reactants) != 2:
        return None
    acid = None
    base = None
    for r in reactants:
        formula = get_molecule_formula(r[1])
        if formula.startswith('H') and not formula.startswith('H2O'):
            acid = r
        elif 'OH' in formula:
            base = r
    if acid and base:
        metal = base[1][0][0] if base[1] else 'Na'
        anion = []
        h_found = False
        for elem, cnt in acid[1]:
            if elem == 'H':
                h_found = True
            elif h_found:
                anion.append((elem, cnt))
        if not anion and len(acid[1]) > 1:
            anion = [acid[1][1]]
        if not anion:
            anion = [('Cl', 1)]
        salt = [(metal, 1)] + anion
        water = [('H', 2), ('O', 1)]
        return [(1, acid[1]), (1, base[1])], [(1, salt), (1, water)], (1, 1, 1, 1)
    return predict_double_replacement(reactants)

def predict_combustion(reactants):
    if not reactants:
        return None
    hydrocarbon = None
    for r in reactants:
        elements = set(elem for elem, _ in r[1])
        if elements.issubset({'C', 'H'}) and 'C' in elements:
            hydrocarbon = r
            break
    if not hydrocarbon:
        return None
    c_count = sum(count for elem, count in hydrocarbon[1] if elem == 'C')
    h_count = sum(count for elem, count in hydrocarbon[1] if elem == 'H')
    if c_count == 0:
        return None
    o2_count = c_count + h_count / 4
    co2 = [('C', 1), ('O', 2)]
    h2o = [('H', 2), ('O', 1)]
    multiplier = 4 if h_count % 4 != 0 else 1
    c_coeff = int(c_count * multiplier)
    h_coeff = int(h_count * multiplier / 2)
    o2_coeff = int((c_count + h_count / 4) * multiplier)
    return [(multiplier, hydrocarbon[1]), (o2_coeff, [('O', 2)])], [(c_coeff, co2), (h_coeff, h2o)], (multiplier, o2_coeff, c_coeff, h_coeff)

# ------------------------
# Balancing Engine
# ------------------------

def is_balanced(reactants, products, xs):
    n_reactants = len(reactants)
    elements = set()
    for term in reactants + products:
        for elem, cnt in term[1]:
            elements.add(elem)
    for elem in elements:
        left_sum = sum(reactants[i][0] * xs[i] * next((cnt for (el, cnt) in reactants[i][1] if el == elem), 0)
                        for i in range(n_reactants))
        right_sum = sum(products[j][0] * xs[n_reactants+j] * next((cnt for (el, cnt) in products[j][1] if el == elem), 0)
                         for j in range(len(products)))
        if left_sum != right_sum:
            return False
    return True

def find_balanced_coefficients(reactants, products, max_coeff=10):
    total = len(reactants) + len(products)
    best_xs = None
    for xs in itertools.product(range(1, max_coeff + 1), repeat=total):
        if is_balanced(reactants, products, xs):
            if best_xs is None or sum(xs) < sum(best_xs):
                best_xs = xs
                if sum(xs) <= total * 2:
                    break
    return best_xs

# ------------------------
# Output Formatting Functions
# ------------------------

def molecule_to_str(molecule):
    result = ""
    for elem, cnt in molecule:
        result += elem + (str(cnt) if cnt != 1 else "")
    return result

def format_molecule(mol, coeff):
    s = molecule_to_str(mol)
    return f"{coeff}{s}" if coeff != 1 else s

def terms_to_str(terms, effective_coeffs):
    return " + ".join(format_molecule(terms[i][1], effective_coeffs[i]) for i in range(len(terms)))

def ast_to_human_readable(ast):
    results = []
    if not ast:
        return "No valid statements found. Please check your input syntax."
    for stmt in ast:
        try:
            if stmt[0] == "balance":
                reaction_info = stmt[1]
                if reaction_info[0] == "reaction":
                    _, reactants, products = reaction_info
                    xs = find_balanced_coefficients(reactants, products)
                    if xs is None:
                        results.append("Could not balance reaction. Please check the chemical formulas.")
                    else:
                        n_reactants = len(reactants)
                        effective_left = [reactants[i][0] * xs[i] for i in range(n_reactants)]
                        effective_right = [products[j][0] * xs[n_reactants + j] for j in range(len(products))]
                        left_str = terms_to_str(reactants, effective_left)
                        right_str = terms_to_str(products, effective_right)
                        results.append(f"Balanced Reaction:\n{left_str} -> {right_str}")
                else:
                    results.append("Invalid reaction format.")
            elif stmt[0] == "predict":
                pred = stmt[1]
                if isinstance(pred, tuple) and len(pred) == 2:
                    reaction_type, reactants = pred
                    if reaction_type == "combustion":
                        predicted = predict_combustion(reactants)
                    elif reaction_type == "synthesis":
                        predicted = predict_synthesis(reactants)
                    elif reaction_type == "decomposition":
                        predicted = predict_decomposition(reactants)
                    elif reaction_type == "single_replacement":
                        predicted = predict_single_replacement(reactants)
                    elif reaction_type == "double_replacement":
                        predicted = predict_double_replacement(reactants)
                    elif reaction_type == "precipitation":
                        predicted = predict_precipitation(reactants)
                    elif reaction_type == "redox":
                        predicted = predict_redox(reactants)
                    elif reaction_type == "acid_base":
                        predicted = predict_acid_base(reactants)
                    else:
                        predicted = None
                        results.append(f"Unknown reaction type: {reaction_type}")
                    if predicted:
                        pred_reactants, pred_products, coeffs = predicted
                        n = len(pred_reactants)
                        eff_left = list(coeffs[:n])
                        eff_right = list(coeffs[n:])
                        left_str = terms_to_str(pred_reactants, eff_left)
                        right_str = terms_to_str(pred_products, eff_right)
                        results.append(f"Predicted {reaction_type.capitalize()} Reaction:\n{left_str} -> {right_str}")
                    else:
                        reactants_str = terms_to_str(reactants, [t[0] for t in reactants])
                        results.append(f"Couldn't predict a {reaction_type} reaction for: {reactants_str}")
                else:
                    results.append("Invalid prediction format.")
            else:
                results.append(f"Unknown statement type: {stmt[0]}")
        except Exception as e:
            results.append(f"Error processing statement: {e}")
    return "\n\n".join(results)

# ------------------------
# GUI Implementation
# ------------------------

class ChemDSLApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ChemDSL Interpreter")
        self.root.geometry("900x650")
        self.root.configure(bg="#f5f5f5")

        # Set up the style for a modern look
        style = ttk.Style(root)
        style.theme_use('clam')
        style.configure("TFrame", background="#f5f5f5")
        style.configure("TLabel", background="#f5f5f5", foreground="#333333", font=("Segoe UI", 12))
        style.configure("Header.TLabel", font=("Segoe UI", 22, "bold"), foreground="#2C3E50")
        style.configure("TButton", font=("Segoe UI", 11), padding=6)
        style.map("TButton", background=[("active", "#4CAF50")])

        # Create a menu bar
        self.menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Clear", command=self.clear_output)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=self.menu_bar)

        # Header
        header = ttk.Label(self.root, text="ChemDSL Interpreter", style="Header.TLabel")
        header.pack(pady=(20, 10))

        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(expand=True, fill="both")

        # Input frame
        input_frame = ttk.LabelFrame(self.main_frame, text="Input ChemDSL Code")
        input_frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.input_text = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, font=("Segoe UI", 12), height=10)
        self.input_text.pack(expand=True, fill="both", padx=10, pady=10)

        # Output frame
        output_frame = ttk.LabelFrame(self.main_frame, text="Output")
        output_frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, font=("Segoe UI", 12), height=15,
                                                     state="disabled")
        self.output_text.pack(expand=True, fill="both", padx=10, pady=10)

        # Command buttons frame
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.pack(fill="x", padx=10, pady=5)
        self.add_button(buttons_frame, "Balance", self.insert_balance)
        self.add_button(buttons_frame, "Predict", self.insert_predict)
        self.add_button(buttons_frame, "->", self.insert_arrow)
        self.add_button(buttons_frame, "+", self.insert_plus)
        self.add_button(buttons_frame, ";", self.insert_semicolon)

        # Run and Clear buttons frame
        run_clear_frame = ttk.Frame(self.main_frame)
        run_clear_frame.pack(fill="x", padx=10, pady=5)
        self.add_button(run_clear_frame, "Run", self.run_code)
        self.add_button(run_clear_frame, "Clear", self.clear_output)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w",
                                    font=("Segoe UI", 10))
        self.status_bar.pack(fill="x", padx=10, pady=(0, 10))

    def add_button(self, parent, text, command):
        btn = ttk.Button(parent, text=text, command=command)
        btn.pack(side=tk.LEFT, padx=5, pady=5)

    def insert_balance(self):
        self.input_text.insert(tk.END, "balance ")
        self.input_text.focus()

    def insert_predict(self):
        self.input_text.insert(tk.END, "predict ")
        self.input_text.focus()

    def insert_arrow(self):
        self.input_text.insert(tk.END, " -> ")
        self.input_text.focus()

    def insert_plus(self):
        self.input_text.insert(tk.END, " + ")
        self.input_text.focus()

    def insert_semicolon(self):
        self.input_text.insert(tk.END, ";")
        self.input_text.focus()

    def run_code(self):
        code = self.input_text.get("1.0", tk.END).strip()
        if not code:
            messagebox.showwarning("Input Error", "Please enter some ChemDSL code.")
            self.status_var.set("No input provided.")
            return
        try:
            # Assume parse_input and ast_to_human_readable are available from the DSL part
            ast = parse_input(code)
            output = ast_to_human_readable(ast)
            self.status_var.set("Code executed successfully.")
        except Exception as e:
            output = f"Error: {str(e)}"
            self.status_var.set("Error during execution.")
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, output)
        self.output_text.config(state="disabled")

    def clear_output(self):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state="disabled")
        self.status_var.set("Cleared.")

    def show_about(self):
        messagebox.showinfo("About", "ChemDSL Interpreter\nVersion 2025\nBuilt with ChemDSL.")


# ------------------------
# Main Application Entry Point
# ------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = ChemDSLApp(root)
    root.mainloop()
