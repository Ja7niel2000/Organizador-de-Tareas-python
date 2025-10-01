# agenda/io_json.py
import json
from typing import List
from .tarea import Tarea


def save_to_file(filename: str, tareas: List[Tarea]) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump([t.to_dict() for t in tareas], f, ensure_ascii=False, indent=2)





def load_from_file(filename: str) -> List[Tarea]:
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Tarea.from_dict(d) for d in data]
