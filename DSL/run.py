# run.py
from DSL.parser import parse
from DSL.interpreter.evaluator_dsl import Evaluator

def main():
    # Example ChemDSL code: you can replace this with your own DSL code.
    code = """
    balance N2 + O2 -> N2O5;
    balance H2 + O2 -> H2O;

    """
    # Parse the code to get the AST.
    ast = parse(code)
    # Create an evaluator instance.
    evaluator = Evaluator()
    # Evaluate the AST.
    output = evaluator.evaluate(ast)
    print(output)

if __name__ == "__main__":
    main()
