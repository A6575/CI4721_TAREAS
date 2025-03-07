from .parser import *
from .gramatica import *
from dataclasses import dataclass, field
import typing as t

@dataclass
class AnalizadorSintactico:
	"""
		Clase para manejar el analizador sintactico. (Programa principal)

		Atributos
			- _grammar: gramatica del analizador sintactico

			- _parser: parser del analizador sintactico
	"""
	_grammar: Grammar = field(default_factory=Grammar)
	_parser: Parser = field(default=Parser(_grammar))

	# funcion para correr el programa
	def run(self):
		while True:
			command = input("$> ").strip()
			if command.startswith("RULE"):
				parts = command.split(maxsplit=2)
			elif command.startswith("PARSE"):
				parts = command.split(maxsplit=1)
			else:
				parts = command.split()

			if not parts:
				print("ERROR: No se coloco ninguna instruccion.")
				continue

			action = parts[0].upper()

			if action == "RULE":
				_, left, right = parts
				try:
					print(self._grammar.add_rule(left, right.split()))
				except Exception as e:
					print(e)
			elif action == "INIT":
				try:
					print(self._grammar.set_start_symbol(parts[1]))
				except Exception as e:
					print(e)
			elif action == "PREC":
				try:
					print(parts)
					print(self._grammar.set_precedence_in_grammar(parts[1], parts[2], parts[3]))
				except Exception as e:
					print(e)
			elif action == "BUILD":
				try:
					f, g = self._grammar.build_grammar()
					self._parser.set_fg(f, g)
				except Exception as e:
					print(e)
			elif action == "PARSE":
				print(parts)
				#self._parser.parse(parts[1])
			elif action == "EXIT":
				print("Saliendo del programa.")
				break
			else:
				print("ERROR: Comando no reconocido.")