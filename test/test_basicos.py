"""
Método en donde podemos checar si la agenda funciona en términos 
generales, checando las 3 operaciones mínimas de las instrucciones
"""
import os
from AgendaModule.repo import AgendaRepo
from AgendaModule.tarea import Tarea
from AgendaModule.jsonFun import save_to_file, load_from_file
# Primero creamos un repositorio vacío y luego checamos si la cantidad 
# de tareas que agregamos está bien
def test_agregar_dos_y_tamano():
    repo = AgendaRepo()
    repo.add(titulo="P1 MOD", prioridad=3, fecha="2025-09-01")
    repo.add(titulo="P2 ARQ", prioridad=2, fecha="2025-09-02")
    assert len(repo.tareas) == 2

# Creamos otro repositorio y checamos si buscando una tarea por una palabra 
# si funciona y regresa un texto con esa palabra n
def test_find_devuelve_esperada():
    repo = AgendaRepo()

    repo.add(titulo="Práctica 1 MYP",prioridad=5,fecha="2025-09-01",descripcion="La de minecraft")
    resultados = repo.find("MYP")
    assert resultados and resultados[0].id == "T-0001"

# Creamos otro repositorio y checamos que las tareas que guardamos si se mantengan
def test_save_load_conserva_numero_y_titulo():
    repo = AgendaRepo()
    repo.add(
        titulo="Tarea 1 de Autómatas",
        prioridad=3,
        fecha="2025-09-01"
    )

    DATABASE = "TareasTemp.json"
    save_to_file(DATABASE,repo.tareas)
    tareas = load_from_file(DATABASE)

    nuevo_repo=AgendaRepo()
    nuevo_repo.carga_de_lista([t.to_dict() for t in tareas])  

    assert len(nuevo_repo.tareas) == 1
    tarea=nuevo_repo.get("T-0001")
    assert tarea.titulo == "Tarea 1 de Autómatas"
    os.remove(DATABASE)
