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

	def add_rule(self, non_terminal: str, production: str) -> str:
		if non_terminal.isupper():
			self.rules.setdefault(non_terminal, []).append(production)
			return f"{non_terminal} -> {production}"
		else:
			raise Exception(f"ERROR: '{non_terminal}' no es un símbolo no-terminal válido.")
	
	def set_start_symbol(self, non_terminal: str) -> str:
		if non_terminal.isupper():
			self.set_start_symbol = non_terminal
			return f"{non_terminal} ahora es el simbolo inicial"
		else:
			raise Exception(f"ERROR: '{non_terminal}' no es un símbolo no-terminal válido.")
	
	def set_precedence(self, left:str, op:str, right:str) -> str:
		if op in ("<", "=", ">"):
			self.precedence[(left, right)] = op
			return "precedencia establecida"
		else:
			raise Exception(f"ERROR: '{op}' no es un operador válido (use <, > o =).")
	