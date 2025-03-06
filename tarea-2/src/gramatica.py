from dataclasses import dataclass, field
import typing as t
from .precedencia import Precedence

@dataclass
class Grammar:
	"""
		Clase para manejar las gramaticas del parser.

		Atributos
			- start_symbol: simbolo inicial de la gramatica

			- rules: diccionario de reglas de la gramatica

			- predecence: diccionario de precedencia entre 
						  simbolos terminales de la gramatica
		
		Funciones:
			- add_rule: agrega una nueva regla a la gramatica.

			- set_start_symbol: establece el simbolo inicial de 
								la gramatica.

			- set_precedence: establece la precedencia entre dos
							  simbolos no terminales.
	"""
	_start_symbol: str = ""
	_rules: dict[str, list[str]] = field(default_factory=dict)
	_precedence: Precedence = field(default_factory=Precedence)

	def is_terminal_symbol(self, symbol: str) -> bool:
		# Verificar que todos los caracteres sean ASCII, que la cadena no contenga '$',
		# que no tenga letras mayúsculas ni números
		return (len(symbol) >= 1 and
				symbol.isascii() and
				'$' not in symbol and
				not any(char.isupper() for char in symbol) and
				not any(char.isdigit() for char in symbol))
	
	def is_valid_production(self, non_terminal: str, production: list) -> bool:
		# Verificar si es una producción vacía (lambda)
		if production == []:
			# Solo el símbolo inicial puede generar lambda
			return non_terminal == self._start_symbol
		
		# Verificar que no haya dos símbolos no terminales adyacentes
		prev_is_non_terminal = False
		
		for char in production:
			current_is_non_terminal = char.isupper()
			
			# Si el carácter actual y el anterior son no terminales, la producción no es válida
			if current_is_non_terminal and prev_is_non_terminal:
				return False
			
			prev_is_non_terminal = current_is_non_terminal
		
		return True

	def add_rule(self, non_terminal: str, production: list) -> str:
		is_non_terminal = not self.is_terminal_symbol(non_terminal)
		is_valid_production = self.is_valid_production(non_terminal, production)
		
		if is_non_terminal and is_valid_production:
			self._rules.setdefault(non_terminal, []).append(production)
			return f"Regla \"{non_terminal} -> {' '.join(production)}\" agregada a la gramatica"
		else:
			if not is_non_terminal:
				raise Exception(f"ERROR: '{non_terminal}' no es un símbolo no-terminal válido.")
			
			if not is_valid_production:
				raise Exception(f"ERROR: '{production}' no es una produccion valida para una gramatica de operadores")
	
	def set_start_symbol(self, non_terminal: str) -> str:
		if not self.is_terminal_symbol(non_terminal):
			self._start_symbol = non_terminal
			return f"{non_terminal} ahora es el simbolo inicial"
		else:
			raise Exception(f"ERROR: '{non_terminal}' no es un símbolo no-terminal válido.")
	
	def set_precedence_in_grammar(self, left:str, op:str, right:str) -> str:
		if op in ("<", "=", ">") and self.is_terminal_symbol(left) and self.is_terminal_symbol(right):
			return self._precedence.set_precedence(left, right, op)
		else:
			raise Exception(f"ERROR: '{op}' no es un operador válido (use <, > o =).")

	def get_rules(self) -> dict:
		return self._rules.item()

	def build_grammar(self):
		self._precedence.construir_fg()
	