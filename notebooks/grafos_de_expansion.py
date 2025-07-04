# -*- coding: utf-8 -*-
"""GRAFOS DE EXPANSION

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11OBOVxYRX6t3JhIrcnX5gYMgq9nx4oro
"""

from IPython.display import display, HTML

html_button = """
<div style="text-align:center; margin:20px 0;">
  <a href="https://economiayetica.blogspot.com/" target="_blank"
     style="
       background-color: #007BFF;
       color: #ffffff;
       padding: 12px 24px;
       text-decoration: none;
       font-size: 18px;
       border-radius: 8px;
       box-shadow: 0 4px 6px rgba(0,0,0,0.1);
       display: inline-block;
       transition: background-color 0.3s ease;
     "
  >
    Mi Blog
  </a>
</div>
<p style="text-align:center; font-size:14px; color:#555;">
  Haz clic en el botón para leer la nota completa que explica en detalle los grafos <em>expander</em> y su relevancia.
</p>
"""

display(HTML(html_button))

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# Mapeo de IDs a títulos completos en español
id_to_title = {
    1: "Big Data y grafos",
    2: "Imagen expander",
    3: "Paradoja de expanders",
    4: "Autovalores y λ₂",
    5: "Ramanujan & Wigner",
    6: "Importancia en Big Data",
    7: "Glosario técnico",
    8: "Bibliografía",
    9: "Epílogo completo"
}

# Definir las aristas del DAG
edges = [
    (1, 2), (2, 3), (3, 4), (4, 5),
    (5, 6), (6, 7), (6, 8), (7, 9), (8, 9)
]

# Construir el grafo dirigido
G = nx.DiGraph()
G.add_nodes_from(id_to_title.keys())
G.add_edges_from(edges)

# Layout para posicionar los nodos
pos = nx.spring_layout(G, seed=42, k=1.2)

# Crear la figura con fondo oscuro
fig, ax = plt.subplots(figsize=(12, 6), facecolor='#0f1e2e')
ax.set_axis_off()
plt.subplots_adjust(top=0.85, right=0.75)

def update(frame):
    ax.clear()
    ax.set_facecolor('#0f1e2e')

    # Determinar el nodo actual para el subtítulo
    current = 1 if frame == 0 else edges[min(frame-1, len(edges)-1)][1]
    subtitle = id_to_title[current]
    ax.text(
        0.5, 0.92, subtitle,
        transform=fig.transFigure,
        ha='center', color='cyan', fontsize=14
    )

    # Dibujar todos los nodos en gris tenue
    nx.draw_networkx_nodes(
        G, pos,
        node_size=900, node_color='gray', alpha=0.3,
        edgecolors='white', linewidths=1, ax=ax
    )

    # Calcular los nodos alcanzados hasta este frame
    reached = {1}
    for i in range(max(frame, 1)):
        if i < len(edges):
            reached.add(edges[i][1])

    # Resaltar los nodos alcanzados en cian
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=list(reached),
        node_size=900, node_color='cyan', alpha=0.9,
        edgecolors='white', linewidths=1, ax=ax
    )

    # Dibujar las aristas hasta el frame actual
    drawn_edges = edges[:max(frame, 0)]
    nx.draw_networkx_edges(
        G, pos,
        edgelist=drawn_edges,
        edge_color='lightblue', width=2.5, ax=ax,
        arrowsize=12, arrowstyle='-|>'
    )

    # Etiquetas numéricas centradas
    nx.draw_networkx_labels(
        G, pos,
        labels={i: str(i) for i in G.nodes()},
        font_color='black', font_size=10, font_weight='bold',
        horizontalalignment='center', verticalalignment='center',
        ax=ax
    )

    return ax,

# Crear la animación (frames = número de aristas + 1)
ani = FuncAnimation(
    fig, update,
    frames=len(edges) + 1,
    interval=1000,  # 1 segundo por paso
    blit=False
)

# Guardar como MP4 y GIF
ani.save('dag_titulos_animacion.mp4', writer='ffmpeg', dpi=150, fps=1)
ani.save('dag_titulos_animacion.gif', writer='pillow', dpi=80, fps=1)

# Mostrar inline en un notebook
HTML(ani.to_jshtml())

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# — Parámetros —
n = 50             # número de nodos
d = 3              # grado regular
ram_limit = 2 * np.sqrt(d - 1)

# — 1) Crear grafo d‑regular aleatorio —
G = nx.random_regular_graph(d, n)

