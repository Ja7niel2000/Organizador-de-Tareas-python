import json
from AgendaModule.tarea import Tarea
from AgendaModule.repo import AgendaRepo
from pathlib import Path

PATH_DB = Path("Tareas.json")
HTML_PATH = Path("index.html")
STYLES_PATH=Path("styles.css")
one="{"
two="}"
STYLES=""" 
:root{
    /* --color-secundario:#5170AE;
    --color-primario:#4993B6; */

      /* --color-secundario:#21396A; */
    /* --color-primario:#13303E; */

    
    --color-secundario:#B24D4D;
    --color-primario:#043D58;
    
    /* --color-secundario:#664DB2;
    --color-primario:#4A45BA; */
    --font-color:#000000;
    --font-color:#ffffff;

    --color-table-bg:#fff;
    --font-table-color:#000;
    --color-table-header:#555;
    --color-table-header:#E6E6E6;
    --color-table-row:#fff;
    --shadow-table-color:#000;

}

*{
    font-size: 12px;
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
    font-size: 3em;
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
    border-radius: 10px 10px 0 0;

   
}

h2{
    padding: 5px 5px 0px 5px;
    margin: 0;
    font-size: 2em;
}

.tableContainer{
    width: 100%;
    background-color: var(--color-table-bg);
    padding: 10px;
    padding-top: 10px;
    margin-bottom: 50px;
    border-radius: 0 0 10px 10px;

    /*
    background-color: #55555;
      */
}

.headers{
    background-color: var(--color-table-header);
    height: 30px;
    border-radius:15px;
    font-weight: bold; 
    color: var(--font-table-color);   
}

.row{
    min-height: 40px;
    display:grid;
    grid-template-columns:0.15fr 1fr 0.3fr 0.5fr 1fr 0.8fr;
    margin:10px 0;
    padding: 1px;
    box-shadow: 0px 0px 15px -10px var(--shadow-table-color);
    color: var(--font-table-color);   
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
    border-radius: 10px 10px 0 0;
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
                    ❌ Tareas Pendientes: {i1}
                </h2>
        </div>
        <div class="tableContainer">
            {header1}

            {t_p}
        </div>

        <div class="containerLabel">
            <h2>
                    ✅ Tareas Completas: {i2}
            </h2>
        </div>
        
        <div class="tableContainer">
            {header2}

            {t_c}
        </div>
    
    </main>
    <footer>
        <div class="footerContainer">
            <p class="footerContainerInfo">Tarea para la asignatura "Modelado y programación" de la carrera de ciencias de la computación, UNAM</p>
            
            <div class="nombresEquipoContainer">
                <div class="nombresEquipo">
                    <p>Equipo: </p>
                    <p>Jatniel Carranza Bolaños</p>
                    <p>Leonardo Téllez Piña</p>
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
    <div class="voidTareas">
        <p>No hay tareas</p>
    </div>
"""

TAREA_HEADER="""
<div class="row headers">
    <div id="numero">#</div>
    <div id="titulo">Titulo</div>
    <div id="prioridad">Prioridad</div>
    <div id="fecha">Fecha</div>
    <div id="descripción">Descripción</div>
    <div id="etiquetas">Etiquetas</div>
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
    tareas=repo.tareas
    tareas_completadas=sorted([t for t in tareas if t.completada ],key=lambda t: t.prioridad, reverse=True)
    tareas_pendientes=sorted([t for t in tareas if not t.completada],key=lambda t:t.prioridad,reverse=True)
    
    i1=0
    i2=0
    for t in tareas_completadas:
        i2=i2+1
        etiquetas=""
        for eti in t.etiquetas:
            etiquetas+=eti+", "
        tareas_completadas_html+=TAREA_TEMPLATE.format(
        id=t.id,
        i_=i2,
        ti=t.titulo,
        pr=t.prioridad,
        fe=t.fecha,
        de=t.descripcion,
        et=etiquetas[0:len(etiquetas)-2]
        )
    for t in tareas_pendientes:
        i1=i1+1
        etiquetas=""
        for eti in t.etiquetas:
            etiquetas+=eti+", "
        tareas_pendientes_html+=TAREA_TEMPLATE.format(
        id=t.id,
        i_=i1,
        ti=t.titulo,
        pr=t.prioridad,
        fe=t.fecha,
        de=t.descripcion,
        et=etiquetas[0:len(etiquetas)-2]
        )

    header1=TAREA_HEADER.format()  
    header2=TAREA_HEADER.format()     

    if(tareas_pendientes_html==""):
        tareas_pendientes_html=NO_TAREA
        header1=""


    if(tareas_completadas_html==""):
        tareas_completadas_html=NO_TAREA
        header2=""

         
    html=HTML.format(header1=header1,header2=header2, t_p=tareas_pendientes_html, t_c=tareas_completadas_html,i1=i1,i2=i2)

    STYLES_PATH.write_text(STYLES, encoding="utf-8")    
    HTML_PATH.write_text(html,encoding="utf-8")

if __name__ == "__main__":
    main()
