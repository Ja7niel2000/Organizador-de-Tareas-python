# agenda/io_json.py
import json
import os
from typing import List
from .tarea import Tarea

def save_to_file(filename: str, tareas: List[Tarea]) -> None:
    """
    Guarda una lista de tareas en un archivo JSON.

    Args:
        filename (str): Nombre del archivo donde se guardarán las tareas.
        tareas (List[Tarea]): Lista de objetos Tarea a guardar.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tareas], f, ensure_ascii=False, indent=2)

def load_from_file(filename: str) -> List[Tarea]:
    """
    Carga una lista de tareas desde un archivo JSON.

    Args:
        filename (str): Nombre del archivo JSON desde el que se cargarán las tareas.

    Returns:
        List[Tarea]: Lista de objetos Tarea cargados del archivo. 
                     Devuelve una lista vacía si el archivo no existe o contiene JSON inválido.
    """
    if not os.path.exists(filename):
        # Si no existe el archivo, devuelve lista vacía
        return []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: El archivo {filename} no contiene JSON válido.")
        return []
    
    return [Tarea.from_dict(d) for d in data]
