
"""
Titulo: Buenas prácticas
Nombre completo: Benjamín Peredo Alonso
Descripcion: Programa principal para administrar una red de transporte
             y encontrar rutas con Dijkstra.
"""

import os

import io_handler
from grafo import Grafo


def mostrar_resultado(
    grafo: Grafo,
    inicio: str,
    destino: str,
    distancia: float,
    camino: list[str]
) -> None:
    """Muestra la ruta encontrada y su peso total."""

    print("\n===== RESULTADO =====")

    if not camino:
        print(f"No existe una ruta de {inicio} a {destino}.")
        return

    print("Recorrido completo:")

    for i in range(len(camino) - 1):
        origen = camino[i]
        siguiente = camino[i + 1]
        peso = grafo.nodos[origen].vecinos[siguiente]

        print(f"{origen} -> {siguiente} | Peso: {peso}")

    print(f"\nRuta: {' -> '.join(camino)}")
    print(f"Peso total: {distancia}")


def cargar_grafo() -> Grafo:
    """Carga las conexiones que ya están guardadas en el CSV."""

    grafo = Grafo()

    if os.path.exists(io_handler.RUTA_CSV):
        grafo.cargar_csv(io_handler.RUTA_CSV)

    return grafo


def registrar_conexiones(grafo: Grafo) -> None:
    """Solicita nuevas conexiones y las guarda en el CSV."""

    conexiones = io_handler.pedir_conexiones()
    conexiones_guardadas = []

    for conexion in conexiones:
        try:
            grafo.agregar_conexion(
                conexion["origen"],
                conexion["destino"],
                float(conexion["peso"])
            )
            conexiones_guardadas.append(conexion)

        except ValueError as error:
            print(f"No se pudo agregar la conexión: {error}")

    if conexiones_guardadas:
        io_handler.guardar_csv(conexiones_guardadas)


def main() -> None:
    """Controla el funcionamiento general del programa."""

    print("===== RED DE TRANSPORTE =====")

    try:
        grafo = cargar_grafo()

        if grafo.nodos:
            print(f"Se cargaron {len(grafo.nodos)} nodos existentes.")

        registrar_conexiones(grafo)

        if not grafo.nodos:
            print("No hay conexiones para trabajar.")
            return

        while True:
            inicio, destino = io_handler.pedir_ruta(
                list(grafo.nodos)
            )

            distancia, camino = grafo.dijkstra(inicio, destino)

            mostrar_resultado(
                grafo, inicio, destino, distancia, camino
            )

            otra = input(
                "\n¿Quieres consultar otra ruta? (s/n): "
            ).strip().lower()

            if otra != "s":
                break

        print("\nPrograma finalizado. Los datos se conservaron en el CSV.")

    except (KeyboardInterrupt, EOFError):
        print("\nPrograma interrumpido por el usuario.")

    except (FileNotFoundError, PermissionError, ValueError) as error:
        print(f"\nNo se pudo completar la operación: {error}")


if __name__ == "__main__":
    main()
