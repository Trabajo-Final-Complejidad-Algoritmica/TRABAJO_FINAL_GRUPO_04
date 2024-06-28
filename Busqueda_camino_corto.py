import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
from tkinter import Tk, Button, Label, StringVar, messagebox
from tkinter.ttk import Combobox
import requests

# El resto del código sigue igual...


# -----------------------------------------------------------------------------
# ------------  Importamos los datos desde el JSON Server    ------------------
# -----------------------------------------------------------------------------

# Función para obtener los datos de crímenes por mes
def get_crime_data(month):
    url = "https://my-json-server.typicode.com/velardesoft/DataBase_CrimenData_LosAngeles_Universidad_Peruana_De_Ciencias_Aplicadas_2024_1/db"
    response = requests.get(url)
    data = response.json()

    for item in data["DataBase"]:
        if item["month"] == month:
            return item["data"]

    return None


# Función para actualizar el gráfico y la información
def update_graph(month):
    crime_data = get_crime_data(month)
    if crime_data:
        # Actualizar el diccionario de crímenes
        cant_crimenes = crime_data

        # Actualizar el grafo
        for area, num_area in areas.items():
            G.nodes[num_area]['label'] = area
            G.nodes[num_area]['crime'] = cant_crimenes[area]

        # Actualizar la visualización
        ax.clear()
        pos = nx.spring_layout(G)
        labels = {num: G.nodes[num]['label'] for num in G.nodes}
        node_colors = ['#DC4E30' if G.nodes[node]['crime'] > 100 else '#6AA1DF' for node in G.nodes]
        nx.draw(G, pos, with_labels=True, labels=labels, node_color=node_colors, node_size=600, edge_color='gray',
                ax=ax)
        canvas.draw()
    else:
        messagebox.showwarning("Alerta", f"No se encontraron datos de crímenes para el mes seleccionado.")


# -----------------------------------------------------------------------------
# -----------------------------  Grafo vació    -------------------------------
# -----------------------------------------------------------------------------

G = nx.Graph()

with open('JSON/areas.txt', 'r') as file:
    areas = json.load(file)

for area, num_area in areas.items():
    G.add_node(num_area, label=area, crime=0)

with open('JSON/grafo.txt', 'r') as file:
    grafo = json.load(file)

for num_area, neighbors in grafo["AREA"].items():
    for neighbor, weight in neighbors.items():
        G.add_edge(num_area, neighbor, weight=weight)


# -----------------------------------------------------------------------------
# ---------------------  Función implementada con disktra    ------------------
# -----------------------------------------------------------------------------
def Buscar_Ruta_Corta():
    area_origen = area1.get()
    area_destino = area2.get()

    if area_origen == area_destino:
        messagebox.showwarning("Alerta", "Áreas Iguales")
        return

    try:
        id_origin = areas[area_origen]
        id_destino = areas[area_destino]

        ruta_corta = nx.dijkstra_path(G, id_origin, id_destino, weight='weight')
        calcular_distancia = nx.dijkstra_path_length(G, id_origin, id_destino, weight='weight')

        Area_Visitada = [G.nodes[num]['label'] for num in ruta_corta]
        areas_seguras = "\n -> ".join(Area_Visitada)
        resultado.config(
            text=f"RUTA RECOMENDADA Y SEGURA:\n\n "
                 f"-> {areas_seguras}\n\n"
                 f"Distancia: {calcular_distancia} Kilómetros Apróx.")

        # Limpiar el gráfico
        ax.clear()

        # Generar un diccionario de colores para los nodos
        node_colors = {node: '#DC4E30' if G.nodes[node]['crime'] >= 100 else '#6AA1DF' for node in G.nodes}

        # Dibujar el grafo completo con los colores de los nodos
        pos = nx.spring_layout(G)
        labels = {num: G.nodes[num]['label'] for num in G.nodes}
        nx.draw(G, pos, with_labels=True, labels=labels, node_color=[node_colors[node] for node in G.nodes], node_size=600, edge_color='gray', ax=ax)

        # Dibujar las aristas de la ruta seleccionada
        edges = list(zip(ruta_corta, ruta_corta[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='green', width=2.0, ax=ax)

        canvas.draw()

        # Verificar si la ruta pasa por áreas de alto riesgo
        for num in ruta_corta:
            if G.nodes[num]['crime'] > 100:
                messagebox.showwarning("Alerta", "Zonas con alto riesgo de crimen!!")
                break

    except KeyError:
        resultado.config(text="Error!!")


# -----------------------------------------------------------------------------
# -------------------------  Crear la ventana principal  ----------------------
# -----------------------------------------------------------------------------
ventana = Tk()
ventana.geometry("800x650")
ventana.configure(bg="#3A2C6C")
ventana.title("Trabajo Final - Universidad Peruana de Ciencias Aplicadas")
ventana.iconbitmap("JSON/U.ico")

# -----------------------------------------------------------------------------
# -----------------------  Listas desplegables en label  ----------------------
# -----------------------------------------------------------------------------

label1 = Label(ventana, text="Área de origen:")
label1.place(x=10, y=110, width=100, height=30)
area1 = Combobox(ventana, values=list(areas.keys()))
area1.place(x=120, y=110, width=120, height=30)

label2 = Label(ventana, text="Área de destino:")
label2.place(x=10, y=150, width=100, height=30)
area2 = Combobox(ventana, values=list(areas.keys()))
area2.place(x=120, y=150, width=120, height=30)

# -----------------------------------------------------------------------------
# ------------------  Botón para calcular la ruta más corta  ------------------
# -----------------------------------------------------------------------------
btn = Button(ventana, text="Buscar ruta", command=Buscar_Ruta_Corta, bg="yellow", fg="black")
btn.place(x=110, y=200, width=100, height=30)

# -----------------------------------------------------------------------------
# ------------------  Botones para seleccionar el mes  ------------------------
# -----------------------------------------------------------------------------

months = ["Enero", "Febrero", "Marzo", "Abril",
          "Mayo", "Junio", "Julio", "Agosto",
          "Septiembre", "Octubre", "Noviembre", "Diciembre"]

rows = 3  # Número de filas
cols = 4  # Número de columnas por fila

for i, month in enumerate(months):
    row = i // cols
    col = i % cols
    btn = Button(ventana, text=month, command=lambda m=month: update_graph(m), bg="#6AA1DF", fg="white")
    btn.grid(row=row, column=col, padx=1, pady=1)

# -----------------------------------------------------------------------------
# --------------  Label para mostrar los RESULTADOS  ---------------
# -----------------------------------------------------------------------------
resultado = Label(ventana, text="", wraplength=780, justify="left")
resultado.place(x=20, y=240, width=255, height=400)

# -----------------------------------------------------------------------------
# ---------------------  Figura para mostrar el grafo  ------------------------
# -----------------------------------------------------------------------------
fig = plt.Figure(figsize=(10, 7))
ax = fig.add_subplot(111)

# -----------------------------------------------------------------------------
# ---------------------------  Posición del gráfico  --------------------------
# -----------------------------------------------------------------------------
canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas.draw()
canvas.get_tk_widget().place(x=300, y=0, width=1150)

# -----------------------------------------------------------------------------
# ------------------------  Grafo inicial al ejecutar  ------------------------
# -----------------------------------------------------------------------------
update_graph("Enero")  # Cargar los datos de Febrero por defecto

# -----------------------------------------------------------------------------
# ---------------------------  Ventana Principal  -----------------------------
# -----------------------------------------------------------------------------
ventana.mainloop()