# — 2) Calcular autovalores —
A = nx.adjacency_matrix(G).toarray()
eigvals = np.sort(np.linalg.eigvals(A).real)

# — 3) Métricas —
cent = nx.eigenvector_centrality_numpy(G)
eb   = nx.edge_betweenness_centrality(G)

# — 4) Posiciones 3D sobre esfera —
theta = np.linspace(0, 2*np.pi, n, endpoint=False)
phi   = np.arccos(2*np.arange(n)/n - 1)
pos3d = {
    i: (
        np.cos(theta[i]) * np.sin(phi[i]),
        np.sin(theta[i]) * np.sin(phi[i]),
        np.cos(phi[i])
    )
    for i in range(n)
}

# — 5) Preparar figura y ejes —
plt.style.use('dark_background')
fig = plt.figure(figsize=(12, 6))
ax_graph    = fig.add_subplot(121, projection='3d')
ax_spectrum = fig.add_subplot(122)

# Precomputar semicírculo de Wigner
sigma = np.sqrt(d - 1)
x_sc   = np.linspace(-2*sigma, 2*sigma, 400)
rho_sc = (1/(2*np.pi*sigma**2)) * np.sqrt(np.maximum(4*sigma**2 - x_sc**2, 0))

def draw_spectrum():
    ax_spectrum.clear()
    ax_spectrum.set_facecolor('#1b2309')
    # Histograma de densidad
    counts, bins, patches = ax_spectrum.hist(
        eigvals, bins=30, density=True,
        color='lightgray', edgecolor='white', alpha=0.6
    )
    # Semicírculo de Wigner
    ax_spectrum.fill_between(x_sc, rho_sc, color='cyan', alpha=0.3)
    ax_spectrum.plot(x_sc, rho_sc, color='cyan', lw=2)
    # Cotas Ramanujan
    for v in (+ram_limit, -ram_limit):
        ax_spectrum.axvline(v, color='blue', ls='--', lw=1.5)
    # Resaltar λ2 y λ_{n-1}
    for val in (eigvals[1], eigvals[-2]):
        c = 'green' if abs(val) <= ram_limit else 'red'
        ax_spectrum.axvline(val, color=c, lw=2)
        ax_spectrum.text(val, ax_spectrum.get_ylim()[1]*0.9,
                         f"{val:.2f}", color=c,
                         ha='center', va='bottom', fontsize=8)
    # Etiquetas y grid suave
    ax_spectrum.set_title("Distribución de autovalores", color='lime', pad=12)
    ax_spectrum.set_xlabel("Valor propio", color='white')
    ax_spectrum.set_ylabel("Densidad", color='white')
    ax_spectrum.tick_params(colors='white')
    ax_spectrum.yaxis.grid(True, color='white', alpha=0.1, ls='--')
    ax_spectrum.xaxis.grid(False)

# Dibujar espectro una sola vez
draw_spectrum()

# Barra de color para centralidad (solo una vez)
# Dibujamos un scatter de prueba para crear la colorbar
cax = fig.add_axes([0.15, 0.08, 0.3, 0.02])  # [left, bottom, width, height]
dummy = cax.imshow(
    np.linspace(0,1,256)[None, :],
    cmap='viridis',
    aspect='auto'
)
cax.set_xticks([0, 255])
cax.set_xticklabels(['baja', 'alta'], color='white')
cax.set_yticks([])
cax.set_title("Eigenvector Centrality", color='white', pad=2)

def update(frame):
    # — Grafo 3D —
    ax_graph.clear()
    ax_graph.set_facecolor('#1b2309')
    # Ortográfica
    try: ax_graph.set_proj_type('ortho')
    except: pass
    ax_graph.dist = 7
    angle = (frame * 4) % 360
    ax_graph.view_init(elev=20, azim=angle)
    # Aristas con gradiente plasma
    weights = np.array([eb[e] for e in G.edges()])
    norm    = plt.Normalize(weights.min(), weights.max())
    cmap    = plt.cm.plasma
    for (u, v), w in zip(G.edges(), weights):
        xs, ys, zs = zip(pos3d[u], pos3d[v])
        ax_graph.plot(xs, ys, zs,
                      color=cmap(norm(w)),
                      alpha=0.7,
                      lw=1.5)
    # Glow effect en nodos
    xs = [pos3d[i][0] for i in G]
    ys = [pos3d[i][1] for i in G]
    zs = [pos3d[i][2] for i in G]
    sizes_glow = [2000 * cent[i] for i in G]
    ax_graph.scatter(xs, ys, zs,
                     s=sizes_glow,
                     color='white',
                     alpha=0.2,
                     edgecolors='none')
    # Nodos coloreados por centralidad
    sizes = [150 * cent[i] for i in G]
    colors = [cent[i] for i in G]
    ax_graph.scatter(xs, ys, zs,
                     s=sizes,
                     c=colors,
                     cmap='viridis',
                     edgecolors='white',
                     lw=0.5)
    ax_graph.set_title(f"Expander {d}-regular (n={n})", color='lime', pad=12)
    ax_graph.axis('off')

