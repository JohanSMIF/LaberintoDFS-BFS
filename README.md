# Laberinto DFS/BFS 🧩

App en Streamlit donde el usuario dibuja su propio laberinto y compara cómo lo resuelven
los algoritmos **BFS** (búsqueda en anchura) y **DFS** (búsqueda en profundidad).

## Cómo funciona

1. Elige el tamaño de la grilla en la barra lateral.
2. En "Modo de edición" elige qué vas a colocar al hacer clic en una celda:
   - **Poner muro**: bloquea el paso.
   - **Poner inicio 🟩**: define el punto de partida.
   - **Poner meta 🟥**: define el objetivo.
   - **Borrar**: limpia una celda.
3. Elige el algoritmo (BFS o DFS) en el selector.
4. Presiona **▶️ Resolver**. Se muestra el camino encontrado (🟨), junto con:
   - Cuántas celdas exploró el algoritmo.
   - La longitud del camino resultante.
   - Si existe o no un camino posible.

## Ejecutar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

Se abrirá en `http://localhost:8501`.

## Desplegar (opcional, para compartir un link)

1. Sube esta carpeta a un repositorio de GitHub.
2. Entra a [share.streamlit.io](https://share.streamlit.io) con tu cuenta de GitHub.
3. Selecciona el repo y el archivo `app.py` como punto de entrada.
4. Streamlit Community Cloud te da un link público en minutos.

## Notas técnicas

- BFS garantiza el camino **más corto** (en número de pasos) porque explora nivel por nivel.
- DFS **no garantiza** el camino más corto: puede encontrar uno más largo, aunque
  generalmente explora menos celdas antes de terminar si tiene "suerte" con la dirección.
- Ambos usan una cola/pila propia (deque y lista) implementadas desde cero, sin librerías
  externas de grafos, para que el código sea fácil de explicar en la sustentación.
