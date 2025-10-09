import json
from AgendaModule.tarea import Tarea
from AgendaModule.repo import AgendaRepo
from pathlib import Path

PATH_DB = Path("Tareas.json")
HTML_PATH = Path("index.html")
STYLES_PATH=Path("styles.css")

STYLES="""
:root{
    /* --color-secundario:#5170AE;
    --color-primario:#4993B6; */

      --color-secundario:#21396A;
    /* --color-primario:#13303E; */

    
    --color-secundario:#B24D4D;
    --color-primario:#043D58;
    
    /* --color-secundario:#664DB2;
    --color-primario:#4A45BA; */
    --font-color:#000000;
    --font-color:#ffffff;


}

body{
    margin: 0;
    width: 100%;
    /* background-color: rgb(179, 29, 84); */
    background-color: var(--color-secundario);
}

header{
    padding: 10px 0;
    width: 100%;
    height: 50px;
    /* background-color: rgb(213, 24, 93); */
    background-color: var(--color-primario);
    margin-bottom: 40px;
    box-shadow: 0px 0px 30px 2px ;
}

h1{
    margin: 0;
    margin-left: 10px;
    color: var(--font-color);
}

.container{
    padding-left:50px;
    padding-right: 50px;

}

.containerLabel{
    padding: 10px;
    width: 100%;
    /* background-color: rgb(213, 24, 93); */
    background-color: var(--color-primario);
    color: var(--font-color);
    border-bottom: 1px solid black;
   
}

h2{
    padding: 5px 5px 0px 5px;
    margin: 0;
}

.tableContainer{
    width: 100%;
    background-color: white;
    padding: 10px;
    padding-top: 10px;
    margin-bottom: 50px;
}

.headers{
    background-color: rgb(231, 231, 231);
    height: 30px;
    border-top: 1px solid black;
    
}
.row{
    min-height: 40px;
    display:grid;
    grid-template-columns:0.15fr 1fr 0.3fr 0.5fr 1fr 0.8fr;
    margin:0;
    padding: 0;
    border-bottom: 1px solid black;

}

.row div{
    width: 100%;
    text-align: center;
    align-self: center;
}

.voidTareas{
    text-align: center;
}

footer{
    display: block;
    width: 100%;
    background-color: var(--color-primario);
    box-shadow: 0px 20px 50px 1px ;
}

.footerContainer{
    width: 100%;
    height: 100%;
    display:flex;
    flex-direction: column;
    align-items: center;
}

.footerContainer p{
    color: var(--font-color);
}

.footerContainerInfo{
    margin-top: 10px;
}

.nombresEquipo{
    display: flex;
    gap: 15px;

}

.noMargin{
    margin: 0;
}

"""
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="styles.css">
    <title>Tareas</title>
</head>
  <header>
            <h1>
                Organizador de Tareas
            </h1>
    </header>
<body>
  
    <main class="container">
        <div class="containerLabel">
                <h2>
                    ❌ Tareas Pendientes [INT]
                </h2>
        </div>

        {t_p}

        <div class="containerLabel">
            <h2>
                [] Tareas Completas [INT]
            </h2>
        </div>

        {t_c}
    
    </main>
    <footer>
        <div class="footerContainer">
            <p class="footerContainerInfo">Tarea para la asignatura "Modelado y programación" de la carrera de ciencias de la computación, UNAM</p>
            
            <div class="nombresEquipoContainer">
                <p class="noMargin">Equipo de: </p>
                <div class="nombresEquipo">
                    <p>Jatniel Carranza Bolaños</p>
                    <p>Leo </p>
                </div>
            </div>
           
        </div>
    </footer>
</body>
</html>
"""

TAREA_TEMPLATE="""
    <div class="row homework" id="{id}">
        <div id="numero">{i_}</div>
        <div id="titulo">{ti}</div>
        <div id="prioridad">{pr}</div>
        <div id="fecha">{fe}</div>
        <div id="descripción">{de}</div>
        <div id="etiquetas">{et}</div>
    </div>
"""

NO_TAREA="""
<div class="tableContainer">
    <div class="voidTareas">
        <p>No hay tareas</p>
    </div>
</div>
"""

def main():
    tareas_completadas_html=""
    tareas_pendientes_html=""

    if not PATH_DB:
        print("NO existe base de datos")
        return 
    
    with open(PATH_DB,"r", encoding="utf-8") as f:
        data=json.load(f)

    repo = AgendaRepo()
    repo.carga_de_lista(data)

    i1=0
    i2=0
    for t in repo.tareas:
        if(t.completada):
            tareas_completadas_html+=TAREA_TEMPLATE.format(
                id=t.id,
                i_=i1,
                titulo=t.titulo,
                pr=t.prioridad,
                fe=t.fecha,
                de=t.descripcion,
                et=t.etiquetas
                )
            i1=i1+1
        else:
            tareas_pendientes_html+=TAREA_TEMPLATE.format(
                id=t.id,
                i_=i2,
                titulo=t.titulo,
                pr=t.prioridad,
                fe=t.fecha,
                de=t.descripcion,
                et=t.etiquetas
            )
            i2=i2+1
    
    if(tareas_completadas_html==""):
         tareas_completadas_html=NO_TAREA.format()

    if(tareas_pendientes_html==""):
         tareas_completadas_html=NO_TAREA.format()

    html=HTML.format(t_p=tareas_pendientes_html, t_c=tareas_completadas_html)

    STYLES_PATH.write_text(STYLES.format(), encoding="utf-8")    
    HTML_PATH.write_text(html,encoding="utf-8")

    if __name__ == "__main__":
        main()
