# agenda/tarea.py
from dataclasses import dataclass, field
from typing import List
from datetime import date

@dataclass
class Tarea:
    #No se necesita el __init__ porque el decorador dataclass ya lo pone automáticamente,lol
    # Representa una tarea.
    id: str|None 
    completada: bool =False
    titulo: str= ""
    prioridad: int =5  # 1..5
    descripcion: str =""
    fecha: str|None =None  # "YYYY-MM-DD" o None
    # default_factory se usa para darle una lista vacia (Etiquetas) diferente a cada instancia de tarea
    etiquetas: List[str] = field(default_factory=list)
    

    def __post_init__(self):
        # revisa si la prioridad está dentro del parámetro
        # isinstance sirve para verificar que prioridad si sea un int y no otro valor invalido.
        if not isinstance(self.prioridad, int) or not (1 <= self.prioridad <= 5):
            raise ValueError("prioridad debe ser un entero entre 1 y 5")

        # validá el formato de la fecha si se proporcionó
        if self.fecha:
            try:
                # Formato de fecha valida = AAAA-MM-DD
                date.fromisoformat(self.fecha)
            except Exception as e:
                raise ValueError("lafecha debe ser YYYY-MM-DD") from e

        # etiquetas debe ser lista
        if not isinstance(self.etiquetas, list):
            raise ValueError("etiquetas debe ser una lista de strings")
