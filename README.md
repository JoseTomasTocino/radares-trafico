# radares-trafico
Scraper para los radares de tráfico de la web de la DGT. Los radares para Cádiz se pueden ver en http://josetomastocino.github.io/radares-trafico/

## Contexto y motivación

Desde hace tiempo la [DGT](www.dgt.es) ha estado pendiente de publicar la ubicación de los radares móviles en las carreteras españolas. A principios de Julio de 2015, finalmente, publicaron en la web de la DGT los tramos de carretera en los que _"se intensifica la vigilancia"_ y es posible ubicar radares móviles. Esto tiene varios problemas:

* En primer lugar, se trata de **datos generales**, que no se actualizan diariamente sino que solo informan de los tramos en los que puede haber dispositivos de radar móviles, sin confirmación real. 
* En segundo lugar, los tramos indicados tienen en algunos casos decenas de **kilómetros de extensión**, por lo que resulta imposible saber exactamente dónde se ubican los radares, si los hubiera.
* Por último, como es habitual en las administraciones españolas, los datos **no se han publicado en ningún formato abierto**, por lo que es complicado utilizarlos como fuentes para otros proyectos.

Es por ello que me decidí a hacer un pequeño párser de estos datos, con objeto de poder disponer de los datos en un formato procesable, para así, por ejemplo, poder tener en un mapa dinámico los radares. Sí, es cierto que la DGT ha publicado mapas, [como este de Cádiz](http://www.dgt.es/Galerias/el-trafico/control-de-velocidad/Cadiz.jpg), pero salta a la vista que son francamente lamentables. 

## Orígenes de datos

Como se ha comentado, los datos no se encuentran en formatos abiertos en la web de la DGT, por lo que es necesario ir cogiendo _de aquí y de allá_ para poder ensamblar un conjunto de datos relevante. Es por ello que este proyecto cuenta con varios scripts que sacan datos de diversos sitios y van generando los ficheros necesarios.

### Datos de provincias

En primer lugar, el script `fetch_provinces.py` genera un listado de las provincias con información de radares, obteniendo además el código numérico de cada provincia y el nombre técnico de cada una, ambos datos usados a la hora de generar peticiones y formar URLs. El fichero que genera este script es `provinces.json`.

### Datos de carreteras

Seguidamente, el script `fetch_roads.py` genera un listado de todas las carreteras que están dadas de alta en el sistema eTraffic, guardando su código identificador. Es importante mencionar que no están todas la carreteras de España. El fichero que se genera es `roads.json`, y depende del anterior fichero para funcionar.

### Datos de radares

Finalmente, el script `fetch_radars.py` genera un listado de todos los radares de una provincia en particular (que se indica en la variable `current_city` del propio script), creando un fichero `radars.json`. Para cada radar, se guarda la siguiente información:

    {
        "province": "Cádiz", 
        "province_code": "11", 
        "kind": "Radar Fijo", 
        "kms": [
          645.4
        ], 
        "kms_gps": [
          {
            "lat": 36.648293, 
            "lng": -6.1757674
          }
        ], 
        "road_code": 55016, 
        "direction": "Decreciente", 
        "road": "A-4"
    }

Los atributos `kms` y `kms_gps` guardan respectivamente el punto kilométrico y las coordenadas GPS del radar. Para los radares fijos solo hay un punto kilométrico, pero para los radares móviles la DGT no indica un solo punto, sino que indica los pk de inicio y final de los tramos en los que _puede estar_ el radar, por lo que el script mete puntos intermedios cada 5 kilómetros.

La ubicación GPS de los puntos kilométricos también se scrapea del sistema eTraffic de la DGT.

## Ejecución

En el fichero `requirements.txt` se encuentran las dependencias de Python que es necesario instalar, preferiblemente dentro de un virtualenv, utilizando `pip`:

    pip install -r requirements.txt

Hecho esto, solo resta ejecutar los scripts en su orden:

    ./fetch_provinces.py
    ./fetch_roads.py
    ./fetch_radars.py

Esto generará los ficheros `.json` con la información. 

### Frontend de prueba

En el fichero `index.html` hay un fichero con un frontend que muestra un Google Maps con los radares de la provincia de Cádiz, cargados desde el fichero `radars.json`. Para que funcione es necesario lanzar la web desde un servidor, se puede hacer fácilmente con

    python -m SimpleHTTPServer

Y entrar en la web desde `http://localhost:8000`.



