import pygame
import numpy as np
import os
import random

# Inicializace Pygame
pygame.init()

# Nastavení okna
width, height = 800, 600
cell_size = 8
rows, cols = height // cell_size, width // cell_size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("5-stavový celulární automat s náhodnými barvami")

# Funkce pro generování náhodných barev
def generate_random_colors(num_colors):
    colors = {}
    for i in range(num_colors):
        # Generování náhodné RGB barvy
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        colors[i] = (r, g, b)
    return colors

# Inicializace barev pro 5 stavů
num_states = 5
colors = generate_random_colors(num_states)

# Inicializace mřížky (náhodné stavy 0-4)
grid = np.random.randint(0, num_states, size=(rows, cols))

# Funkce pro výpočet sousedů
def count_neighbors(grid, x, y, state):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nx, ny = (x + i) % rows, (y + j) % cols  # Periodické okraje
            if grid[nx, ny] == state:
                count += 1
    return count

# Pravidla automatu pro kontinuální změnu (5 stavů)
def update_grid(grid):
    new_grid = grid.copy()
    for i in range(rows):
        for j in range(cols):
            current_state = grid[i, j]
            neighbors = [count_neighbors(grid, i, j, s) for s in range(num_states)]
            # Cyklická pravidla: stav X se mění na X+1, pokud má dost sousedů stavu X+1
            # Pokud má málo sousedů stejného stavu, vrací se na X-1
            next_state = (current_state + 1) % num_states  # Další stav v cyklu
            prev_state = (current_state - 1) % num_states  # Předchozí stav
            if neighbors[next_state] >= 3:  # Přechod na další stav
                new_grid[i, j] = next_state
            elif neighbors[current_state] < 2:  # Návrat na předchozí stav
                new_grid[i, j] = prev_state
    return new_grid

# Hlavní smyčka
running = True
paused = False
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Mezerník pro pauzu/obnovení
                paused = not paused
            elif event.key == pygame.K_r:  # R pro reset mřížky a nové barvy
                grid = np.random.randint(0, num_states, size=(rows, cols))
                colors = generate_random_colors(num_states)  # Nové náhodné barvy
                frame_count = 0  # Reset počitadla snímků

    if not paused:
        # Aktualizace mřížky (rekurzivní předávání stavů)
        grid = update_grid(grid)

        # Vykreslení mřížky
        screen.fill((255, 255, 255))  # Bílé pozadí
        for i in range(rows):
            for j in range(cols):
                pygame.draw.rect(screen, colors[grid[i, j]],
                                (j * cell_size, i * cell_size, cell_size, cell_size))

        pygame.display.flip()
        clock.tick(10)  # Rychlost simulace (10 FPS)

pygame.quit()