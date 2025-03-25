# ChemDSL

A domain-specific language (DSL) designed to model, predict, and analyze chemical reactions using formal language concepts such as lexical analysis, parsing, and finite-state machines.

## Features
- **Reaction Balancing**: Automatically balances chemical equations.
- **Reaction Prediction**: Supports synthesis and decomposition reaction prediction (expanding to all general reaction types).
- **Combustion Analysis**: Predicts hydrocarbon combustion products.
- **Lexical and Syntax Parsing**: Uses formal grammar techniques for robust chemical reaction interpretation.
- **Error Detection**: Provides validation and feedback on incorrect chemical formulas or reactions.
- **Graphical User Interface (GUI)**: Modern and user-friendly interface for interaction.

## Planned Enhancements
- Expand element support to ~30 elements.
- Implement support for additional reaction types:
  - Single Replacement
  - Double Replacement
  - Precipitation
  - Redox
  - Acid-Base Reactions
- Improve evaluator integration for seamless reaction simulation.
- Enhance the DSL syntax for better flexibility and expressiveness.

## Installation
### Prerequisites
- Python 3.8+
- Required dependencies (install via `pip`):
  ```sh
  pip install -r requirements.txt
  ```

## Usage
1. Clone the repository:
   ```sh
   git clone https://github.com/CmMarin/ChemDSL.git
   cd ChemDSL/DSL
   ```
2. Run the ChemDSL interpreter:
   ```sh
   python main.py
   ```
3. Input a chemical reaction in the DSL syntax and receive predictions and analysis.

## Complete Technical Documentation

### Lexical Analysis (Lexer)
#### 1.1 Token Specification
##### 1.1.1 Keywords
- **Control:** BALANCE, PREDICT, ANALYZE, QUERY, WITH, FOR, OF, INFO, IF
- **Reaction Types:** COMBUSTION, DECOMPOSITION, SINGLE_REPLACEMENT, DOUBLE_REPLACEMENT, ACID_BASE, PRECIPITATION, GAS_FORMATION
- **Thermodynamics:** ENTHALPY, ENTROPY, GIBBS_ENERGY, EQUILIBRIUM
- **Analysis:** OXIDATION_STATES, LIMITING_REAGENT, PERCENT_YIELD, EMPIRICAL_FORMULA, MOLECULAR_FORMULA, MOLAR_MASS
- **Conditions:** CATALYST, TEMPERATURE, PRESSURE, PH, MOLARITY

##### 1.1.2 Literals
- **ELEMENT_SYMBOL:** `[A-Z][a-z]?` (valid chemical symbols)
- **INTEGER:** `\d+`
- **FLOAT:** `\d+.\d*`
- **STRING:** `"[^"]*"`

##### 1.1.3 Operators
- **PLUS:** `+`
- **ARROW:** `->`
- **REVERSIBLE_ARROW:** `<->`
- **LPAREN/RPAREN:** `(`, `)`
- **LBRACKET/RBRACKET:** `[`, `]`
- **COMMA:** `,`
- **SEMICOLON:** `;`

#### 1.2 Lexer Implementation Details
- Implemented using PLY's lex module
- Token precedence rules:
  - Keywords
  - Element symbols
  - Numeric literals
  - Operators
- Special handling for:
  - Case-insensitive keywords (converted to uppercase)
  - Element symbol validation against the periodic table
  - Line number and position tracking for error reporting

#### 1.3 Error Handling
- The lexer raises `SyntaxError` for:
  - Invalid element symbols
  - Malformed numeric literals
  - Unrecognized tokens
  - Unterminated strings

### Syntax Analysis (Parser)
#### 2.1 Grammar Definition
The parser implements an LALR(1) grammar:

##### 2.1.1 Core Productions
```
program : statement_list
statement_list : statement SEMICOLON statement_list
               | statement SEMICOLON
```

##### 2.1.2 Statement Types
```
statement : balance_statement
          | predict_statement
          | analyze_statement
          | reaction_type_statement
          | thermodynamic_statement
          | chemical_analysis_statement
```