# — 6) Crear animación —
ani = FuncAnimation(fig, update, frames=120, interval=100, repeat=True)

# Mostrar en notebook
HTML(ani.to_jshtml())

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

# — Parámetros —
n = 50             # número de nodos
d = 3              # grado regular
ram_limit = 2 * np.sqrt(d - 1)

# — 1) Crear grafo d‑regular aleatorio —
G = nx.random_regular_graph(d, n)

# — 2) Calcular autovalores —
A = nx.adjacency_matrix(G).toarray()
eigvals = np.sort(np.linalg.eigvals(A).real)

# — 3) Métricas —
cent = nx.eigenvector_centrality_numpy(G)
eb   = nx.edge_betweenness_centrality(G)

# — 4) Posiciones 3D sobre esfera —
theta = np.linspace(0, 2*np.pi, n, endpoint=False)
phi   = np.arccos(2*np.arange(n)/n - 1)
pos3d = {
    i: (
        np.cos(theta[i]) * np.sin(phi[i]),
        np.sin(theta[i]) * np.sin(phi[i]),
        np.cos(phi[i])
    )
    for i in range(n)
}

# — 5) Preparar figura y ejes —
plt.style.use('dark_background')
fig = plt.figure(figsize=(12, 6))
ax_graph    = fig.add_subplot(121, projection='3d')
ax_spectrum = fig.add_subplot(122)

# Precomputar semicírculo de Wigner
sigma = np.sqrt(d - 1)
x_sc   = np.linspace(-2*sigma, 2*sigma, 400)
rho_sc = (1/(2*np.pi*sigma**2)) * np.sqrt(np.maximum(4*sigma**2 - x_sc**2, 0))

def draw_spectrum():
    ax_spectrum.clear()
    ax_spectrum.set_facecolor('#1b2309')
    # Histograma de densidad
    ax_spectrum.hist(
        eigvals, bins=30, density=True,
        color='lightgray', edgecolor='white', alpha=0.6
    )
    # Semicírculo de Wigner
    ax_spectrum.fill_between(x_sc, rho_sc, color='cyan', alpha=0.3)
    ax_spectrum.plot(x_sc, rho_sc, color='cyan', lw=2)
    # Cotas Ramanujan
    for v in (+ram_limit, -ram_limit):
        ax_spectrum.axvline(v, color='blue', ls='--', lw=1.5)
    # Resaltar λ2 y λ_{n-1}
    for val in (eigvals[1], eigvals[-2]):
        c = 'green' if abs(val) <= ram_limit else 'red'
        ax_spectrum.axvline(val, color=c, lw=2)
        ax_spectrum.text(val, ax_spectrum.get_ylim()[1]*0.9,
                         f"{val:.2f}", color=c,
                         ha='center', va='bottom', fontsize=8)
    # Etiquetas y grid suave
    ax_spectrum.set_title("Distribución de autovalores", color='lime', pad=12)
    ax_spectrum.set_xlabel("Valor propio", color='white')
    ax_spectrum.set_ylabel("Densidad", color='white')
    ax_spectrum.tick_params(colors='white')
    ax_spectrum.yaxis.grid(True, color='white', alpha=0.1, ls='--')

# Dibujar espectro una sola vez
draw_spectrum()

# Barra de color para centralidad (solo una vez)
cax = fig.add_axes([0.15, 0.08, 0.3, 0.02])
cax.imshow(np.linspace(0,1,256)[None, :], cmap='viridis', aspect='auto')
cax.set_xticks([0, 255]); cax.set_xticklabels(['baja', 'alta'], color='white')
cax.set_yticks([]); cax.set_title("Eigenvector Centrality", color='white', pad=2)

