import streamlit as st
from collections import deque
import time

st.set_page_config(page_title="Laberinto DFS/BFS", page_icon="🧩", layout="centered")


//Constantes de celdas

EMPTY, WALL, START, END, PATH, VISITED = 0, 1, 2, 3, 4, 5

CELL_STYLES = {
    EMPTY:   ("⬜", "#f0f2f6"),
    WALL:    ("⬛", "#2b2b2b"),
    START:   ("🟩", "#2ecc71"),
    END:     ("🟥", "#e74c3c"),
    PATH:    ("🟨", "#f1c40f"),
    VISITED: ("🟦", "#5dade2"),
}

DEFAULT_SIZE = 10



//Estado inicial

def nueva_grilla(size):
    return [[EMPTY for _ in range(size)] for _ in range(size)]


if "size" not in st.session_state:
    st.session_state.size = DEFAULT_SIZE
if "grid" not in st.session_state:
    st.session_state.grid = nueva_grilla(st.session_state.size)
if "start" not in st.session_state:
    st.session_state.start = None
if "end" not in st.session_state:
    st.session_state.end = None
if "result" not in st.session_state:
    st.session_state.result = None  # dict con path, visited_order, found, steps



//Lógica de algoritmos

def vecinos(pos, size):
    r, c = pos
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < size and 0 <= nc < size:
            yield (nr, nc)


def resolver_bfs(grid, start, end, size):
    q = deque([start])
    came_from = {start: None}
    visited_order = [start]

    while q:
        actual = q.popleft()
        if actual == end:
            break
        for vecino in vecinos(actual, size):
            r, c = vecino
            if grid[r][c] == WALL or vecino in came_from:
                continue
            came_from[vecino] = actual
            visited_order.append(vecino)
            q.append(vecino)

    return reconstruir(came_from, start, end, visited_order)


def resolver_dfs(grid, start, end, size):
    stack = [start]
    came_from = {start: None}
    visited_order = []
    visitado = {start}

    while stack:
        actual = stack.pop()
        visited_order.append(actual)
        if actual == end:
            break
        for vecino in vecinos(actual, size):
            r, c = vecino
            if grid[r][c] == WALL or vecino in visitado:
                continue
            visitado.add(vecino)
            came_from[vecino] = actual
            stack.append(vecino)

    return reconstruir(came_from, start, end, visited_order)


def reconstruir(came_from, start, end, visited_order):
    if end not in came_from:
        return {"found": False, "path": [], "visited_order": visited_order, "steps": len(visited_order)}

    path = []
    nodo = end
    while nodo is not None:
        path.append(nodo)
        nodo = came_from[nodo]
    path.reverse()
    return {"found": True, "path": path, "visited_order": visited_order, "steps": len(visited_order)}



//Interfaz

st.title("🧩 Laberinto: DFS vs BFS")
st.caption("Dibuja tu propio laberinto, elige el algoritmo y descubre si encuentra la salida.")

with st.sidebar:
    st.header("Controles")

    nuevo_size = st.slider("Tamaño de la grilla", 6, 16, st.session_state.size)
    if nuevo_size != st.session_state.size:
        st.session_state.size = nuevo_size
        st.session_state.grid = nueva_grilla(nuevo_size)
        st.session_state.start = None
        st.session_state.end = None
        st.session_state.result = None
        st.rerun()

    modo = st.radio(
        "Modo de edición",
        ["Poner muro", "Poner inicio 🟩", "Poner meta 🟥", "Borrar"],
        index=0,
    )

    algoritmo = st.selectbox("Algoritmo de búsqueda", ["BFS (anchura)", "DFS (profundidad)"])

    col_a, col_b = st.columns(2)
    with col_a:
        resolver_click = st.button("▶️ Resolver", use_container_width=True, type="primary")
    with col_b:
        limpiar_click = st.button("🧹 Limpiar todo", use_container_width=True)

    if limpiar_click:
        st.session_state.grid = nueva_grilla(st.session_state.size)
        st.session_state.start = None
        st.session_state.end = None
        st.session_state.result = None
        st.rerun()

    st.divider()
    st.markdown(
        """
        **Leyenda**
        - 🟩 Inicio &nbsp;&nbsp; 🟥 Meta
        - ⬛ Muro &nbsp;&nbsp; ⬜ Vacío
        - 🟨 Camino encontrado
        """
    )


//Manejo de clic en celda

def click_celda(r, c):
    grid = st.session_state.grid
    valor_actual = grid[r][c]

    if modo == "Poner muro":
        if valor_actual in (START, END):
            if valor_actual == START:
                st.session_state.start = None
            else:
                st.session_state.end = None
        grid[r][c] = WALL if valor_actual != WALL else EMPTY

    elif modo == "Poner inicio 🟩":
        if st.session_state.start is not None:
            sr, sc = st.session_state.start
            grid[sr][sc] = EMPTY
        grid[r][c] = START
        st.session_state.start = (r, c)

    elif modo == "Poner meta 🟥":
        if st.session_state.end is not None:
            er, ec = st.session_state.end
            grid[er][ec] = EMPTY
        grid[r][c] = END
        st.session_state.end = (r, c)

    elif modo == "Borrar":
        if valor_actual == START:
            st.session_state.start = None
        elif valor_actual == END:
            st.session_state.end = None
        grid[r][c] = EMPTY

    st.session_state.result = None  # invalidar resultado anterior



//Render de la grilla

size = st.session_state.size
grid = st.session_state.grid
result = st.session_state.result

display_grid = [row[:] for row in grid]
if result and result["found"]:
    for (r, c) in result["path"]:
        if display_grid[r][c] not in (START, END):
            display_grid[r][c] = PATH

for r in range(size):
    cols = st.columns(size, gap="small")
    for c in range(size):
        emoji, _ = CELL_STYLES[display_grid[r][c]]
        if cols[c].button(emoji, key=f"cell_{r}_{c}", use_container_width=True):
            click_celda(r, c)
            st.rerun()


//Resolver

if resolver_click:
    if st.session_state.start is None or st.session_state.end is None:
        st.error("Debes colocar un punto de inicio 🟩 y una meta 🟥 antes de resolver.")
    else:
        t0 = time.time()
        if algoritmo.startswith("BFS"):
            resultado = resolver_bfs(grid, st.session_state.start, st.session_state.end, size)
        else:
            resultado = resolver_dfs(grid, st.session_state.start, st.session_state.end, size)
        resultado["tiempo"] = time.time() - t0
        resultado["algoritmo"] = algoritmo
        st.session_state.result = resultado
        st.rerun()

//Mostrar resultados

if st.session_state.result:
    r = st.session_state.result
    st.divider()
    st.subheader("Resultado")

    c1, c2, c3 = st.columns(3)
    c1.metric("Algoritmo", r["algoritmo"].split(" ")[0])
    c2.metric("Celdas exploradas", r["steps"])
    c3.metric("Longitud del camino", len(r["path"]) if r["found"] else 0)

    if r["found"]:
        st.success(f"¡Camino encontrado! Tomó {r['tiempo']*1000:.2f} ms en calcularse.")
    else:
        st.warning("No existe un camino posible entre el inicio y la meta con los muros actuales.")
