import re
from parsec import *

# reconoce cualquier cantidad de espacios en blanco, incluyendo saltos de línea.
whitespace = regex(r'\s*', re.MULTILINE)

# Esto asegura que cualquier parser combinado con lexeme también consuma cualquier espacio en blanco que siga.
lexeme = lambda p: p << whitespace

# Tokens para JSON
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

@lexeme
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
    return (yield (string_literal | number | true | false | null | J))

@generate
def Y():
    """
    Produccion:
		Y -> ,s:VY
			| lambda
    """
    yield comma
    key = yield string_literal
    yield colon
    val = yield value
    
    rest = yield optional(Y, None)
    if rest:
        return [(key, val)] + rest
    return [(key, val)]

@generate
def L():
    """
    Produccion:
		L -> s:VY
    """
    key = yield string_literal
    yield colon
    val = yield value
    
    rest = yield optional(Y, None)
    if rest is not None:
        return [(key, val)] + rest
    return [(key, val)]

@generate
def J_obj():
    """
    Produccion:
		J -> {L}
    """
    yield lbrace
    l = yield optional(L, None)
    yield rbrace
    if l is None:
        return {}
    return dict(l)

@generate
def A():
    """
    Produccion:
		A -> ,VA
            | lambda
    """
    yield comma
    v = yield value
    r = [v]
    a = yield optional(A, None)
    
    if a is not None:
        r += a
    return r

@generate
def X():
    """
    Produccion:
		X -> VA
    """
    v = yield value
    r = [v]
    a = yield optional(A, None)
    
    if a is not None:
        r += a
    return r

@generate
def J_array():
    """
    Produccion:
		J -> [X]
    """
    yield lbrack
    elements = yield optional(X, None)
    yield rbrack
    if elements is None:
        return []
    return elements

"""
Produccion:
    J -> {L}
        | [X]
"""
J = J_obj | J_array

"""
Produccion:
    S -> J  
"""
S = whitespace >> J << eof()