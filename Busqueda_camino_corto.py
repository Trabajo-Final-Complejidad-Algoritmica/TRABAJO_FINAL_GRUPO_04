# -----------------------------------------------------------------------------
# ---------------------  Implementación de disjktra    ------------------------
# -----------------------------------------------------------------------------

import tkinter as tk
from tkinter.ttk import Combobox, Button, Label
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

cant_crimines = {
    "Central":      107,
    "Rampart":      68,
    "Southwest":    88,
    "Hollenbeck":   70,
    "Harbor":       66,
    "Hollywood":    70,
    "Wilshire":     94,
    "West LA":      100,
    "Van Nuys":     73,
    "West Valley":  85,
    "Northeast":    89,
    "77th Street":  93,
    "Newton":       92,
    "Pacific":      83,
    "N Hollywood":  106,
    "Foothill":     54,
    "Devonshire":   94,
    "Southeast":    77,
    "Mission":      68,
    "Olympic":      72,
    "Topanga":      68
}

areas = {
    "Central":      "1",
    "Rampart":      "2",
    "Southwest":    "3",
    "Hollenbeck":   "4",
    "Harbor":       "5",
    "Hollywood":    "6",
    "Wilshire":     "7",
    "West LA":      "8",
    "Van Nuys":     "9",
    "West Valley":  "10",
    "Northeast":    "11",
    "77th Street":  "12",
    "Newton":       "13",
    "Pacific":      "14",
    "N Hollywood":  "15",
    "Foothill":     "16",
    "Devonshire":   "17",
    "Southeast":    "18",
    "Mission":      "19",
    "Olympic":      "20",
    "Topanga":      "21"
}

graph = {
    "AREA": {
        "1": {"4": 6, "2": 4, "13": 2, "3": 3, "11": 2},  ## Distancias aproximados.
        "2": {"1": 4, "11": 4, "6": 2, "20": 3, "7": 1, "3": 2},
        "3": {"14": 3, "20": 4, "7": 1, "2": 2, "1": 3, "13": 5, "12": 5},
        "4": {"1": 6, "13": 4, "11": 3},
        "5": {"18": 4, "12": 1},
        "6": {"7": 2, "11": 4, "2": 2, "20": 3, "15": 2},
        "7": {"6": 2, "20": 6, "11": 3, "2": 1, "15": 2, "3": 1},
        "8": {"14": 5, "10": 2},
        "9": {"10": 3, "19": 5, "16": 3, "15": 2},
        "10": {"9": 3, "19": 3, "8": 2, "15": 2, "17": 3, "21": 5},
        "11": {"2": 4, "6": 4, "1": 2, "4": 3, "7": 3},
        "12": {"18": 4, "3": 5, "13": 2, "14": 1, "5": 1},
        "13": {"3": 5, "12": 2, "18": 2, "1": 2, "4": 4},
        "14": {"8": 5, "7": 1, "3": 1, "12": 1},
        "15": {"6": 2, "7": 2, "10": 2, "9": 2, "16": 3},
        "16": {"15": 3, "9": 3, "19": 2},
        "17": {"21": 3, "19": 2, "10": 3},
        "18": {"12": 4, "13": 2, "5": 4},
        "19": {"9": 5, "10": 3, "16": 1, "15": 2, "17": 2},
        "20": {"7": 6, "2": 3, "6": 3, "1": 1, "3": 4, "14": 1},
        "21": {"17": 3, "10": 5}
    }
}

G = nx.Graph()

for area, num_area in areas.items():  # agregar nodos
    G.add_node(num_area, label=area)

# Agregar aristas al grafo con los números correspondientes
for num_area, neighbors in graph["AREA"].items():
    for neighbor, weight in neighbors.items():
        G.add_edge(num_area, neighbor, weight=weight)


def Buscar_Ruta_Corta():
    area_origen = area1.get()
    area_destino = area2.get()

    if area_origen == area_destino:
        resultado.config(text="\tAreas invalidas !!!")
        return

    try:
        num_origen = areas[area_origen]
        num_destino = areas[area_destino]

        ruta_corta = nx.dijkstra_path(G, num_origen, num_destino, weight='weight')
        calcular_distancia = nx.dijkstra_path_length(G, num_origen, num_destino, weight='weight')

        ruta_nombres = [G.nodes[num]['label'] for num in ruta_corta]
        ruta_str = "\n -> ".join(ruta_nombres)
        resultado.config(text=f"RUTA RECOMENDADA Y SEGURA:\n\n -> {ruta_str}\n\nDistancia: {calcular_distancia} Kilómetros Apróx.")

        edges = list(zip(ruta_corta, ruta_corta[1:]))
        ax.clear()
        pos = nx.spring_layout(G)
        labels = {num: G.nodes[num]['label'] for num in G.nodes}
        nx.draw(G, pos, with_labels=True, labels=labels, node_color='lightblue', node_size=800, edge_color='gray', ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color='green', width=2.0, ax=ax)

        canvas.draw()

    except KeyError:
        resultado.config(text="Error!!")

# Crear la ventana principal
ventana = tk.Tk()
ventana.geometry("800x650")
ventana.title("Trabajo Final - Universidad Peruana de Ciencias Aplicadas")
ventana.iconbitmap("U.ico")

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
