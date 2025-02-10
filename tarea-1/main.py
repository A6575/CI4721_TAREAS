import sys
from json_rrd import *

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print(f"ERROR: expected \"python {sys.argv[0]} <archivo-prueba.txt>\" ")
		sys.exit(1)

	nombre_archivo = sys.argv[1]
	if not nombre_archivo.endswith(".json"):
		print(f"ERROR: expected a .json file, got {nombre_archivo}")
		sys.exit(1)
	
	with open(nombre_archivo) as f:
		archivo_json = f.read()
	
	try:
		resultado = json_parser.parse(archivo_json)
		print("JSON válido:", resultado)
	except Exception as e:
		print("Error de parsing:", e)
	print(archivo_json)