def update(frame):
    ax_graph.clear()
    ax_graph.set_facecolor('#1b2309')
    try: ax_graph.set_proj_type('ortho')
    except: pass
    ax_graph.dist = 7
    ax_graph.view_init(elev=20, azim=(frame * 4) % 360)

    # Aristas con gradiente
    weights = np.array([eb[e] for e in G.edges()])
    norm    = plt.Normalize(weights.min(), weights.max())
    cmap    = plt.cm.plasma
    for (u, v), w in zip(G.edges(), weights):
        xs, ys, zs = zip(pos3d[u], pos3d[v])
        ax_graph.plot(xs, ys, zs, color=cmap(norm(w)), alpha=0.7, lw=1.5)

    # Glow nodes
    xs = [pos3d[i][0] for i in G]; ys = [pos3d[i][1] for i in G]; zs = [pos3d[i][2] for i in G]
    ax_graph.scatter(xs, ys, zs, s=[2000*cent[i] for i in G], color='white', alpha=0.2, edgecolors='none')

    # Colored nodes
    ax_graph.scatter(xs, ys, zs, s=[150*cent[i] for i in G], c=[cent[i] for i in G],
                     cmap='viridis', edgecolors='white', lw=0.5)
    ax_graph.set_title(f"Expander {d}-regular (n={n})", color='lime', pad=12)
    ax_graph.axis('off')

# — 6) Crear animación —
ani = FuncAnimation(fig, update, frames=120, interval=100, repeat=True)

# — 7) Guardar como MP4 y GIF —
# Requiere ffmpeg y pillow instalados en Colab
ani.save('expander.mp4', writer='ffmpeg', dpi=150, fps=10)
ani.save('expander.gif', writer='pillow', dpi=80, fps=10)

# — 8) Mostrar en notebook —
HTML(ani.to_jshtml())

!pip install bokeh
from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool

# Esto carga los recursos de Bokeh en la celda
output_notebook()

# Tu código…
años = [1984, 1988, 2008, 2013, 2020, 2025]
eventos = [
    "Dodziuk: unifica expansiones",
    "Lubotzky–Phillips–Sarnak: Ramanujan",
    "Estudio preliminar de grafos aleatorios",
    "Sarnak invita a Yau",
    "Yau–Huang–McKenzie: universalidad",
    "Quanta: bet settled"
]

src = ColumnDataSource(dict(x=años, y=[1]*len(años), desc=eventos))
p = figure(x_range=(1980, 2030), y_range=(0,2), height=200,
           tools="hover", toolbar_location=None)
p.segment(x0=años, y0=1.2, x1=años, y1=1.8, color="white")
p.scatter('x','y', size=12, source=src, color="cyan", marker="circle")
p.add_tools(HoverTool(tooltips=[("Año","@x"),("Evento","@desc")]))
p.yaxis.visible = False
p.xaxis.axis_label = "Año"
p.background_fill_color="#0f1e2e"
p.xgrid.grid_line_color="white"

show(p)

from matplotlib.projections import PolarAxes

# Calculamos histograma y densidad para cada bin
counts, bins = np.histogram(eigvals, bins=30, density=True)
angles = np.linspace(0, 2*np.pi, len(counts), endpoint=False)
width = 2*np.pi/len(counts)

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='polar')
ax.set_facecolor('#1b2309')

# Barras radiales
bars = ax.bar(angles, counts, width=width, bottom=0.0,
              color=plt.cm.cividis(counts/counts.max()), alpha=0.8)

# Curva semicircular mapeada al semicírculo
theta_sc = np.linspace(0, np.pi, len(x_sc))
rho_norm = rho_sc / rho_sc.max() * counts.max()
ax.plot(theta_sc, rho_norm, color='cyan', lw=2, label='Semicírculo Wigner')

ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_title("Espectro radial de autovalores", color='white', pad=20)
ax.legend(loc='lower right', facecolor='#1b2309', framealpha=0.5)
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx

# Parámetros
n, d = 50, 3
G = nx.random_regular_graph(d, n)
A = nx.to_numpy_array(G)
eigvals = np.sort(np.linalg.eigvals(A).real)

# Semicírculo de Wigner
sigma = np.sqrt(d - 1)
x_sc = np.linspace(-2*sigma, 2*sigma, 400)
rho_sc = (1/(2*np.pi*sigma**2)) * np.sqrt(np.maximum(4*sigma**2 - x_sc**2, 0))

# Histograma
counts, bins = np.histogram(eigvals, bins=30, density=True)
angles = np.linspace(0, 2*np.pi, len(counts), endpoint=False)
width = 2*np.pi / len(counts)

# Prepara figura polar
fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='polar')
ax.set_facecolor('#1b2309')

# Barras radiales iniciales
bars = ax.bar(
    angles, counts, width=width, bottom=0.0,
    color=plt.cm.cividis(counts/counts.max()), alpha=0.8
)

