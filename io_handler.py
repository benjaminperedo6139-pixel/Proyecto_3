"""
Titulo: Buenas prácticas
Nombre completo: Benjamín Peredo Alonso
Descripcion: Entrada de datos y almacenamiento de conexiones en CSV.
"""

import csv
import math
import os


RUTA_CSV = os.path.join(os.path.dirname(__file__), "Nodos.csv")
ENCABEZADOS = ["origen", "destino", "peso"]


def validar_nodo(texto: str) -> str:
    """Comprueba que el nombre del nodo sea una sola letra."""

    nodo = texto.strip().upper()

    if len(nodo) != 1 or not nodo.isalpha():
        raise ValueError("El nodo debe ser una sola letra.")

    return nodo


def validar_peso(texto: str) -> float:
    """Comprueba que el peso sea un número positivo."""

    try:
        peso = float(texto)
    except ValueError:
        raise ValueError("El peso debe ser un número.")

    if not math.isfinite(peso) or peso <= 0:
        raise ValueError("El peso debe ser mayor que cero.")

    return peso


def pedir_nodo(mensaje: str) -> str:
    """Solicita un nodo hasta recibir uno válido."""

    while True:
        try:
            return validar_nodo(input(mensaje))
        except ValueError as error:
            print(f"Error: {error}")


def pedir_peso() -> float:
    """Solicita el peso de una conexión."""

    while True:
        try:
            return validar_peso(input("Peso de la conexión: "))
        except ValueError as error:
            print(f"Error: {error}")


def pedir_conexiones() -> list[dict[str, str | float]]:
    """Recopila las nuevas conexiones."""

    conexiones = []

    print("\n===== REGISTRO DE CONEXIONES =====")
    print("Escribe los datos de las conexiones.")

    while True:
        origen = pedir_nodo("Nodo origen: ")
        destino = pedir_nodo("Nodo destino: ")

        if origen == destino:
            print("Error: Los nodos deben ser diferentes.")
            continue

        peso = pedir_peso()

        conexiones.append({
            "origen": origen,
            "destino": destino,
            "peso": peso
        })

        otra = input("¿Agregar otra conexión? (s/n): ").strip().lower()

        if otra != "s":
            break

    return conexiones


def guardar_csv(
    conexiones: list[dict[str, str | float]]
) -> None:
    """Agrega las nuevas conexiones sin borrar las anteriores."""

    archivo_existe = os.path.exists(RUTA_CSV)
    tiene_datos = archivo_existe and os.path.getsize(RUTA_CSV) > 0

    with open(RUTA_CSV, mode="a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=ENCABEZADOS)

        if not tiene_datos:
            escritor.writeheader()

        escritor.writerows(conexiones)

    print("Conexiones guardadas correctamente.")


def leer_csv() -> list[dict[str, str | float]]:
    """Lee las conexiones que ya están guardadas en el CSV."""

    conexiones = []

    if not os.path.exists(RUTA_CSV):
        return conexiones

    with open(RUTA_CSV, mode="r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            conexiones.append({
                "origen": fila["origen"],
                "destino": fila["destino"],
                "peso": float(fila["peso"])
            })

    return conexiones


def pedir_ruta(nodos: list[str]) -> tuple[str, str]:
    """Solicita el nodo inicial y el nodo de destino."""

    print(f"\nNodos disponibles: {', '.join(nodos)}")

    while True:
        inicio = pedir_nodo("Nodo de inicio: ")
        destino = pedir_nodo("Nodo de destino: ")

        if inicio in nodos and destino in nodos:
            return inicio, destino

        print("Error: Uno o ambos nodos no existen.")
