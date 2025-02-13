# Tarea 1 - LL y LR: Pregunta 1.b

*«Implemente un reconocedor recursivo descendente para su gramática libre de contexto que genere frases correctas en `JSON`, usando una herramienta basada en **parsec** (información disponible en: https://en.wikipedia.org/wiki/Parsec_(parser)). Puede utilizar el lenguaje de su elección, siempre y cuando tenga una implementación oficial de **parsec** disponible.»*
## Sobre la instalación
1. Clone el repositorio:
	```bash
	git clone https://github.com/A6575/CI4721_TAREAS.git
	```
2. Ir a la carpeta `tarea-1/`
	```bash
	cd ~/CI4721_TAREAS/tarea-1
	```
## Sobre la Implementación

### Prerequisitos
- #### Versión Utilizada
	Para esta implementación se utilizó `Python 3.10.6`
- #### Instalación de librería: `Parsec.py`
	Para instalar la librería se debe ejecutar:
	- Unix/macOs
		```bash
		python3 -m pip install parsec
		```
	- Windows
		```bash
		py -m pip install parsec
		```
	Para más detalles sobre el uso de la librería, visite la [Documentación Oficial](https://pythonhosted.org/parsec/documentation.html).

> [!IMPORTANT]
> Esta librería es compatible desde `Python 2.7` hasta `Python 3.12`.

> [!WARNING]
> **EN CASO DE PROBLEMAS CON LA INSTALACIÓN (`error: externally-managed-environment`)**
> 1. Crear un enviroment con el siguiente comando
> ```bash
> python3 -m venv env
> ```
> 2. Activar el environment con
> ```bash
> source env/bin/activate
> ```
> Luego, realice la instalación respectiva.
	
### Ejecución
Para ejecutar el programa debe ejecutar el archivo `main.py` con el siguiente comando:
- Unix/macOs
	```bash
	python3 main.py <nombre_archivo.json>
	```
- Windows
  ```bash
  py main.py <nombre_archivo.json>
  ```
> [!WARNING]
> En caso de haber necesitado crear un entorno virtual para instalar la librería, asegúrese de activar el mismo antes de ejecutar el programa
### Ejemplos
Los casos de ejemplo con el que se realizaron pruebas se encuentran en la carpeta `test/`