##### 2.1.3 Detailed Productions
```
balance_statement : BALANCE reaction_expr
predict_statement : PREDICT reaction_expr
                  | PREDICT reactants_expr
                  | PREDICT reaction_expr IF condition
                  | PREDICT reactants_expr IF condition
analyze_statement : ANALYZE molecule
                  | ANALYZE molecule FOR detail_level
reaction_type_statement : REACTION_TYPE
                        | REACTION_TYPE OF molecule
thermodynamic_statement : THERMO_TYPE OF reaction_expr
                        | THERMO_TYPE INFO reaction_expr
chemical_analysis_statement : ANALYSIS_TYPE OF target
```

##### 2.1.4 Expression Structures
```
reaction_expr : reactants_expr ARROW products_expr
reactants_expr : chemical_term_list
products_expr : chemical_term_list
chemical_term_list : chemical_term PLUS chemical_term_list
                  | chemical_term
chemical_term : INTEGER molecule
              | molecule
molecule : molecule_part molecule
         | molecule_part
molecule_part : element_group
              | LPAREN molecule RPAREN INTEGER
element_group : ELEMENT_SYMBOL INTEGER
              | ELEMENT_SYMBOL
```

#### 2.2 Parser Implementation
- Built using PLY's yacc module
- LALR(1) parsing table with 87 states
- Precedence rules:
  - Parentheses groups
  - Chemical term coefficients
  - Reaction arrows
- AST node construction for each production
- Comprehensive error recovery with:
  - Token synchronization
  - Error productions
  - Panic-mode recovery

### Abstract Syntax Tree (AST)
- **ProgramNode:** Contains a list of statement nodes
- **BalanceStatementNode:** Represents a balance statement
- **ReactionExpressionNode:** Contains reactants and products
- **ChemicalTermNode:** Holds coefficients and molecules
- **ConditionNode:** Represents conditions (e.g., temperature, pressure)

### Evaluation Engine
- **Reaction Balancing:** Uses a matrix-based algorithm
- **Reaction Prediction:** Uses pattern matching and reactivity series
- **Compound Analysis:** Includes molar mass calculation, oxidation state determination

### Example Workflow
#### Input
```
balance Fe + O2 -> Fe2O3;
```
#### Processing Steps
- Lexer produces tokens
- Parser builds AST
- Evaluator processes AST
- **Output:** `4Fe + 3O2 -> 2Fe2O3`


COMPLETE CHEMDSL FORMAL GRAMMAR
================================

## 1. LEXICAL GRAMMAR (TERMINALS)

### 1.1 KEYWORDS:
```
BALANCE     = 'balance'
PREDICT     = 'predict'
ANALYZE     = 'analyze'
FOR         = 'for'
OF          = 'of'
INFO        = 'info'
IF          = 'if'
AND         = 'and'
OR          = 'or'
```

### 1.2 REACTION TYPES:
```
COMBUSTION          = 'combustion'
DECOMPOSITION       = 'decomposition'
SINGLE_REPLACEMENT  = 'single_replacement'
DOUBLE_REPLACEMENT  = 'double_replacement'
ACID_BASE           = 'acid_base'
PRECIPITATION       = 'precipitation'
GAS_FORMATION       = 'gas_formation'
```

### 1.3 THERMODYNAMIC PROPERTIES:
```
ENTHALPY        = 'enthalpy'
ENTROPY         = 'entropy'
GIBBS_ENERGY    = 'gibbs_energy'
EQUILIBRIUM     = 'equilibrium'
```

### 1.4 ANALYSIS TYPES:
```
OXIDATION_STATES    = 'oxidation_states'
LIMITING_REAGENT    = 'limiting_reagent'
PERCENT_YIELD       = 'percent_yield'
EMPIRICAL_FORMULA   = 'empirical_formula'
MOLECULAR_FORMULA   = 'molecular_formula'
MOLAR_MASS          = 'molar_mass'
```

### 1.5 CONDITION TYPES:
```
CATALYST     = 'catalyst'
TEMPERATURE  = 'temperature'
PRESSURE     = 'pressure'
```

