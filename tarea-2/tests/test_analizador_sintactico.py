import sys
import os

# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.precedencia import *
from src.gramatica import *
from src.parser import *

if __name__ == "__main__":
	prueba = Precedence()
	prueba.set_precedence('+', '+', '>')
	prueba.set_precedence('+', '*', '<')
	prueba.set_precedence('+', 'n', '<')
	prueba.set_precedence('+', '(', '<')
	prueba.set_precedence('+', ')', '>')
	prueba.set_precedence('+', '$', '>')
	
	prueba.set_precedence('*', '+', '>')
	prueba.set_precedence('*', '*', '>')
	prueba.set_precedence('*', 'n', '<')
	prueba.set_precedence('*', '(', '<')
	prueba.set_precedence('*', ')', '>')
	prueba.set_precedence('*', '$', '>')

	prueba.set_precedence('n', '+', '>')
	prueba.set_precedence('n', '*', '>')
	prueba.set_precedence('n', ')', '>')
	prueba.set_precedence('n', '$', '>')

	prueba.set_precedence("(", "+", "<")
	prueba.set_precedence("(", "*", "<")
	prueba.set_precedence("(", "n", "<")
	prueba.set_precedence("(", "(", "<")
	prueba.set_precedence("(", ")", "=")

	prueba.set_precedence(")", "+", ">")
	prueba.set_precedence(")", "*", ">")
	prueba.set_precedence(")", ")", ">")
	prueba.set_precedence(")", "$", ">")

	prueba.set_precedence('$', '+', '<')
	prueba.set_precedence('$', '*', '<')
	prueba.set_precedence('$', 'n', '<')
	prueba.set_precedence('$', '(', '<')

	gramatica = Grammar(_precedence = prueba)
	gramatica.add_rule("E", "E + E")
	gramatica.add_rule("E", "E * E")
	gramatica.add_rule("E", "n")
	parser = Parser(gramatica)

	parser.create_input_string("n + n * n")
	parser.parse()