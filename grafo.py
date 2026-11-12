
"""
Titulo: Buenas prácticas
Nombre completo: Benjamín Peredo Alonso
Descripcion: Manejo de nodos, conexiones y algoritmo de Dijkstra.
"""

import csv


class Nodo:
    """Representa un punto de la red de transporte."""

    def __init__(self, nombre: str) -> None:
        self.nombre: str = nombre
        self.vecinos: dict[str, float] = {}


class Grafo:
    """Administra los nodos y sus conexiones."""

    def __init__(self) -> None:
        self.nodos: dict[str, Nodo] = {}

    def agregar_nodo(self, nombre: str) -> None:
        """Agrega un nodo solamente si todavía no existe."""
        if nombre not in self.nodos:
            self.nodos[nombre] = Nodo(nombre)

    def agregar_conexion(
        self, origen: str, destino: str, peso: float
    ) -> None:
        """Conecta dos nodos y guarda el peso del recorrido."""

        if origen == destino:
            raise ValueError("Un nodo no puede conectarse consigo mismo.")

        if peso <= 0:
            raise ValueError("El peso debe ser mayor que cero.")

        if origen in self.nodos:
            if destino in self.nodos[origen].vecinos:
                raise ValueError("Esta conexión ya existe.")

        self.agregar_nodo(origen)
        self.agregar_nodo(destino)

        self.nodos[origen].vecinos[destino] = peso
        self.nodos[destino].vecinos[origen] = peso

    def cargar_csv(self, ruta: str) -> None:
        """Lee las conexiones guardadas en el archivo CSV."""

        with open(ruta, mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)

            columnas = {"origen", "destino", "peso"}

            if not columnas.issubset(lector.fieldnames or []):
                raise ValueError("El CSV no tiene las columnas necesarias.")

            for fila in lector:
                origen = fila["origen"].strip().upper()
                destino = fila["destino"].strip().upper()
                peso = float(fila["peso"])

                self.agregar_conexion(origen, destino, peso)

    def dijkstra(
        self, inicio: str, destino: str
    ) -> tuple[float, list[str]]:
        """Busca el camino de menor peso entre dos nodos."""

        if inicio not in self.nodos or destino not in self.nodos:
            raise ValueError("El nodo de inicio o destino no existe.")

        distancias: dict[str, float] = {}
        anteriores: dict[str, str | None] = {}
        visitados: set[str] = set()

        # Al principio, todos los nodos tienen distancia infinita.
        for nombre in self.nodos:
            distancias[nombre] = float("inf")
            anteriores[nombre] = None

        distancias[inicio] = 0

        while len(visitados) < len(self.nodos):
            nodo_actual = None
            menor_distancia = float("inf")

            # Buscamos el nodo pendiente con menor distancia.
            for nombre in self.nodos:
                if nombre not in visitados:
                    if distancias[nombre] < menor_distancia:
                        menor_distancia = distancias[nombre]
                        nodo_actual = nombre

            if nodo_actual is None:
                break

            if nodo_actual == destino:
                break

            visitados.add(nodo_actual)

            for vecino, peso in self.nodos[nodo_actual].vecinos.items():
                nueva_distancia = distancias[nodo_actual] + peso

                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    anteriores[vecino] = nodo_actual

        # Si no hay conexión entre el inicio y el destino.
        if distancias[destino] == float("inf"):
            return float("inf"), []

        # Reconstruimos el camino encontrado.
        camino: list[str] = []
        actual: str | None = destino

        while actual is not None:
            camino.append(actual)
            actual = anteriores[actual]

        camino.reverse()

        return distancias[destino], camino
