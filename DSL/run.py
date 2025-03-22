from DSL.parser import parse
from DSL.interpreter.evaluator_dsl import Evaluator

code = "predict N2 + O2;"
ast = parse(code)
evaluator = Evaluator()
print(evaluator.evaluate(ast))