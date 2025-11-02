# Greenberg-Hastings cellular automaton

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap

# --- Parametry experimentu ---
WIDTH = 640
HEIGHT = 480
p_init = 0.1
n_states = 4
threshold = 2

# --- Inicializace gridu ---
grid = np.zeros((HEIGHT, WIDTH), dtype=np.int8)
grid[np.random.random((HEIGHT, WIDTH)) < p_init] = 1

cmap = ListedColormap(['black', 'white', 'red', 'orange', 'yellow'])
fig, ax = plt.subplots(figsize=(WIDTH/100, HEIGHT/100), dpi=100)
ax.set_axis_off()
im = ax.imshow(grid, cmap=cmap, interpolation='nearest', vmin=0, vmax=n_states-1)

# --- Funkce jednoho kroku ---
def step(grid):
    excited = (grid == 1).astype(np.int8)
    nsum = (
        np.roll(excited,  1, 0) + np.roll(excited, -1, 0) +
        np.roll(excited,  1, 1) + np.roll(excited, -1, 1) +
        np.roll(np.roll(excited,  1, 0),  1, 1) +
        np.roll(np.roll(excited,  1, 0), -1, 1) +
        np.roll(np.roll(excited, -1, 0),  1, 1) +
        np.roll(np.roll(excited, -1, 0), -1, 1)
    )
    new = np.copy(grid)
    # klidové buňky se vznící pokud mají dost excited sousedů
    new[(grid==0) & (nsum >= threshold)] = 1
    # buňky excitované a refrakterní postupují do dalšího stavu
    new[(grid>0)] += 1
    new[new >= n_states] = 0
    return new

def update(frame):
    global grid
    grid = step(grid)
    im.set_data(grid)
    return (im,)

ani = animation.FuncAnimation(fig, update, frames=1000, interval=30, blit=True)
plt.show()
