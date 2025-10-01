# agenda/repo.py
from dataclasses import dataclass,field
from typing import List
import re
from .tarea import Tarea

@dataclass
class AgendaRepo:
    
    #Repo en memoria que guarda las Tareas. Genera ids T-0001, T-0002, ...
    tareas:List[Tarea]=field(default_factory=list)
    next_num =1

    def _agrega_nuevo_numero(self):
        # Aquí use regex para encontrar el número de id más grande en la lista de tareas.
        # y le suma un 1 al_next_num, para saber cual sera el siguiente número de tarea;
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
        #Le la el formato al id
        id_ = f"T-{self.next_num:04d}"
        self.next_num+= 1
        return id_

    def add(self, titulo: str, prioridad: int = 3, fecha:str|None=None, etiquetas: List[str]|None=None, descripcion: str = "") -> Tarea:
        etiquetas = etiquetas or []
        # generar id 
        id_=self._genera_id()
        tarea=Tarea(id=id_, titulo=titulo, prioridad=prioridad,fecha=fecha, etiquetas=etiquetas, descripcion=descripcion)
        self.tareas.append(tarea)
        return tarea

    # Busca una tarea en base a su Id y lo devuelve
    def get(self, id: str) -> Tarea|None:
        for t in self.tareas:
            if t.id == id:
                return t
        return None

    # Usa get y elimina la tarea devuelta con el método remove() de List
    def remove(self, id_: str) -> bool:
        t =self.get(id_)
        if t:
            self.tareas.remove(t)
            return True
        return False

    #regresa una lista ordenada 
    def list(self, orden: str = "fecha") -> List[Tarea]:
        if orden=="fecha":
            key=lambda t: (t.fecha or "")
        elif orden== "prioridad":
            key =lambda t: t.prioridad
        elif orden== "titulo":
            key =lambda t: t.titulo.lower()
        else:
            key =lambda t: t.id or ""
        return sorted(self.tareas, key=key, reverse=False)

    def marca_hecho(self, id: str) -> bool:
        t = self.get(id)
        if t:
            t.completada = True
            return True
        return False
    
    def carga_de_lista(self, lista_dicts: List[dict]):
        self.tareas = [Tarea.from_dict(d) for d in lista_dicts]
        self._agrega_nuevo_numero()

    def convierte_list(self) -> List[dict]:
        return [t.to_dict() for t in self.tareas]
    
    #Busca por titulo o descripción
    def find(self, texto: str) -> List[Tarea]:
        texto = texto.lower()
        return [t for t in self.tareas if texto in t.titulo.lower() or texto in t.descripcion.lower()]

 
