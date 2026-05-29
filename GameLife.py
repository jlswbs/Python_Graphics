# Conway's Game of Life

import pygame
import numpy as np
import sys

WIDTH, HEIGHT = 320, 240
SCALE = 2
FPS = 60

ALIVE = 1
DEAD = 0

def generate_initial_grid():
    return (np.random.rand(HEIGHT, WIDTH) > 0.75).astype(np.uint8)

def count_neighbors(grid):
    neighbors = sum(
        np.roll(np.roll(grid, dy, axis=0), dx, axis=1)
        for dy in (-1, 0, 1)
        for dx in (-1, 0, 1)
        if not (dx == 0 and dy == 0)
    )
    return neighbors

grid = generate_initial_grid()

pygame.init()

screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
pygame.display.set_caption("Game of Life")

clock = pygame.time.Clock()

running = True
paused = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

            elif event.key == pygame.K_r:
                grid = generate_initial_grid()

    if not paused:
        neighbors = count_neighbors(grid)

        birth = (neighbors == 3) & (grid == DEAD)
        survive = ((neighbors == 2) | (neighbors == 3)) & (grid == ALIVE)

        grid = np.where(birth | survive, ALIVE, DEAD).astype(np.uint8)

    view_grid = grid * 255

    surface_array = np.stack(
        [view_grid, view_grid, view_grid],
        axis=-1
    )

    surface_array = np.repeat(
        np.repeat(surface_array, SCALE, axis=0),
        SCALE,
        axis=1
    )

    surface = pygame.surfarray.make_surface(
        np.transpose(surface_array, (1, 0, 2))
    )

    screen.blit(surface, (0, 0))

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()