### 1.6 LITERALS:
```
ELEMENT_SYMBOL = [A-Z][a-z]? (valid chemical symbol)
INTEGER        = [0-9]+
FLOAT          = [0-9]+.[0-9]*
STRING         = "*?"
```

### 1.7 OPERATORS:
```
PLUS       = '+'
ARROW      = '->'
LPAREN     = '('
RPAREN     = ')'
SEMICOLON  = ';'
```

## 2. SYNTAX GRAMMAR (PRODUCTIONS)

### 2.1 PROGRAM STRUCTURE:
```
<program> ::= <statement_list>

<statement_list> ::= <statement> SEMICOLON
                   | <statement> SEMICOLON <statement_list>
```

### 2.2 STATEMENT TYPES:
```
<balance_statement> ::= BALANCE <reaction_expr>
<predict_statement> ::= PREDICT <reactants_expr>
                      | PREDICT <reaction_expr>
                      | PREDICT <reactants_expr> IF <condition>
                      | PREDICT <reaction_expr> IF <condition>
```

### 2.3 EXPRESSIONS:
```
<reaction_expr> ::= <reactants_expr> ARROW <products_expr>
<reactants_expr> ::= <chemical_term_list>
<products_expr> ::= <chemical_term_list>
```

## 3. SYNTAX CONSTRAINTS

### 3.1 CHEMICAL CONSTRAINTS:
- Element symbols must be valid (from periodic table)
- Parentheses must balance in molecules
- Coefficients must be positive integers
- Reaction arrows must separate reactants/products

### 3.2 SEMANTIC CONSTRAINTS:
- Balance statements must have both sides
- Predict statements require at least reactants
- Analysis targets must be valid compounds
- Conditions must use proper units:
  - Temperature in Celsius ('c' suffix)
  - Pressure in atmospheres ('atm' suffix)

## 4. PRECEDENCE RULES
1. Parentheses (highest precedence)
2. Molecule grouping (e.g., (OH)2)
3. Chemical term coefficients
4. Plus operator (in term lists)
5. Reaction arrow
6. Logical operators (AND/OR)

## 5. GRAMMAR NOTES
- The grammar is LALR(1) with no conflicts
- Terminals are case-insensitive (normalized to lowercase)
- Whitespace is ignored except as token separator
- Semicolon is required as statement terminator
- Empty productions are not allowed

## 6. WELL-FORMEDNESS RULES

### 6.1 MOLECULES MUST:
- Contain at least one element group
- Have balanced parentheses
- Have valid element symbols
- Have integer multipliers > 0

### 6.2 REACTIONS MUST:
- Have at least one reactant
- Have at least one product when using arrow
- Maintain element conservation when balanced

### 6.3 CONDITIONS MUST:
- Use proper comparison operators
- Have valid units where required
- Reference defined variables

## 7. EXAMPLE DERIVATIONS

### 7.1 BALANCE STATEMENT:
```
Input: "balance Fe + O2 -> Fe2O3;"

Derivation:
<program>
→ <statement_list>
→ <statement> SEMICOLON
→ <balance_statement> SEMICOLON
→ BALANCE <reaction_expr> SEMICOLON
→ BALANCE <reactants_expr> ARROW <products_expr> SEMICOLON
→ BALANCE <chemical_term_list> ARROW <chemical_term_list> SEMICOLON
→ BALANCE <chemical_term> PLUS <chemical_term> ARROW <chemical_term> SEMICOLON
→ BALANCE [INTEGER] <molecule> PLUS [INTEGER] <molecule> ARROW [INTEGER] <molecule> SEMICOLON
→ balance Fe + O2 -> Fe2O3;
```

### 7.2 PREDICT STATEMENT WITH CONDITION:
```
Input: "predict H2 + O2 if temperature(500c) and pressure(2atm);"

Derivation:
<program>
→ <statement_list>
→ <statement> SEMICOLON
→ <predict_statement> SEMICOLON
→ PREDICT <reactants_expr> IF <condition> SEMICOLON
→ predict H2 + O2 if temperature(500c) and pressure(2atm);
```
