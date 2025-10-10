from dataclasses import dataclass, field
from typing import List
from datetime import date

@dataclass
class Tarea:
    """
    Representa una tarea dentro del organizador

    Esta clase modela una tarea con título, prioridad, fecha, descripción,
    estado (completada o no) y una lista de etiquetas. 
    No se necesita el __init__ porque el decorador dataclass ya lo pone automáticamente,lol.

    Atributos:
        id (str | None): Identificador único de la tarea.
        completada (bool): Indica si la tarea fue completada. Por defecto `False`.
        titulo (str): Título o nombre de la tarea.
        prioridad (int): Nivel de prioridad (1 = alta, 5 = baja).
        descripcion (str): Detalles o notas adicionales sobre la tarea.
        fecha (str | None): Fecha en formato ISO (`YYYY-MM-DD`) o `None`.
        etiquetas (List[str]): Lista de etiquetas asociadas con la tarea.

    Excepciones:
        ValueError: Si la prioridad o la fecha tienen un formato inválido.
    """
    id: str|None 
    completada: bool =False
    titulo: str = ""
    prioridad: int = 5  # 1..5
    descripcion: str = ""
    fecha: str|None = None  # "YYYY-MM-DD" o None
    # default_factory se usa para darle una lista vacia (Etiquetas) diferente a cada instancia de tarea
    etiquetas: List[str] = field(default_factory=list)
    

    def __post_init__(self):
        """
        Valida los campos de la tarea después de la inicialización automática de dataclass.

        - Verifica que la prioridad esté entre 1 y 5.
        - Asegura que `fecha` (si existe) tenga el formato ISO correcto.
        - Confirma que `etiquetas` sea una lista.
        
        Raises:
            ValueError: Si alguno de los campos no cumple con las validaciones.
        """
        if not isinstance(self.prioridad, int) or not (1 <= self.prioridad <= 5):
            raise ValueError("prioridad debe ser un entero entre 1 y 5")

        # validá el formato de la fecha si se proporcionó
        if self.fecha:
            try:
                # Formato de fecha valida = AAAA-MM-DD
                date.fromisoformat(self.fecha)
            except Exception as e:
                raise ValueError("La fecha debe ser YYYY-MM-DD") from e

        # etiquetas debe ser lista
        if not isinstance(self.etiquetas, list):
            raise ValueError("etiquetas debe ser una lista de strings")
        
    def to_dict(self) -> dict:
        """
        Convierte el objeto `Tarea` a un diccionario serializable (por ejemplo, para JSON).

        Returns:
            dict: Un diccionario con las claves:
                - id
                - titulo
                - prioridad
                - fecha
                - etiquetas
                - descripcion
                - completada
        """
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
        """
        Crea una instancia de `Tarea` a partir de un diccionario.

        Este método es útil al cargar datos desde JSON u otras fuentes de almacenamiento.

        Args:
            d (dict): Diccionario con los datos de la tarea.

        Returns:
            Tarea: Una nueva instancia con los valores extraídos del diccionario.
        """
        return Tarea(
            id = d.get("id"),
            titulo = d.get("titulo", ""),
            #Devuelve el valor de "prioridad" si no está regresa el valor por defecto (5)
            prioridad = int(d.get("prioridad", 5)),
            fecha = d.get("fecha"),
            etiquetas = d.get("etiquetas", []) or [],
            descripcion = d.get("descripcion", "") or "",
            completada = bool(d.get("completada", False)),
        )