# Curva semicircular normalizada
theta_sc = np.linspace(0, np.pi, len(x_sc))
rho_norm = rho_sc / rho_sc.max() * counts.max()
line, = ax.plot(theta_sc, rho_norm, color='cyan', lw=2, label='Semicírculo Wigner')

# Ajustes estéticos
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_title("Espectro radial de autovalores (animado)", color='white', pad=20)
ax.legend(loc='lower right', facecolor='#1b2309', framealpha=0.5)

# Función de actualización: rota el offset angular
def update(frame):
    offset = frame * 2*np.pi / 60  # 60 fotogramas = 1 vuelta completa
    ax.set_theta_offset(offset)
    # Debemos devolver una lista de artistas
    return list(bars) + [line]

# Crear animación (sin mostrar inline)
ani = FuncAnimation(fig, update, frames=60, interval=100, blit=True)

# Guardar MP4 y GIF
ani.save('espectro_radial.mp4', writer='ffmpeg', dpi=150, fps=10)
ani.save('espectro_radial.gif', writer='pillow', dpi=80, fps=10)

print("He guardado 'espectro_radial.mp4' y 'espectro_radial.gif' en tu directorio de trabajo.")

import plotly.graph_objects as go
import networkx as nx

# Generamos el grafo (asegúrate de tener G definido)
n, d = 50, 3
G = nx.random_regular_graph(d, n)

# Nodo fuente y dos niveles de vecinos
source = 0
lvl1 = list(G.neighbors(source))
lvl2 = set(sum([list(G.neighbors(u)) for u in lvl1], [])) - {source} - set(lvl1)

# Construimos las listas de labels
nodes = [f"Src {source}"] + [f"L1 {u}" for u in lvl1] + [f"L2 {v}" for v in lvl2]
idx = {name: i for i, name in enumerate(nodes)}

# Ahora las tres listas para Sankey
sources, targets, values = [], [], []

# Primer nivel: flujo 1 desde el source
for u in lvl1:
    sources.append(idx[f"Src {source}"])
    targets.append(idx[f"L1 {u}"])
    values.append(1)

# Segundo nivel: flujo 0.5 de cada L1 a L2
for u in lvl1:
    for v in G.neighbors(u):
        if v != source and v not in lvl1:
            sources.append(idx[f"L1 {u}"])
            targets.append(idx[f"L2 {v}"])
            values.append(0.5)

# Creamos el diagrama Sankey
fig = go.Figure(go.Sankey(
    node = dict(
        label = nodes,
        color = "cyan",
        pad=15, thickness=15
    ),
    link = dict(
        source = sources,
        target = targets,
        value  = values,
        color  = "lightblue"
    )
))

fig.update_layout(
    title_text="Flujo de datos: Expander 3‑regular",
    font_color="white",
    paper_bgcolor="#0f1e2e",
    plot_bgcolor="#0f1e2e"
)

fig.show()

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx
from IPython.display import HTML

# Construir grafo y niveles
n, d = 50, 3
G = nx.random_regular_graph(d, n)
source = 0
lvl1 = list(G.neighbors(source))
lvl2 = sorted(set(sum([list(G.neighbors(u)) for u in lvl1], [])) - {source} - set(lvl1))

# Creamos el grafo dirigido
DG = nx.DiGraph()
DG.add_node(source)
DG.add_nodes_from(lvl1)
DG.add_nodes_from(lvl2)
edges = [(source, u) for u in lvl1] + [
    (u, v)
    for u in lvl1
    for v in sorted(G.neighbors(u))
    if v != source and v in lvl2
]

# Posiciones
pos = {source: (0, 0)}
for i, u in enumerate(lvl1):
    pos[u] = (1, (len(lvl1)-1)/2 - i)
for j, v in enumerate(lvl2):
    pos[v] = (2, (len(lvl2)-1)/2 - j)

# Figura con fondo oscuro
fig, ax = plt.subplots(figsize=(8, 4), facecolor='#0f1e2e')
ax.set_axis_off()

def update(frame):
    ax.clear()
    ax.set_facecolor('#0f1e2e')
    ax.set_title("Flujo dinámico: Expander 3‑regular", color='white')
    nx.draw_networkx_nodes(DG, pos,
        node_size=500, node_color='cyan', ax=ax)
    nx.draw_networkx_labels(DG, pos,
        labels={n:str(n) for n in DG.nodes()},
        font_color='black', ax=ax)
    # Sólo dibujamos hasta el frame actual
    nx.draw_networkx_edges(DG, pos,
        edgelist=edges[:frame],
        edge_color='lightblue', width=3, ax=ax)

