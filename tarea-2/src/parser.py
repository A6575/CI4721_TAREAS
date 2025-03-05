from .gramatica import *
from dataclasses import dataclass, field
import typing as t

@dataclass
class Parser:
	_grammar: Grammar
	_terminal_token: str = '$'
	
	def parse(self, input_string: str) -> None:
		stack = [self._terminal_token]
		input_string+=self._terminal_token
		index = 0

		while index < len(input_string):
			symbol = input_string[index]

			if self._grammar.is_defined_precedence((stack[-1], symbol)):
				relation = self._grammar.get_precedence((stack[-1], symbol))

				if relation in [">", "="]:
					stack.append(symbol)
					index+=1
				elif relation == "<":
					pass
				else:
					raise Exception()
			else:
				raise Exception()
		if stack == [self._terminal_token]:
			print("")
			return
		else:
			print()
	
	def reduce(self, stack: list) -> None:
		for no_terminal, productions in self._grammar.get_rules():
			for prod in productions:
				if stack[-len(prod):] == list(prod):
					stack[-len(prod):] = [no_terminal]
					print("")
					return
		
		raise Exception()
