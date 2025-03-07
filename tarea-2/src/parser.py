from .gramatica import *
from dataclasses import dataclass, field
import typing as t

@dataclass
class Parser:
	"""
		Clase para manejar el parser del analizador sintactico.

		Atributos
			- _grammar: gramatica del analizador sintactico

			- _terminal_token: token terminal de la gramatica

			- _f: diccionario de precedencia f

			- _g: diccionario de precedencia g
	"""
	_grammar: Grammar
	_terminal_token: str = '$'
	_f: dict = field(default_factory=dict)
	_g: dict = field(default_factory=dict)
	
	# funcion para crear la cadena de entrada
	def create_input_string(self, input_string: str) -> str:
		input_string = "".join(input_string.split())
		new_input = self._terminal_token + input_string + self._terminal_token
		result = self._terminal_token
		for i in range(1 ,len(new_input)):
			precedence = self._grammar.get_precedence_in_grammar(new_input[i-1], new_input[i])
			result += precedence + new_input[i]
		return result
	
	# funcion para establecer los diccionarios de precedencia f y g
	def set_fg(self, f: dict, g: dict) -> None:
		self._f, self._g = f, g
	
	# funcion para parsear la cadena de entrada
	def parse(self, input_string: str) -> None:
		stack = ['$']
		precedence_stack = ['$']
		index = 1
		print(f"{'Pila':<30}{'Entrada':<30}{'Acción'}")
		print(f"{'-'*70}")
		
		while True:
			top = precedence_stack[-1]
			current = input_string[index]
			
			visible_stack = [s.strip('<>') for s in stack]
			print(f"{' '.join(visible_stack):<30}{input_string[index:]:<30}", end='')
			
			if top == '$' and current == '$':
				print("Aceptar")
				break
			
			if current != '$':
				print(f"Desplazar {current.strip('<>')}")
				stack.append(current)
				precedence_stack.append(current)
				index += 1
			else:
				print(f"Reducir")
				stack.pop()
				precedence_stack.pop()

