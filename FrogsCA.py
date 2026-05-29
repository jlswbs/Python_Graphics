# Frogs Cellular Automaton

import pygame
import numpy as np
import sys

WIDTH, HEIGHT = 320, 240
SCALE = 2
FPS = 60

DEAD = 0
ALIVE = 1
DECAY = 2

def generate_initial_grid():
    grid = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
    random_cells = np.random.rand(HEIGHT, WIDTH)
    grid[random_cells > 0.93] = ALIVE
    return grid

def count_neighbors(grid, state):
    target = (grid == state).astype(np.uint8)
    neighbors = sum(
        np.roll(np.roll(target, dy, axis=0), dx, axis=1)
        for dy in (-1, 0, 1)
        for dx in (-1, 0, 1)
        if not (dx == 0 and dy == 0)
    )
    return neighbors

grid = generate_initial_grid()

pygame.init()
screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
pygame.display.set_caption("Frogs Cellular Automaton")
clock = pygame.time.Clock()

running = True
paused = False
generation = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                grid = generate_initial_grid()
                generation = 0

    if not paused:
        alive_neighbors = count_neighbors(grid, ALIVE)
        
        new_grid = np.zeros_like(grid)
        
        birth = (grid == DEAD) & ((alive_neighbors == 3) | (alive_neighbors == 4))
        new_grid[birth] = ALIVE
        
        survive = (grid == ALIVE) & ((alive_neighbors == 1) | (alive_neighbors == 2))
        new_grid[survive] = ALIVE
        
        dying = (grid == ALIVE) & ~survive
        new_grid[dying] = DECAY
        
        grid = new_grid
        generation += 1

    surface_array = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    surface_array[grid == ALIVE] = [0, 255, 100]
    surface_array[grid == DECAY] = [255, 140, 0]

    surface_array = np.repeat(np.repeat(surface_array, SCALE, axis=0), SCALE, axis=1)
    
    surface = pygame.surfarray.make_surface(np.transpose(surface_array, (1, 0, 2)))
    screen.blit(surface, (0, 0))
    
    pygame.display.set_caption(f"Frogs CA - Gen: {generation} {'[PAUSED]' if paused else ''}")
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()