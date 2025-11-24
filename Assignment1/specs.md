# Specifications — Calculator CFG

This document describes the internal logic, methods, and overall flow of the `calculator_cfg.py` implementation.

---

## 1. Overview

The calculator program is a command-line tool that evaluates mathematical expressions according to a context-free grammar defined in `grammar.lark`.  
It supports the following operations:

- Addition (`+`)
- Subtraction (`-`)
- Multiplication (`*`)
- Exponentiation (`^`)
- Unary negation (e.g. `-3`)
- Logarithms with arbitrary base (`log <value> base <base>`)

The program uses the **Lark** parsing library to parse input strings into an abstract syntax tree (AST).  
A custom transformer (`CalcTransformer`) converts the parse tree into a simplified internal AST representation.  
The `evaluate()` function then recursively computes the final numeric result.

---

## 2. File Structure

Assignment1/
├── calculator_cfg.py
└── grammar.lark

- **`calculator_cfg.py`** — main Python program implementing parsing, transformation, and evaluation.  
- **`grammar.lark`** — Lark grammar defining the syntax rules for valid calculator expressions.

---

## 3. Program Flow

1. The program reads `grammar.lark` from the same directory as the script.  
2. The grammar is passed to `Lark()` to create a parser.  
3. The user’s expression is taken from the command-line argument.  
4. The expression is parsed into a syntax tree.  
5. The `CalcTransformer` converts the parse tree into a simplified tuple-based AST.  
6. The `evaluate()` function recursively computes the numeric result.  
7. The result is printed. If the result is an integer-valued float, it is printed without a decimal.

---

## 4. Classes and Methods

### `CalcTransformer(Transformer)`

Responsible for converting the raw Lark parse tree into a simpler internal AST that can be easily evaluated.  
Each method corresponds to a grammar rule in `grammar.lark`.

| Method | Purpose | Returns |
|---------|----------|----------|
| `num(self, items)` | Converts numeric tokens (strings) into numeric tuples. | `('num', float_value)` |
| `plus(self, items)` | Represents an addition node. | `('plus', left_ast, right_ast)` |
| `minus(self, items)` | Represents a subtraction node. | `('minus', left_ast, right_ast)` |
| `times(self, items)` | Represents a multiplication node. | `('times', left_ast, right_ast)` |
| `power(self, items)` | Represents an exponentiation node. | `('power', base_ast, exponent_ast)` |
| `neg(self, items)` | Represents a unary negation (e.g., `-3`). | `('neg', value_ast)` |
| `logbase(self, items)` | Represents a logarithm operation with a given base. | `('logbase', value_ast, base_ast)` |

---

## 5. Function: `evaluate(ast)`

This function performs recursive evaluation of the AST produced by `CalcTransformer`.

### Parameters

- `ast` — A tuple representing an AST node.

### Logic

| Node Type | Operation |
|------------|------------|
| `'num'` | Returns the numeric value. |
| `'plus'` | Returns the sum of left and right subexpressions. |
| `'minus'` | Returns the difference of left and right subexpressions. |
| `'times'` | Returns the product of left and right subexpressions. |
| `'power'` | Returns the base raised to the exponent. |
| `'neg'` | Returns the negation of the subexpression. |
| `'logbase'` | Computes the logarithm of a value with a given base using `math.log(val, base)`. |

Invalid node types raise a `ValueError`.

---

## 6. Main Execution Logic
1. Validates that an expression argument was provided.
2. Parses the expression using parser.parse(input_string).
3. Transforms the parse tree with CalcTransformer.
4. Calls evaluate(ast) to compute the result.
5. Prints the result:
6. If the result is nearly an integer (difference < 1e−12), it prints as an integer.
7. Otherwise, it prints the full floating-point value.

---

## 7. Error Handling

If the input expression cannot be parsed according to the grammar, Lark will raise a syntax error.

Invalid math inputs (e.g., log -5 base 2) will raise a ValueError from math.log().

The program exits with an error message if no expression is provided.