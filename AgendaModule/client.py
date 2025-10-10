import argparse
import os
from typing import List
from pathlib import Path
from .repo import AgendaRepo
from .jsonFun import save_to_file, load_from_file

def separa_etiquetas(s: str) -> List[str]:
    """
    Convierte una cadena de etiquetas separadas por comas en una lista.

    Args:
        s (str): Cadena con etiquetas separadas por comas, por ejemplo "escuela, tarea, urgente".

    Returns:
        List[str]: Lista de etiquetas sin espacios vacíos.
    """
    if not s:
        return []
    return [x.strip() for x in s.split(",") if x.strip()]

def print_tareas(tareas):
    """
    Imprime una lista de tareas en formato legible en la consola.

    Args:
        tareas (List[Tarea]): Lista de objetos Tarea a imprimir.
    """
    for t in tareas:
        status = "[x]" if t.completada else "[ ]"
        print(f"{t.id}  {status} {t.titulo} (prio:{t.prioridad})  {t.fecha or ''}")
 
def main():
    """
    Punto de entrada principal de la aplicación CLI (línea de comandos) para la agenda.

    Permite gestionar tareas desde la terminal mediante subcomandos:
    - add: Agregar una tarea nueva.
    - ls: Listar todas las tareas.
    - find: Buscar tareas por texto.
    - done: Marcar una tarea como completada.
    - rm: Eliminar una tarea.
    
    Al finalizar cualquier operación, el programa guarda automáticamente los cambios
    en el archivo JSON de la base de datos.
    """
    #nombre del archivo donde se guardara las tareas.
    DATABASE="Tareas.json"

    comando = argparse.ArgumentParser(prog = "agenda", description = "Agenda CLI simple")
    sub = comando.add_subparsers(dest = "command", required = True)

    # add
    p = sub.add_parser("add", help = "Agregar tarea")
    p.add_argument("--titulo" ,required = True)
    p.add_argument("--fecha", help = "AAAA-MM-DD", default = None)
    p.add_argument("--prioridad", type = int, default = 3)
    p.add_argument("--etiquetas", default = "")
    p.add_argument("--descripcion", default = "")

    #  ls
    p = sub.add_parser("ls", help = "Listar tareas")
    p.add_argument("--por", choices = ["fecha", "prioridad", "titulo"], default = "fecha")

    #find
    p = sub.add_parser("find", help = "Buscar por texto")
    p.add_argument("texto")

    # done
    p = sub.add_parser("done", help = "Marcar como completada")
    p.add_argument("id")

    p = sub.add_parser("rm", help = "Eliminar tarea")
    p.add_argument("id")

    args = comando.parse_args()

    repo = AgendaRepo()

    #si no existe DB lo crea
    if not os.path.exists(DATABASE):
        Path(DATABASE).write_text("", encoding="utf-8")
        print("DB creada, usa add para agregar")
        return
    
    tareas = load_from_file(DATABASE)
    repo.carga_de_lista([t.to_dict()  for t in tareas])

    # ejecutar comando
    if args.command == "add":
        etiquetas = separa_etiquetas(args.etiquetas)
        tarea = repo.add(args.titulo, prioridad = args.prioridad, fecha = args.fecha, etiquetas = etiquetas, descripcion = args.descripcion)
        print(f"Tarea agregada: {tarea.id}")

    elif args.command == "ls":
        tareas = repo.list(orden = args.por)
        print_tareas(tareas)

    elif args.command == "find":
        res = repo.find(args.texto)
        print_tareas(res)

    elif args.command == "done":
        ok = repo.marca_hecho(args.id)
        print("OK" if ok else "No encontrada")

    elif args.command == "rm":
        ok = repo.remove(args.id)
        print("OK" if ok else "No encontrada")

    #guardar automáticamente al terminar
    save_to_file(DATABASE, repo.tareas)


