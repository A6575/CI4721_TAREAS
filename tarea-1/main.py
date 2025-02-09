import json_rrd
import sys

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print(f"ERROR: expected \"python {sys.argv[0]} <archivo-prueba.txt>\" ")
		sys.exit(1)

	nombre_archivo = sys.argv[1]
	with open(nombre_archivo) as f:
		archivo_json = f.readlines()

	print(archivo_json)