ani = FuncAnimation(
    fig, update,
    frames=len(edges)+1,
    interval=300,
    blit=False     # <<–– Desactivamos blit
)

# Guardar MP4 y GIF
ani.save('sankey_dynamic.mp4', writer='ffmpeg', dpi=150, fps=5)
ani.save('sankey_dynamic.gif', writer='pillow', dpi=80, fps=5)

print("Archivos listos: sankey_dynamic.mp4 y sankey_dynamic.gif")

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML, FileLink

# --- Parameters ---
n = 50             # number of nodes
d = 3              # regular degree
ram_limit = 2 * np.sqrt(d - 1)

# 1) Create a random d‑regular graph
G = nx.random_regular_graph(d, n)

# 2) Compute eigenvalues
A = nx.adjacency_matrix(G).toarray()
eigvals = np.sort(np.linalg.eigvals(A).real)

# 3) Compute centrality metrics
cent = nx.eigenvector_centrality_numpy(G)
eb   = nx.edge_betweenness_centrality(G)

# 4) 3D positions projected on a sphere
theta = np.linspace(0, 2*np.pi, n, endpoint=False)
phi   = np.arccos(2*np.arange(n)/n - 1)
pos3d = {
    i: (
        np.cos(theta[i]) * np.sin(phi[i]),
        np.sin(theta[i]) * np.sin(phi[i]),
        np.cos(phi[i])
    )
    for i in range(n)
}

# 5) Prepare figure and axes
plt.style.use('dark_background')
fig = plt.figure(figsize=(12, 6))
ax_graph    = fig.add_subplot(121, projection='3d')
ax_spectrum = fig.add_subplot(122)

# Precompute Wigner semicircle distribution
sigma = np.sqrt(d - 1)
x_sc   = np.linspace(-2*sigma, 2*sigma, 400)
rho_sc = (1/(2*np.pi*sigma**2)) * np.sqrt(np.maximum(4*sigma**2 - x_sc**2, 0))

def draw_spectrum():
    ax_spectrum.clear()
    ax_spectrum.set_facecolor('#1b2309')
    # Density histogram
    ax_spectrum.hist(
        eigvals, bins=30, density=True,
        color='lightgray', edgecolor='white', alpha=0.6
    )
    # Wigner semicircle overlay
    ax_spectrum.fill_between(x_sc, rho_sc, color='cyan', alpha=0.3)
    ax_spectrum.plot(x_sc, rho_sc, color='cyan', lw=2)
    # Ramanujan bounds
    for v in (+ram_limit, -ram_limit):
        ax_spectrum.axvline(v, color='blue', ls='--', lw=1.5)
    # Highlight second and second-to-last eigenvalues
    for val in (eigvals[1], eigvals[-2]):
        c = 'green' if abs(val) <= ram_limit else 'red'
        ax_spectrum.axvline(val, color=c, lw=2)
        ax_spectrum.text(val, ax_spectrum.get_ylim()[1]*0.9,
                         f"{val:.2f}", color=c,
                         ha='center', va='bottom', fontsize=8)
    # Labels and grid
    ax_spectrum.set_title("Eigenvalue Distribution", color='lime', pad=12)
    ax_spectrum.set_xlabel("Eigenvalue", color='white')
    ax_spectrum.set_ylabel("Density", color='white')
    ax_spectrum.tick_params(colors='white')
    ax_spectrum.yaxis.grid(True, color='white', alpha=0.1, ls='--')

# Draw the static spectrum once
draw_spectrum()

# Color bar for eigenvector centrality
cax = fig.add_axes([0.15, 0.08, 0.3, 0.02])
cax.imshow(np.linspace(0,1,256)[None, :], cmap='viridis', aspect='auto')
cax.set_xticks([0, 255]); cax.set_xticklabels(['low', 'high'], color='white')
cax.set_yticks([]); cax.set_title("Eigenvector Centrality", color='white', pad=2)

