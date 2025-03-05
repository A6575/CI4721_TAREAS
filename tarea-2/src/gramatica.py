from dataclasses import dataclass, field
import typing as t

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
	_start_symbol: str = field(default_factory=str)
	_rules: dict[str, list[str]] = field(default_factory=dict)
	_precedence: dict[t.Tuple[str,str], str] = field(default_factory=dict)

	def is_terminal_symbol(self, symbol: str) -> bool:
		# Verificar que todos los caracteres sean ASCII, que la cadena no contenga '$',
		# que no tenga letras mayúsculas ni números
		return (len(symbol) >= 1 and
				symbol.isascii() and
				'$' not in symbol and
				not any(char.isupper() for char in symbol) and
				not any(char.isdigit() for char in symbol))
	
	def is_valid_production(self, non_terminal: str, production: str) -> bool:
		# Verificar si es una producción vacía (lambda)
		if production == "":
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

	def add_rule(self, non_terminal: str, production: str) -> str:
		if not self.is_terminal_symbol(non_terminal) and self.is_valid_production(non_terminal, production):
			self.rules.setdefault(non_terminal, []).append(production)
			return f"{non_terminal} -> {production}"
		else:
			raise Exception(f"ERROR: '{non_terminal}' no es un símbolo no-terminal válido.")
	
	def set_start_symbol(self, non_terminal: str) -> str:
		if not self.is_terminal_symbol(non_terminal):
			self.set_start_symbol = non_terminal
			return f"{non_terminal} ahora es el simbolo inicial"
		else:
			raise Exception(f"ERROR: '{non_terminal}' no es un símbolo no-terminal válido.")
	
	def set_precedence(self, left:str, op:str, right:str) -> str:
		if op in ("<", "=", ">") and self.is_terminal_symbol(left) and self.is_terminal_symbol(right):
			self.precedence[(left, right)] = op
			return "precedencia establecida"
		else:
			raise Exception(f"ERROR: '{op}' no es un operador válido (use <, > o =).")
		
	def is_defined_precedence(self, key: tuple) -> bool:
		return key in self._precedence
	
	def get_precedence(self, key: tuple) -> bool:
		return self._precedence[key]
	
	def get_rules(self):
		return self._rules.item()
	