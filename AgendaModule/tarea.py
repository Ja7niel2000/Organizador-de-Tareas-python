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
        
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "titulo": self.titulo,
            "prioridad": self.prioridad,
            "fecha": self.fecha,
            "etiquetas": self.etiquetas,
            "descripcion": self.descripcion,
            "completada": self.completada,
        }

    @staticmethod
    def from_dict(d: dict) -> "Tarea":
        return Tarea(
            id= d.get("id"),
            titulo= d.get("titulo", ""),
            #Devuelve el valor de "prioridad" si no está regresa el valor por defecto (5)
            prioridad= int(d.get("prioridad", 5)),
            fecha= d.get("fecha"),
            etiquetas =d.get("etiquetas", []) or [],
            descripcion =d.get("descripcion", "") or "",
            completada= bool(d.get("completada", False)),
        )