def update(frame):
    ax_graph.clear()
    ax_graph.set_facecolor('#1b2309')
    try: ax_graph.set_proj_type('ortho')
    except: pass
    ax_graph.dist = 7
    ax_graph.view_init(elev=20, azim=(frame * 4) % 360)

    # Draw edges with gradient by betweenness
    weights = np.array([eb[e] for e in G.edges()])
    norm    = plt.Normalize(weights.min(), weights.max())
    cmap    = plt.cm.plasma
    for (u, v), w in zip(G.edges(), weights):
        xs, ys, zs = zip(pos3d[u], pos3d[v])
        ax_graph.plot(xs, ys, zs, color=cmap(norm(w)), alpha=0.7, lw=1.5)

    # Draw node glow by centrality
    xs = [pos3d[i][0] for i in G]; ys = [pos3d[i][1] for i in G]; zs = [pos3d[i][2] for i in G]
    ax_graph.scatter(xs, ys, zs, s=[2000*cent[i] for i in G], color='white', alpha=0.2, edgecolors='none')

    # Draw colored nodes by centrality
    ax_graph.scatter(xs, ys, zs, s=[150*cent[i] for i in G], c=[cent[i] for i in G],
                     cmap='viridis', edgecolors='white', lw=0.5)
    ax_graph.set_title(f"3‑Regular Expander (n={n})", color='lime', pad=12)
    ax_graph.axis('off')

# 6) Create animation
ani = FuncAnimation(fig, update, frames=120, interval=100, repeat=True)

# 7) Save as MP4 and GIF
ani.save('expander.mp4', writer='ffmpeg', dpi=150, fps=10)
ani.save('expander.gif', writer='pillow', dpi=80, fps=10)

# 8) Display in notebook and provide download links
html = HTML(ani.to_jshtml())
links = HTML(
    "<a href='expander.mp4' download>Download expander.mp4</a><br>" +
    "<a href='expander.gif' download>Download expander.gif</a>"
)

display(html, links)

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML

id_to_title = {
    1: "Big Data and Graphs",
    2: "Expander Image",
    3: "Expander Paradox",
    4: "Eigenvalues and λ₂",
    5: "Ramanujan & Wigner",
    6: "Importance in Big Data",
    7: "Technical Glossary",
    8: "Bibliography",
    9: "Full Epilogue"
}

# Define the edges of the DAG
edges = [
    (1, 2), (2, 3), (3, 4), (4, 5),
    (5, 6), (6, 7), (6, 8), (7, 9), (8, 9)
]

# Build the directed graph
G = nx.DiGraph()
G.add_nodes_from(id_to_title.keys())
G.add_edges_from(edges)

# Layout for positioning
pos = nx.spring_layout(G, seed=42, k=1.2)

# Create the figure
fig, ax = plt.subplots(figsize=(12, 6), facecolor='#0f1e2e')
ax.set_axis_off()
plt.subplots_adjust(top=0.85, right=0.75)

def update(frame):
    ax.clear()
    ax.set_facecolor('#0f1e2e')

    # Determine current node for subtitle
    current = 1 if frame == 0 else edges[min(frame-1, len(edges)-1)][1]
    subtitle = id_to_title[current]
    ax.text(
        0.5, 0.92, subtitle,
        transform=fig.transFigure,
        ha='center', color='cyan', fontsize=14
    )

    # Draw all nodes in light grey
    nx.draw_networkx_nodes(
        G, pos,
        node_size=900, node_color='gray', alpha=0.3,
        edgecolors='white', linewidths=1, ax=ax
    )

    # Determine which nodes have been reached so far
    reached = {1}
    for i in range(max(frame, 1)):
        if i < len(edges):
            reached.add(edges[i][1])

    # Highlight reached nodes in cyan
    nx.draw_networkx_nodes(
        G, pos,
        nodelist=list(reached),
        node_size=900, node_color='cyan', alpha=0.9,
        edgecolors='white', linewidths=1, ax=ax
    )

    # Draw edges up to the current frame
    drawn_edges = edges[:max(frame, 0)]
    nx.draw_networkx_edges(
        G, pos,
        edgelist=drawn_edges,
        edge_color='lightblue', width=2.5, ax=ax,
        arrowsize=12, arrowstyle='-|>'
    )

    # Draw numeric labels at the center of each node
    nx.draw_networkx_labels(
        G, pos,
        labels={i: str(i) for i in G.nodes()},
        font_color='black', font_size=10, font_weight='bold',
        horizontalalignment='center', verticalalignment='center',
        ax=ax
    )

    return ax,

# Create the animation (frames = number of edges + 1)
ani = FuncAnimation(
    fig, update,
    frames=len(edges) + 1,
    interval=1000,  # 1 second per step
    blit=False
)

# Save as MP4 and GIF
ani.save('dag_titles_animation.mp4', writer='ffmpeg', dpi=150, fps=1)
ani.save('dag_titles_animation.gif', writer='pillow', dpi=80, fps=1)

