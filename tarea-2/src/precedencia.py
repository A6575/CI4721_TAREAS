from dataclasses import dataclass, field
from collections import defaultdict
import typing as t

@dataclass
class Precedence:
	"""
		Clase para manejar la precedencia entre simbolos terminales de la gramatica.

		Atributos
			- precedence: diccionario de precedencia entre simbolos terminales de la gramatica
	"""
	_relation: dict[tuple[str,str], str] = field(default_factory=dict)
	_f: dict = field(default_factory=dict)
	_g: dict = field(default_factory=dict)
	_grafo: dict[str, list] = field(default_factory=dict)

	def is_defined_precedence(self, symbols: tuple[str, str]) -> bool:
		return symbols in self._relation

	def get_precedence(self, symbols: tuple[str, str]) -> str:
		return self._relation[symbols]

	def set_precedence(self, symbol1: str, symbol2: str, relation: str) -> None:
		self._relation[(symbol1, symbol2)] = relation
		if relation == '<':
			return f"'{symbol1}' tiene menor precedencia que '{symbol2}'"
		if relation == '>':
			return f"'{symbol1}' tiene mayor precedencia que '{symbol2}'"
		if relation == '=':
			return f"'{symbol1}' tiene igual precedencia que '{symbol2}'"

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
	
	def values_fg(self, nodo: str) -> int:
		longest_f = self.find_longest_path(nodo, "f$")
		longest_g = self.find_longest_path(nodo, "g$")
		
		return max(longest_f, longest_g)

	def construir_fg(self) -> tuple[int, int]:
		# Paso 1: Identificar clases de equivalencia
		equivalence_classes = set()
		same_precedence = []
		for (a, b), op in self._relation.items():
			if a not in same_precedence and b not in same_precedence:
				equivalence_classes.add((a,))
				equivalence_classes.add((b,))
			if op == '=':
				same_precedence.append(a)
				same_precedence.append(b)
				equivalence_classes.add((a, b))
				equivalence_classes.discard((a,))
				equivalence_classes.discard((b,))
		
		equivalence_classes = [list(x) for x in equivalence_classes]
		print(equivalence_classes)
		print(same_precedence)
		
		# Paso 2: Crear nodos equivalentes
		valores_f, valores_g = {}, {}

		for clases in equivalence_classes:
			if len(clases) > 1:
				self._grafo["f"+"".join(clases)] = []
				self._grafo["g"+"".join(clases)] = []
				for nodo in clases:
					valores_f[nodo], valores_g[nodo] = 0, 0
				
				continue
			
			valores_f[clases[0]], valores_g[clases[0]] = 0, 0
			self._grafo["f"+clases[0]] = []
			self._grafo["g"+clases[0]] = []

		for (a, b), op in self._relation.items():
			if op == '<':
				if a in same_precedence and b not in same_precedence:
					aux = [x for x in equivalence_classes if a in x]
					self._grafo["g"+b].append("f"+''.join(aux[0]))
					print()
				elif a not in same_precedence and b in same_precedence:
					aux = [x for x in equivalence_classes if b in x]
					self._grafo["g"+''.join(aux[0])].append("f"+a)
				elif a in same_precedence and b in same_precedence:
					aux_a = [x for x in equivalence_classes if a in x]
					aux_b = [x for x in equivalence_classes if b in x]
					if "f"+''.join(aux_a[0]) in self._grafo["g"+''.join(aux_b[0])]:
						continue
					self._grafo["g"+''.join(aux_b[0])].append("f"+''.join(aux_a[0]))
				else:	
					self._grafo["g"+b].append("f"+a)
			elif op == '>':
				if a in same_precedence and b not in same_precedence:
					aux = [x for x in equivalence_classes if a in x]
					self._grafo["f"+''.join(aux[0])].append("g"+b)
				elif a not in same_precedence and b in same_precedence:
					aux = [x for x in equivalence_classes if b in x]
					self._grafo["f"+a].append("g"+''.join(aux[0]))
				elif a in same_precedence and b in same_precedence:
					aux_a = [x for x in equivalence_classes if a in x]
					aux_b = [x for x in equivalence_classes if b in x]
					if "g"+''.join(aux_b[0]) in self._grafo["f"+''.join(aux_a[0])]:
						continue
					self._grafo["f"+''.join(aux_a[0])].append("g"+''.join(aux_b[0]))
				else:
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

if __name__ == "__main__":
	prueba = Precedence()
	prueba.set_precedence('+', '+', '>')
	prueba.set_precedence('+', '*', '<')
	prueba.set_precedence('+', 'n', '<')
	#prueba.set_precedence('+', '(', '<')
	#prueba.set_precedence('+', ')', '>')
	prueba.set_precedence('+', '$', '>')
	
	prueba.set_precedence('*', '+', '>')
	prueba.set_precedence('*', '*', '>')
	prueba.set_precedence('*', 'n', '<')
	#prueba.set_precedence('*', '(', '<')
	#prueba.set_precedence('*', ')', '>')
	prueba.set_precedence('*', '$', '>')

	prueba.set_precedence('n', '+', '>')
	prueba.set_precedence('n', '*', '>')
	#prueba.set_precedence('n', ')', '>')
	prueba.set_precedence('n', '$', '>')

	#prueba.set_precedence("(", "+", "<")
	#prueba.set_precedence("(", "*", "<")
	#prueba.set_precedence("(", "n", "<")
	#prueba.set_precedence("(", "(", "<")
	#prueba.set_precedence("(", ")", "=")

	#prueba.set_precedence(")", "+", ">")
	#prueba.set_precedence(")", "*", ">")
	#prueba.set_precedence(")", ")", ">")
	#prueba.set_precedence(")", "$", ">")

	prueba.set_precedence('$', '+', '<')
	prueba.set_precedence('$', '*', '<')
	prueba.set_precedence('$', 'n', '<')
	#prueba.set_precedence('$', '(', '<')
	print(*prueba.construir_fg())