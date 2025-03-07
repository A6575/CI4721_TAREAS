from dataclasses import dataclass, field
from collections import defaultdict
import typing as t

@dataclass
class Precedence:
	"""
		Clase para manejar la precedencia entre simbolos terminales de la gramatica.

		Atributos
			- _relation: diccionario de precedencia entre simbolos terminales
			- _f: diccionario de valores f
			- _g: diccionario de valores g
			- _grafo: diccionario de nodos y sus vecinos
	"""
	_relation: dict[tuple[str,str], str] = field(default_factory=dict)
	_f: dict = field(default_factory=dict)
	_g: dict = field(default_factory=dict)
	_grafo: dict[str, list] = field(default_factory=dict)

	# funcion para verificar si una precedencia esta definida
	def is_defined_precedence(self, symbols: tuple[str, str]) -> bool:
		return symbols in self._relation

	# funcion para obtener la precedencia entre dos simbolos
	def get_precedence(self, symbols: tuple[str, str]) -> str:
		return self._relation[symbols]

	# funcion para establecer la precedencia entre dos simbolos
	def set_precedence(self, symbol1: str, symbol2: str, relation: str) -> None:
		self._relation[(symbol1, symbol2)] = relation
		if relation == '<':
			return f"'{symbol1}' tiene menor precedencia que '{symbol2}'"
		if relation == '>':
			return f"'{symbol1}' tiene mayor precedencia que '{symbol2}'"
		if relation == '=':
			return f"'{symbol1}' tiene igual precedencia que '{symbol2}'"

	# funcion para encontrar el camino mas largo entre dos nodos
	def find_longest_path(self, start: str, end: str) -> int:
		def topological_sort_util(v, visited, stack):
			visited[v] = True
			if v in self._grafo:
				for i in self._grafo[v]:
					if not visited[i]:
						topological_sort_util(i, visited, stack)
			stack.insert(0, v)

		def topological_sort():
			visited = {key: False for key in self._grafo}
			stack = []
			for i in self._grafo:
				if not visited[i]:
					topological_sort_util(i, visited, stack)
			return stack

		stack = topological_sort()
		dist = {key: float('-inf') for key in self._grafo}
		dist[start] = 0
		path = {key: [] for key in self._grafo}
		path[start] = []

		while stack:
			u = stack.pop(0)
			if dist[u] != float('-inf'):
				for i in self._grafo[u]:
					if dist[i] < dist[u] + 1:
						dist[i] = dist[u] + 1
						path[i] = path[u] + [i]

		return len(path[end]) if dist[end] != float('-inf') else 0
	
	# funcion para obtener los valores f y g de un nodo
	def values_fg(self, nodo: str) -> int:
		longest_f = self.find_longest_path(nodo, "f$")
		longest_g = self.find_longest_path(nodo, "g$")
		
		return max(longest_f, longest_g)

	# funcion para construir los valores f y g
	def construir_fg(self) -> tuple[dict, dict]:
		nodos = set()
		for (a, b), op in self._relation.items():
			nodos.add(a)
			nodos.add(b)
		
		valores_f, valores_g = {}, {}

		for nodo in nodos:
			valores_f[nodo], valores_g[nodo] = 0, 0
			self._grafo["f"+nodo] = []
			self._grafo["g"+nodo] = []

		for (a, b), op in self._relation.items():
			if op == '<':	
				self._grafo["g"+b].append("f"+a)
			elif op == '>':
				self._grafo["f"+a].append("g"+b)
			
		for nodo in self._grafo.keys():
			print(nodo, "->", end=" ")
			for neighbor in self._grafo[nodo]:
				print(neighbor, ",", end=" ")
			print()

		for nodo in self._grafo.keys():
			if nodo.startswith("f"):
				valores_f[nodo[1:]] += self.values_fg(nodo)
			else:
				valores_g[nodo[1:]] += self.values_fg(nodo)

		self._f, self._g = valores_f, valores_g
		return self._f, self._g