# Display inline in a Jupyter notebook
HTML(ani.to_jshtml())

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx
from IPython.display import HTML

# Build a random 3‑regular graph and determine levels (same as before)
n, d = 50, 3
G = nx.random_regular_graph(d, n)
source = 0
level1 = list(G.neighbors(source))
level2 = sorted(
    set(sum([list(G.neighbors(u)) for u in level1], []))
    - {source}
    - set(level1)
)

# Create a directed graph with those levels
DG = nx.DiGraph()
DG.add_node(source)
DG.add_nodes_from(level1)
DG.add_nodes_from(level2)
edges = [(source, u) for u in level1] + [
    (u, v)
    for u in level1
    for v in sorted(G.neighbors(u))
    if v != source and v in level2
]

# Manually specify positions for a layered layout
pos = {source: (0, 0)}
for i, u in enumerate(level1):
    pos[u] = (1, (len(level1) - 1) / 2 - i)
for j, v in enumerate(level2):
    pos[v] = (2, (len(level2) - 1) / 2 - j)

# Create the figure with a dark background
fig, ax = plt.subplots(figsize=(8, 4), facecolor='#0f1e2e')
ax.set_axis_off()

def update(frame):
    ax.clear()
    ax.set_facecolor('#0f1e2e')
    ax.set_title("Dynamic Flow: 3‑Regular Expander", color='white')
    # Draw all nodes in cyan
    nx.draw_networkx_nodes(DG, pos, node_size=500, node_color='cyan', ax=ax)
    # Label nodes by their identifier
    nx.draw_networkx_labels(
        DG, pos,
        labels={node: str(node) for node in DG.nodes()},
        font_color='black', ax=ax
    )
    # Draw edges up to the current frame
    nx.draw_networkx_edges(
        DG, pos,
        edgelist=edges[:frame],
        edge_color='lightblue', width=3, ax=ax
    )

ani = FuncAnimation(
    fig, update,
    frames=len(edges) + 1,
    interval=300,
    blit=False  # blitting turned off for compatibility
)

# Save as MP4 and GIF
ani.save('sankey_dynamic.mp4', writer='ffmpeg', dpi=150, fps=5)
ani.save('sankey_dynamic.gif', writer='pillow', dpi=80, fps=5)

print("Files ready: sankey_dynamic.mp4 and sankey_dynamic.gif")

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx

# Parameters
n, d = 50, 3
G = nx.random_regular_graph(d, n)
A = nx.to_numpy_array(G)
eigvals = np.sort(np.linalg.eigvals(A).real)

# Wigner semicircle distribution
sigma = np.sqrt(d - 1)
x_sc = np.linspace(-2 * sigma, 2 * sigma, 400)
rho_sc = (1 / (2 * np.pi * sigma**2)) * np.sqrt(np.maximum(4 * sigma**2 - x_sc**2, 0))

# Histogram of eigenvalues
counts, bins = np.histogram(eigvals, bins=30, density=True)
angles = np.linspace(0, 2 * np.pi, len(counts), endpoint=False)
width = 2 * np.pi / len(counts)

# Prepare polar figure
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection='polar')
ax.set_facecolor('#1b2309')

# Initial radial bars
bars = ax.bar(
    angles, counts, width=width, bottom=0.0,
    color=plt.cm.cividis(counts / counts.max()), alpha=0.8
)

# Normalized semicircle curve
theta_sc = np.linspace(0, np.pi, len(x_sc))
rho_norm = rho_sc / rho_sc.max() * counts.max()
line, = ax.plot(theta_sc, rho_norm, color='cyan', lw=2, label='Wigner Semicircle')

# Aesthetic adjustments
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_title("Animated Radial Eigenvalue Spectrum", color='white', pad=20)
ax.legend(loc='lower right', facecolor='#1b2309', framealpha=0.5)

# Update function: rotate angular offset
def update(frame):
    offset = frame * 2 * np.pi / 60  # 60 frames = one full rotation
    ax.set_theta_offset(offset)
    # Return list of artists to redraw
    return list(bars) + [line]

# Create animation (not displayed inline)
ani = FuncAnimation(fig, update, frames=60, interval=100, blit=True)

# Save as MP4 and GIF
ani.save('radial_spectrum.mp4', writer='ffmpeg', dpi=150, fps=10)
ani.save('radial_spectrum.gif', writer='pillow', dpi=80, fps=10)

print("Saved 'radial_spectrum.mp4' and 'radial_spectrum.gif' to your working directory.")