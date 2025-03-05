from .parser import *
from .gramatica import *
from dataclasses import dataclass, field
import typing as t

@dataclass
class AnalizadorSintactico:
	_grammar: Grammar = field(default_factory=Grammar())
	_parser: Parser = field(default=Parser(_grammar))

	def run(self):
		while True:
			command = input("").strip()
			parts = command.split(maxsplit=2)

			if not parts:
				continue

			action = parts[0].upper()

			if action == "RULE":
				_, left, right = parts
				self.grammar.add_rule(left, right.split())
			elif action == "INIT":
				self.grammar.set_start_symbol(parts[1])
			elif action == "PREC":
				self.grammar.set_precedence(parts[1], parts[2], parts[3])
			elif action == "BUILD":
				print("Analizador construido.")
			elif action == "PARSE":
				self.parser.parse(parts[1])
			elif action == "EXIT":
				print("Saliendo del programa.")
				break
			else:
				print("ERROR: Comando no reconocido.")