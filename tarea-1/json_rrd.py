import re
from parsec import *

whitespace = regex(r'\s*', re.MULTILINE)

# lexer para JSON
lexeme = lambda p: p << whitespace

lbrace = lexeme(string('{'))
rbrace = lexeme(string('}'))
lbrack = lexeme(string('['))
rbrack = lexeme(string(']'))
colon = lexeme(string(':'))
comma = lexeme(string(','))
true = lexeme(string('true')).result(True)
false = lexeme(string('false')).result(False)
null = lexeme(string('null')).result(None)
number = lexeme(regex(r'-?\d+(\.\d+)?([eE][+-]?\d+)?')).parsecmap(float)
string_literal = lexeme(regex(r'"(\\.|[^"\\])*"')).parsecmap(lambda s: s[1:-1])

# gramática para JSON
"""
S -> J
J -> {L}
	| [X]
"""
@generate
def value():
    """
    Produccion:
		V -> s
			| n
			| true
			| false
			| null
			| J
    """
    return (yield (string_literal | number | true | false | null | obj | array))

@generate
def pair():
    """
	Produccion:
		L -> s:VY
    """
    key = yield string_literal
    yield colon
    val = yield value
    return (key, val)

@generate
def obj():
    """
    Produccion:
		Y -> ,s:VY
			| lambda
    """
    yield lbrace
    pairs = yield sepBy(pair, comma)
    yield rbrace
    return dict(pairs)

@generate
def array():
    yield lbrack
    values = yield sepBy(value, comma)
    yield rbrack
    return values

json_parser = whitespace >> (obj | array)
"""
X -> VA
A -> ,X
	| lambda
"""