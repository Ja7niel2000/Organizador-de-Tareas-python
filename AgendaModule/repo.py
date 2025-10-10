# agenda/repo.py
import re
from dataclasses import dataclass, field
from typing import List
from .tarea import Tarea

@dataclass
class AgendaRepo:
    # Repo en memoria que guarda las Tareas. Genera ids T-0001, T-0002, ...
    tareas: List[Tarea] = field(default_factory=list)
    next_num = 1

    def _agrega_nuevo_numero(self):
        """
        Recorre la lista de tareas y determina el número de ID más alto (T-XXXX).
        Actualiza el atributo `next_num` con el siguiente número disponible.
        """
        maxn = 0
        pattern = re.compile(r"T-(\d+)")
        for t in self.tareas:
            if t.id:
                m = pattern.match(t.id)
                if m:
                    # m.group(1) Guarda lo que encontro en el primer parentesis de la expresión regular.
                    # y lo convierte en un int, "000x" -> x;
                    n = int(m.group(1))
                    if n > maxn:
                        maxn = n
        self.next_num = maxn + 1

    def _genera_id(self) -> str:
        """
        Genera un nuevo ID de tarea en formato 'T-XXXX' usando `next_num`.
        Incrementa el contador interno para el siguiente ID.
        """
        id_ = f"T-{self.next_num:04d}"
        self.next_num += 1
        return id_

    def add(self, titulo: str, prioridad: int = 3, fecha: str | None = None, etiquetas: List[str] | None = None, descripcion: str = "") -> Tarea:
        """
        Crea una nueva tarea con los datos proporcionados y la agrega al repositorio.

        Args:
            titulo: Título de la tarea.
            prioridad: Nivel de prioridad (por defecto 3).
            fecha: Fecha asociada a la tarea en formato 'AAAA-MM-DD'.
            etiquetas: Lista opcional de etiquetas.
            descripcion: Descripción breve de la tarea.

        Returns:
            La instancia de Tarea creada.
        """
        etiquetas = etiquetas or []
        id_ = self._genera_id()
        tarea = Tarea(id=id_, titulo=titulo, prioridad=prioridad,
                      fecha=fecha, etiquetas=etiquetas, descripcion=descripcion)
        self.tareas.append(tarea)
        return tarea

    def get(self, id: str) -> Tarea | None:
        """
        Busca una tarea por su ID y la devuelve.

        Args:
            id: Identificador único de la tarea (por ejemplo, 'T-0001').

        Returns:
            La tarea encontrada o None si no existe.
        """
        for t in self.tareas:
            if t.id == id:
                return t
        return None

    def remove(self, id_: str) -> bool:
        """
        Elimina una tarea del repositorio según su ID.

        Args:
            id_: Identificador único de la tarea.

        Returns:
            True si la tarea fue eliminada, False si no se encontró.
        """
        t = self.get(id_)
        if t:
            self.tareas.remove(t)
            return True
        return False

    def list(self, orden: str = "fecha") -> List[Tarea]:
        """
        Devuelve una lista de tareas ordenadas según el campo especificado.

        Args:
            orden: Criterio de ordenamiento ('fecha', 'prioridad', 'titulo' o 'id').

        Returns:
            Una lista de tareas ordenadas.
        """
        if orden == "fecha":
            key = lambda t:  (t.fecha or "")
        elif orden == "prioridad":
            key = lambda t: t.prioridad
        elif orden == "titulo":
            key = lambda t: t.titulo.lower()
        else:
            def key(t): return t.id or ""
        return sorted(self.tareas, key=key, reverse=False)
    
    def find(self, texto: str) -> List[Tarea]:
        """
        Busca tareas cuyo título o descripción contengan el texto indicado (sin distinguir mayúsculas/minúsculas).

        Args:
        texto: Texto a buscar dentro del título o la descripción.

        Returns:
        Lista de tareas que coinciden con el texto.
        """
        texto = texto.lower()
        return [t for t in self.tareas if texto in t.titulo.lower() or texto in t.descripcion.lower()]

    def marca_hecho(self, id: str) -> bool:
        """
        Marca una tarea como completada usando su ID.

        Args:
            id: Identificador único de la tarea.

        Returns:
            True si la tarea fue encontrada y marcada, False en caso contrario.
        """
        t = self.get(id)
        if t:
            t.completada = True
            return True
        return False

    def carga_de_lista(self, lista_dicts: List[dict]):
        """
        Carga una lista de tareas desde una lista de diccionarios y actualiza el contador de IDs.

        Args:
            lista_dicts: Lista de objetos tipo dict representando tareas.
        """
        self.tareas = [Tarea.from_dict(d) for d in lista_dicts]
        self._agrega_nuevo_numero()

    def convierte_list(self) -> List[dict]:
        """
        Convierte todas las tareas del repositorio a una lista de diccionarios serializables.

        Returns:
            Lista de diccionarios que representan las tareas.
        """
        return [t.to_dict() for t in self.tareas]
