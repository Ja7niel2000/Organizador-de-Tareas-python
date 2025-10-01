# agenda/cli.py
import argparse
import os
from typing import List
from .repo import AgendaRepo
from .jsonFun import save_to_file, load_from_file

def separa_etiquetas(s: str) -> List[str]:
    if not s:
        return []
    return [x.strip() for x in s.split(",") if x.strip()]

def print_tareas(tareas):
    for t in tareas:
        status = "[x]" if t.completada else "[ ]"
        print(f"{t.id} {status} {t.titulo} (prio:{t.prioridad}) {t.fecha or ''}")
 
def main():
    #nombre del archivo donde se guardara las tareas.
    dataBase="Tareas.json"

    comando = argparse.ArgumentParser(prog="agenda", description="Agenda CLI simple")
    sub = comando.add_subparsers(dest="command", required=True)

    # add
    p =sub.add_parser("add", help="Agregar tarea")
    p.add_argument("--titulo" ,required=True)
    p.add_argument("--fecha",help="AAAA-MM-DD", default=None)
    p.add_argument("--prioridad", type=int, default=3)
    p.add_argument("--etiquetas" , default="")
    p.add_argument("--descripcion" , default="")

    # ls
    p= sub.add_parser("ls",help="Listar tareas")
    p.add_argument("--por" ,  choices=["fecha", "prioridad", "titulo"], default="fecha")

    #find
    p =sub.add_parser("find" , help="Buscar por texto")
    p.add_argument("texto")

    # done
    p =sub.add_parser("done",help=" Marcar como completada")
    p.add_argument("id")

    p = sub.add_parser("rm",help="Eliminar tarea")
    p.add_argument("id")

    args =comando.parse_args()

    repo =AgendaRepo()
    # si especificaron db y existe, cargar primero
    if os.path.exists(dataBase):
        tareas = load_from_file(dataBase)
        repo.carga_de_lista([t.to_dict() for t in tareas])

    # ejecutar comando
    if args.command == "add":
        etiquetas = separa_etiquetas(args.etiquetas)
        tarea = repo.add(args.titulo, prioridad=args.prioridad, fecha=args.fecha,
                        etiquetas=etiquetas, descripcion=args.descripcion)
        print(f"Tarea agregada: {tarea.id}")

    elif args.command == "ls":
        tareas = repo.list(orden=args.por)
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
    save_to_file(dataBase, repo.tareas)


