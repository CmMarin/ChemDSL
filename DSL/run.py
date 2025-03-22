from DSL.parser import parse
from DSL.interpreter.evaluator_dsl import Evaluator

code = "balance H2O -> H2 + O2;"
ast = parse(code)
evaluator = Evaluator()
print(evaluator.evaluate(ast))