# -----------------------------------------------------------------------------
# -----  Implementación de librerías tkinter and matplotlib    ----------------
# -----------------------------------------------------------------------------

import tkinter as tk
from tkinter.ttk import Combobox, Button, Label
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json


with open('JSON/cant_crimenes.txt', 'r') as file:
    cant_crimines = json.load(file)

with open('JSON/areas.txt', 'r') as file:
    areas = json.load(file)

with open('JSON/grafo.txt', 'r') as file:
    grafo = json.load(file)

G = nx.Graph() # Grafo vacío según la librería Networ

for area, num_area in areas.items():  # agregar nodos
    G.add_node(num_area, label=area)

# Agregar aristas al grafo con los números correspondientes
for num_area, neighbors in grafo["AREA"].items():
    for neighbor, weight in neighbors.items():
        G.add_edge(num_area, neighbor, weight=weight)


def Buscar_Ruta_Corta():
    area_origen = area1.get()
    area_destino = area2.get()

    if area_origen == area_destino:
        resultado.config(text="\tAreas iguales!")
        return

    try:
        num_origen = areas[area_origen]
        num_destino = areas[area_destino]

        ruta_corta = nx.dijkstra_path(G, num_origen, num_destino, weight='weight')
        calcular_distancia = nx.dijkstra_path_length(G, num_origen, num_destino, weight='weight')

        ruta_nombres = [G.nodes[num]['label'] for num in ruta_corta]
        ruta_str = "\n -> ".join(ruta_nombres)
        resultado.config(

            text=f"RUTA RECOMENDADA Y SEGURA:\n\n -> {ruta_str}\n\nDistancia: {calcular_distancia} Kilómetros Apróx.")

        edges = list(zip(ruta_corta, ruta_corta[1:]))
        ax.clear()
        pos = nx.spring_layout(G)
        labels = {num: G.nodes[num]['label'] for num in G.nodes}

        node_colors = ['#DC4E30' if cant_crimines[G.nodes[node]['label']] > 100 else '#6AA1DF' for node in G.nodes]

        nx.draw(G, pos, with_labels=True, labels=labels, node_color=node_colors, node_size=800, edge_color='gray',
                ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='green', width=2.0, ax=ax)

        canvas.draw()

    except KeyError:
        resultado.config(text="Error!!")

# Crear la ventana principal
ventana = tk.Tk()
ventana.geometry("800x650")
ventana.title("Trabajo Final - Universidad Peruana de Ciencias Aplicadas")
ventana.iconbitmap("JSON/U.ico")

# -----------------------------------------------------------------------------
# -----------------------  Listas desplegables en label  ----------------------
# -----------------------------------------------------------------------------
label1 = tk.Label(ventana, text="Área de origen:")
label1.place(x=10, y=10, width=100, height=30)
area1 = Combobox(ventana, values=list(areas.keys()))
area1.place(x=120, y=10, width=120, height=30)

label2 = tk.Label(ventana, text="Área de destino:")
label2.place(x=10, y=50, width=100, height=30)
area2 = Combobox(ventana, values=list(areas.keys()))
area2.place(x=120, y=50, width=120, height=30)

# -----------------------------------------------------------------------------
# ------------------  Botón para calcular la ruta más corta  ------------------
# -----------------------------------------------------------------------------
btn = Button(ventana, text="Buscar ruta", command=Buscar_Ruta_Corta, )
btn.place(x=130, y=90, width=100, height=30)

# -----------------------------------------------------------------------------
# --------------  Label para mostrar los resultados del camino  ---------------
# -----------------------------------------------------------------------------
resultado = Label(ventana, text="", wraplength=780, justify="left")
resultado.place(x=10, y=130, width=780, height=500)

# -----------------------------------------------------------------------------
# ---------------------  Figura para mostrar el grafo  ------------------------
# -----------------------------------------------------------------------------
fig = plt.Figure(figsize=(10, 7))
ax = fig.add_subplot(111)

# -----------------------------------------------------------------------------
# ------------------------  Grafo inicial al ejecutar  ------------------------
# -----------------------------------------------------------------------------
pos = nx.spring_layout(G)
labels = {num: G.nodes[num]['label'] for num in G.nodes}
nx.draw(G, pos, with_labels=True, labels=labels, node_color='lightblue', node_size=800, edge_color='gray', ax=ax)

# -----------------------------------------------------------------------------
# ---------------------------  Posición del gráfico  --------------------------
# -----------------------------------------------------------------------------
canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas.draw()
canvas.get_tk_widget().place(x=300, y=10)

# -----------------------------------------------------------------------------
# ---------------------------  Ventana Principal  -----------------------------
# -----------------------------------------------------------------------------

ventana.mainloop()
