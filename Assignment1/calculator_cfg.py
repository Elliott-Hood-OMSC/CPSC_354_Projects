import os
import sys
import math
from lark import Lark, Transformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, "grammar.lark"), "r") as f:
    grammar = f.read()

parser = Lark(grammar, parser="lalr")

class CalcTransformer(Transformer):
    def num(self, items):
        # Lark gives the number token as a string
        return ('num', float(items[0]))

    def plus(self, items):
        return ('plus', items[0], items[1])

    def minus(self, items):
        return ('minus', items[0], items[1])

    def times(self, items):
        return ('times', items[0], items[1])

    def power(self, items):
        return ('power', items[0], items[1])

    def neg(self, items):
        return ('neg', items[0])

    def logbase(self, items):
        # items[0] is the value, items[1] is the base
        return ('logbase', items[0], items[1])

def evaluate(ast):
    kind = ast[0]
    if kind == 'num':
        return ast[1]
    if kind == 'plus':
        return evaluate(ast[1]) + evaluate(ast[2])
    if kind == 'minus':
        return evaluate(ast[1]) - evaluate(ast[2])
    if kind == 'times':
        return evaluate(ast[1]) * evaluate(ast[2])
    if kind == 'power':
        return evaluate(ast[1]) ** evaluate(ast[2])
    if kind == 'neg':
        return -evaluate(ast[1])
    if kind == 'logbase':
        val = evaluate(ast[1])
        base = evaluate(ast[2])
        # math.log(x, base) raises ValueError for invalid values; let it propagate
        return math.log(val, base)
    raise ValueError(f"Unknown AST node: {ast}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python calculator_cfg.py \"<expression>\"")
        sys.exit(1)

    input_string = sys.argv[1]
    tree = parser.parse(input_string)
    ast = CalcTransformer().transform(tree)
    result = evaluate(ast)
    # If the result is an integer-valued float, print as int to match expected
    if abs(result - round(result)) < 1e-12:
        # print integer without decimal point
        print(int(round(result)))
    else:
        print(result)
