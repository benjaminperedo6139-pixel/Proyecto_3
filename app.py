"""
Proyecto 2 - Dijkstra
Interfaz visual creada con Streamlit.
Utiliza grafo.py para Dijkstra e io_handler.py para validar
y guardar las conexiones en el archivo CSV.
"""

import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

import io_handler
from grafo import Grafo


# ---------------------------------------------------------
# Configuración de la página
# ---------------------------------------------------------

st.set_page_config(
    page_title="Dijkstra - Rutas Óptimas",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# Funciones para cargar y mostrar información
# ---------------------------------------------------------

def cargar_grafo() -> Grafo:
    """Carga las conexiones guardadas en el CSV."""
    grafo = Grafo()

    if io_handler.leer_csv():
        grafo.cargar_csv(io_handler.RUTA_CSV)

    return grafo


def leer_conexiones() -> list[dict[str, str | float]]:
    """Prepara las conexiones para mostrarlas en la tabla."""
    conexiones = []

    for fila in io_handler.leer_csv():
        conexiones.append({
            "Origen": fila["origen"],
            "Destino": fila["destino"],
            "Peso": fila["peso"],
        })

    return conexiones


def crear_grafo_visual(grafo: Grafo):
    """Dibuja la red de conexiones con nodos y pesos."""

    red = nx.Graph()

    for nombre in grafo.nodos:
        red.add_node(nombre)

    for origen, nodo in grafo.nodos.items():
        for destino, peso in nodo.vecinos.items():
            red.add_edge(origen, destino, weight=peso)

    posiciones = nx.spring_layout(
        red,
        seed=42,
        k=1.3,
        iterations=100,
    )

    figura, ax = plt.subplots(figsize=(8, 5))
    figura.patch.set_facecolor("#151526")
    ax.set_facecolor("#151526")

    nx.draw_networkx_edges(
        red,
        posiciones,
        ax=ax,
        edge_color="#AAA0D0",
        width=2.5,
    )

    nx.draw_networkx_nodes(
        red,
        posiciones,
        ax=ax,
        node_color="#673DE6",
        edgecolors="#A58AFF",
        linewidths=2,
        node_size=1100,
    )

    nx.draw_networkx_labels(
        red,
        posiciones,
        ax=ax,
        font_size=13,
        font_color="white",
        font_weight="bold",
    )

    pesos = nx.get_edge_attributes(red, "weight")

    nx.draw_networkx_edge_labels(
        red,
        posiciones,
        edge_labels=pesos,
        ax=ax,
        font_size=11,
        font_color="white",
        label_pos=0.5,
        rotate=False,
        bbox={
            "facecolor": "#25233A",
            "edgecolor": "none",
            "alpha": 0.9,
        },
    )

    ax.axis("off")
    figura.tight_layout()

    return figura


# ---------------------------------------------------------
# Estilo visual
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0d0d18 0%, #151526 100%);
        color: #f4f2ff;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #202033 0%, #171727 100%);
        border-right: 1px solid #34344d;
    }
    h1, h2, h3 {
        color: #f7f5ff !important;
    }
    .subtitle {
        color: #b9b7d0;
        font-size: 1.05rem;
        margin-top: -12px;
    }
    .route-card {
        background: linear-gradient(110deg, #12372d, #17352f);
        border: 1px solid #239b69;
        border-radius: 14px;
        padding: 18px;
        margin-top: 12px;
    }
    .route-title {
        color: #80e6ae;
        font-size: 1.15rem;
        font-weight: 700;
    }
    .route-path {
        color: #f3efff;
        font-size: 1.15rem;
        margin-top: 7px;
    }
    .route-cost {
        color: #b78cff;
        font-size: 1.45rem;
        font-weight: 700;
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #6337df, #8055f5);
        border: 0;
        border-radius: 10px;
        color: white;
        font-weight: 600;
    }
    div[data-testid="stMetric"] {
        background: #1c1c2d;
        border: 1px solid #34344d;
        padding: 14px;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Barra lateral
# ---------------------------------------------------------

with st.sidebar:
    st.markdown(
        "<div style='text-align:center; font-size:3.5rem;'>📍</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h1 style='text-align:center;'>Dijkstra</h1>"
        "<p style='text-align:center;color:#c5c2dc;'>"
        "Encuentra la ruta más corta</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    seccion = st.radio(
        "Navegación",
        ["Inicio", "Agregar conexiones", "Ver datos", "Acerca de"],
        label_visibility="collapsed",
    )

    st.divider()
    st.caption("Proyecto 2 de Programación 3")
    st.caption("Algoritmo de Dijkstra")
    st.caption("Benjamín Peredo Alonso")


# ---------------------------------------------------------
# Cargar datos
# ---------------------------------------------------------

try:
    grafo = cargar_grafo()
    conexiones = leer_conexiones()
except (FileNotFoundError, PermissionError, ValueError, KeyError) as error:
    st.error(f"No se pudieron cargar los datos: {error}")
    st.stop()


# ---------------------------------------------------------
# Página de inicio
# ---------------------------------------------------------

if seccion == "Inicio":
    st.title("Algoritmo de Dijkstra")
    st.markdown(
        '<p class="subtitle">Visualiza y encuentra la ruta más corta '
        "entre los nodos de tu red de transporte.</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<hr style='border:1px solid #7549ef; margin: 18px 0 24px 0;'>",
        unsafe_allow_html=True,
    )

    columna_grafo, columna_busqueda = st.columns([1.05, 1])

    with columna_grafo:
        st.subheader("🔗 Grafo actual")

        if grafo.nodos:
            figura = crear_grafo_visual(grafo)
            st.pyplot(figura, use_container_width=True)
            plt.close(figura)
        else:
            st.info("Todavía no hay conexiones. Agrega algunas para visualizar la red.")

    with columna_busqueda:
        st.subheader("🔎 Buscar ruta")
        nodos_disponibles = sorted(grafo.nodos)

        if len(nodos_disponibles) >= 2:
            origen_col, destino_col = st.columns(2)

            with origen_col:
                inicio = st.selectbox(
                    "Nodo de origen",
                    nodos_disponibles,
                    key="inicio",
                )

            with destino_col:
                destino = st.selectbox(
                    "Nodo de destino",
                    nodos_disponibles,
                    index=1,
                    key="destino",
                )

            if st.button(
                "Encontrar ruta",
                type="primary",
                use_container_width=True,
            ):
                try:
                    distancia, camino = grafo.dijkstra(inicio, destino)

                    if camino:
                        st.session_state["resultado_ruta"] = {
                            "inicio": inicio,
                            "destino": destino,
                            "distancia": distancia,
                            "camino": camino,
                        }
                    else:
                        st.session_state["resultado_ruta"] = None
                        st.warning("No existe una ruta entre esos nodos.")
                except ValueError as error:
                    st.error(str(error))
        else:
            st.info("Necesitas al menos dos nodos para buscar una ruta.")

        resultado = st.session_state.get("resultado_ruta")

        if resultado:
            st.markdown(
                f"""
                <div class="route-card">
                    <div class="route-title">✓ Ruta encontrada</div>
                    <div class="route-path">
                        Ruta más corta: {' → '.join(resultado['camino'])}
                    </div>
                    <div style="margin-top:8px;color:#ded9ed;">
                        Costo total:
                        <span class="route-cost">{resultado['distancia']:g}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    columna_tabla, columna_info = st.columns([0.85, 1.45])

    with columna_tabla:
        st.subheader("📋 Conexiones en la red")
        if conexiones:
            st.dataframe(
                conexiones,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No hay conexiones guardadas.")

    with columna_info:
        st.subheader("💡 ¿Cómo funciona?")
        pasos = [
            "Se parte del nodo de origen.",
            "Se revisan las conexiones disponibles.",
            "Se elige el nodo pendiente con menor distancia.",
            "Se actualizan los costos y se muestra la ruta óptima.",
        ]

        for numero, paso in enumerate(pasos, start=1):
            st.markdown(f"**{numero}.** {paso}")


# ---------------------------------------------------------
# Agregar conexiones
# ---------------------------------------------------------

elif seccion == "Agregar conexiones":
    st.title("Agregar conexiones")
    st.markdown(
        '<p class="subtitle">Registra nuevos caminos en la red de transporte.</p>',
        unsafe_allow_html=True,
    )

    with st.form("formulario_conexion", clear_on_submit=True):
        col_origen, col_destino, col_peso = st.columns(3)

        with col_origen:
            origen_texto = st.text_input(
                "Nodo de origen",
                max_chars=1,
            )

        with col_destino:
            destino_texto = st.text_input(
                "Nodo de destino",
                max_chars=1,
            )

        with col_peso:
            peso_texto = st.text_input("Peso de la conexión")

        enviar = st.form_submit_button(
            "Guardar conexión",
            type="primary",
            use_container_width=True,
        )

    if enviar:
        try:
            # Se reutilizan las validaciones de io_handler.py.
            origen = io_handler.validar_nodo(origen_texto)
            destino = io_handler.validar_nodo(destino_texto)
            peso = io_handler.validar_peso(peso_texto)

            if origen == destino:
                raise ValueError("Un nodo no puede conectarse consigo mismo.")

            # Primero se comprueba que la conexión se pueda agregar al grafo.
            grafo.agregar_conexion(origen, destino, peso)

            # Después se guarda usando la función de io_handler.py.
            nueva_conexion = [{
                "origen": origen,
                "destino": destino,
                "peso": peso,
            }]
            io_handler.guardar_csv(nueva_conexion)

            st.success(f"Conexión {origen} — {destino} guardada correctamente.")
            st.rerun()

        except ValueError as error:
            st.error(str(error))
        except (PermissionError, OSError) as error:
            st.error(f"No se pudo guardar el archivo CSV: {error}")

    st.subheader("Conexiones registradas")
    if conexiones:
        st.dataframe(conexiones, use_container_width=True, hide_index=True)
    else:
        st.info("Todavía no hay conexiones registradas.")


# ---------------------------------------------------------
# Ver datos
# ---------------------------------------------------------

elif seccion == "Ver datos":
    st.title("Datos de la red")
    st.markdown(
        '<p class="subtitle">Consulta los nodos y las conexiones almacenadas.</p>',
        unsafe_allow_html=True,
    )

    metrica_nodos, metrica_conexiones = st.columns(2)
    metrica_nodos.metric("Nodos registrados", len(grafo.nodos))
    metrica_conexiones.metric("Conexiones registradas", len(conexiones))

    st.subheader("Archivo Nodos.csv")
    if conexiones:
        st.dataframe(conexiones, use_container_width=True, hide_index=True)

        with open(io_handler.RUTA_CSV, "rb") as archivo:
            contenido_csv = archivo.read()

        st.download_button(
            "Descargar CSV",
            data=contenido_csv,
            file_name="Nodos.csv",
            mime="text/csv",
        )
    else:
        st.info("El archivo todavía no contiene conexiones.")

    st.subheader("Visualización de la red")
    if grafo.nodos:
        figura = crear_grafo_visual(grafo)
        st.pyplot(figura, use_container_width=True)
        plt.close(figura)


# ---------------------------------------------------------
# Acerca de
# ---------------------------------------------------------

elif seccion == "Acerca de":
    st.title("Acerca del proyecto")
    st.markdown(
        """
        ### Proyecto 2 - Programación 3

        Esta aplicación permite administrar una red de transporte y encontrar
        rutas de menor costo mediante el algoritmo de Dijkstra.

        **Funciones principales:**
        - Registrar nodos y conexiones.
        - Asignar un peso a cada conexión.
        - Guardar los datos en un archivo CSV.
        - Consultar las conexiones existentes.
        - Encontrar la ruta más corta entre dos nodos.

        **Tecnologías utilizadas:**
        - Python
        - Streamlit
        - CSV
        - Algoritmo de Dijkstra
        """
    )
