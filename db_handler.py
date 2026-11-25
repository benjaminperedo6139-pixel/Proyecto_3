"""
Titulo: Proyecto 4 - Persistencia relacional con SQLite
Nombre completo: Benjamín Peredo Alonso
Descripcion: Único módulo que se comunica con la base de datos SQLite.
             Guarda los nodos y sus conexiones en tablas normalizadas.
"""

import os
import sqlite3
from contextlib import closing


RUTA_DB = os.path.join(os.path.dirname(__file__), "nodos.db")


def conectar() -> sqlite3.Connection:
    """Abre la base de datos y crea las tablas si todavía no existen."""

    con = sqlite3.connect(RUTA_DB)

    # SQLite no revisa las llaves foráneas si no se activa esta opción.
    con.execute("PRAGMA foreign_keys = ON")

    con.executescript("""
        CREATE TABLE IF NOT EXISTS nodos (
            id_nodo INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE CHECK (nombre <> '')
        );

        CREATE TABLE IF NOT EXISTS conexiones (
            id_conexion INTEGER PRIMARY KEY AUTOINCREMENT,
            id_origen INTEGER NOT NULL,
            id_destino INTEGER NOT NULL,
            peso REAL NOT NULL CHECK (peso > 0),
            CHECK (id_origen <> id_destino),
            FOREIGN KEY (id_origen) REFERENCES nodos (id_nodo),
            FOREIGN KEY (id_destino) REFERENCES nodos (id_nodo)
        );
    """)

    return con


def limpiar_nodo(texto: str) -> str:
    """Quita espacios y comprueba que el nodo sea una sola letra."""

    nodo = texto.strip().upper()

    if not nodo:
        raise ValueError("El nombre del nodo no puede estar vacío.")

    if len(nodo) != 1 or not nodo.isalpha():
        raise ValueError("El nodo debe ser una sola letra.")

    return nodo


def existe_conexion(
    con: sqlite3.Connection, origen: str, destino: str
) -> bool:
    """Revisa si la conexión ya existe en cualquiera de los dos sentidos."""

    fila = con.execute(
        """
        SELECT 1
        FROM conexiones AS c
        JOIN nodos AS o ON c.id_origen = o.id_nodo
        JOIN nodos AS d ON c.id_destino = d.id_nodo
        WHERE (o.nombre = ? AND d.nombre = ?)
           OR (o.nombre = ? AND d.nombre = ?)
        """,
        (origen, destino, destino, origen),
    ).fetchone()

    return fila is not None


def obtener_id_nodo(con: sqlite3.Connection, nombre: str) -> int:
    """Devuelve el id del nodo y lo registra si todavía no existe."""

    con.execute(
        "INSERT OR IGNORE INTO nodos (nombre) VALUES (?)",
        (nombre,),
    )
    fila = con.execute(
        "SELECT id_nodo FROM nodos WHERE nombre = ?",
        (nombre,),
    ).fetchone()

    return fila[0]


def guardar_conexion(origen: str, destino: str, peso: float) -> None:
    """Valida y guarda una nueva conexión entre dos nodos."""

    origen = limpiar_nodo(origen)
    destino = limpiar_nodo(destino)

    if origen == destino:
        raise ValueError("Un nodo no puede conectarse consigo mismo.")

    if peso <= 0:
        raise ValueError("El peso debe ser mayor que cero.")

    try:
        with closing(conectar()) as con:
            if existe_conexion(con, origen, destino):
                raise ValueError("Esta conexión ya existe.")

            id_origen = obtener_id_nodo(con, origen)
            id_destino = obtener_id_nodo(con, destino)

            con.execute(
                """
                INSERT INTO conexiones (id_origen, id_destino, peso)
                VALUES (?, ?, ?)
                """,
                (id_origen, id_destino, peso),
            )
            con.commit()

    except sqlite3.IntegrityError as error:
        raise ValueError(f"La base de datos rechazó los datos: {error}")
    except sqlite3.OperationalError as error:
        raise RuntimeError(f"No se pudo guardar la conexión: {error}")
    except sqlite3.DatabaseError as error:
        raise RuntimeError(f"La base de datos no es válida: {error}")


def leer_conexiones() -> list[dict[str, str | float]]:
    """Consulta las conexiones con JOIN para obtener los nombres."""

    try:
        with closing(conectar()) as con:
            filas = con.execute("""
                SELECT o.nombre, d.nombre, c.peso
                FROM conexiones AS c
                JOIN nodos AS o ON c.id_origen = o.id_nodo
                JOIN nodos AS d ON c.id_destino = d.id_nodo
                ORDER BY c.id_conexion
            """).fetchall()

    except sqlite3.OperationalError as error:
        raise RuntimeError(f"No se pudo leer la base de datos: {error}")
    except sqlite3.DatabaseError as error:
        raise RuntimeError(f"La base de datos no es válida: {error}")

    conexiones = []

    for origen, destino, peso in filas:
        conexiones.append({
            "origen": origen,
            "destino": destino,
            "peso": float(peso),
        })

    return conexiones
