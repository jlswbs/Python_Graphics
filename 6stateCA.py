import pygame
import numpy as np
import os
import random

pygame.init()

width, height = 800, 600
cell_size = 8
rows, cols = height // cell_size, width // cell_size
screen = pygame.display.set_mode((width, height))

def generate_random_colors(num_colors):
    colors = {}
    for i in range(num_colors):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        colors[i] = (r, g, b)
    return colors

num_states = 6
colors = generate_random_colors(num_states)

grid = np.random.randint(0, num_states, size=(rows, cols))

def count_neighbors(grid, x, y, state):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            nx, ny = (x + i) % rows, (y + j) % cols
            if grid[nx, ny] == state:
                count += 1
    return count

def update_grid(grid):
    new_grid = grid.copy()
    for i in range(rows):
        for j in range(cols):
            current_state = grid[i, j]
            neighbors = [count_neighbors(grid, i, j, s) for s in range(num_states)]
            next_state = (current_state + 1) % num_states
            prev_state = (current_state - 1) % num_states
            if neighbors[next_state] >= 3:
                new_grid[i, j] = next_state
            elif neighbors[current_state] < 2:
                new_grid[i, j] = prev_state
    return new_grid

running = True
paused = False
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:
                grid = np.random.randint(0, num_states, size=(rows, cols))
                colors = generate_random_colors(num_states)
                frame_count = 0

    if not paused:
        grid = update_grid(grid)
        screen.fill((255, 255, 255))
        for i in range(rows):
            for j in range(cols):
                pygame.draw.rect(screen, colors[grid[i, j]],
                                (j * cell_size, i * cell_size, cell_size, cell_size))
        pygame.display.flip()

pygame.quit()