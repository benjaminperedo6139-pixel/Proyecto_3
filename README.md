# Proyecto 4 - Dijkstra con SQLite

**Autor:** Benjamín Peredo Alonso
**Materia:** Programación III

## ¿Qué es este programa?

[Explica en 3-5 líneas, como se lo contarías a un compañero: qué problema
resuelve, qué es un nodo y una conexión en tu red de transporte, y qué
hace Dijkstra.]

## ¿Cómo funciona?

[Describe el recorrido con tus palabras: qué pasa cuando abres la app,
qué pasa al guardar una conexión y qué pasa al buscar una ruta.
Pista: menciona que los datos viven en nodos.db y que la app los guarda
en memoria con st.session_state para no consultar la base en cada clic.]

## Estructura del proyecto

```
proyecto/
├── app.py            # Interfaz en Streamlit (sin sqlite3 ni pandas)
├── db_handler.py     # Toda la comunicación con SQLite
├── grafos.py         # Clases Nodo y Grafo, y el algoritmo de Dijkstra
├── nodos.db          # Base de datos con conexiones de prueba
├── requirements.txt  # Librerías y versiones
└── README.md
```

## Base de datos

La base `nodos.db` tiene dos tablas relacionadas:

- **nodos**: `id_nodo` (llave primaria) y `nombre` (único, no vacío).
- **conexiones**: `id_conexion` (llave primaria), `id_origen` e
  `id_destino` (llaves foráneas hacia `nodos`) y `peso` (mayor que 0).

Para mostrar las conexiones con los nombres de los nodos se usa un `JOIN`
entre las dos tablas.

[Explica con tus palabras por qué es mejor separar los datos en dos tablas
que guardarlos en una sola, como en el CSV.]

## Herramientas utilizadas

- Python 3.13.18
- Streamlit 1.67.0, NetworkX 3.7 y Matplotlib 3.11.2
- SQLite (módulo `sqlite3`, incluido en Python)
- DBeaver Community [tu versión]
- flake8 para revisar el estilo del código

## Cómo ejecutarlo

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

En Windows, el segundo comando es `.venv\Scripts\activate`.

## Cómo revisar la base en DBeaver

1. Nueva conexión → SQLite.
2. En *Path*, seleccionar el archivo `nodos.db` del proyecto.
3. En *Tables* aparecen `nodos` y `conexiones`; en *ER Diagram* se ven
   las llaves foráneas.

[Opcional pero recomendado: agrega aquí tus capturas de DBeaver.]

## Conclusión de la materia

[Escríbela tú. El PDF pide:
- Qué aprendiste a lo largo del semestre.
- Qué temas o dinámicas te gustaron más.
- Qué no te gustó.
- Qué áreas crees que puedes mejorar.]
