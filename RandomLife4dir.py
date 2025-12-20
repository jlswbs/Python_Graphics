# 2D random Life 4 directions CA

import pygame
import random
import numpy as np

WIDTH = 160
HEIGHT = 120

ALIVE = 3
DEATH_1 = 2
DEATH_2 = 1
DEAD = 0

pygame.init()
CELL_SIZE = 2
screen = pygame.display.set_mode((WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE))
clock = pygame.time.Clock()

current = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
next_grid = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
alive_counts = np.zeros((HEIGHT, WIDTH), dtype=np.uint16)
directions = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)

survival_rules = set()
birth_rules = set()

def wrap(v, m):
    if v < 0: return v + m
    if v >= m: return v - m
    return v

def rndrule():
    global survival_rules, birth_rules
    survival_rules = set(random.sample(range(0, 9), random.randint(1, 9)))
    birth_rules = set(random.sample(range(0, 9), random.randint(1, 9)))
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if random.randint(0, 99) < 20:
                current[y, x] = ALIVE
                directions[y, x] = random.choice([0, 2, 4, 6])
            else:
                current[y, x] = DEAD
                directions[y, x] = 0
    alive_counts.fill(0)

def step():
    global directions
    dx = [1, 0, -1, 0]
    dy = [0, -1, 0, 1]
    dir_map = {0:(1,0),2:(0,-1),4:(-1,0),6:(0,1)}
    next_grid.fill(DEAD)
    new_directions = np.zeros_like(directions)
    new_alive_counts = np.zeros_like(alive_counts)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            self_val = current[y, x]
            self_dir = directions[y, x]
            count = 0
            for ny in range(y-1, y+2):
                for nx in range(x-1, x+2):
                    if nx == x and ny == y:
                        continue
                    wx = wrap(nx, WIDTH)
                    wy = wrap(ny, HEIGHT)
                    if current[wy, wx] == ALIVE:
                        count += 1
            if self_val == ALIVE:
                if count in survival_rules:
                    next_grid[y, x] = ALIVE
                    new_directions[y, x] = self_dir
                    new_alive_counts[y, x] = min(alive_counts[y, x] + 1, 100)
                else:
                    next_grid[y, x] = DEATH_1
                    new_directions[y, x] = self_dir
            elif self_val == DEAD:
                if count in birth_rules:
                    next_grid[y, x] = ALIVE
                    dirs = []
                    for ny in range(y-1, y+2):
                        for nx in range(x-1, x+2):
                            wx = wrap(nx, WIDTH)
                            wy = wrap(ny, HEIGHT)
                            if current[wy, wx] == ALIVE:
                                dirs.append(directions[wy, wx])
                    if dirs:
                        new_directions[y, x] = random.choice([d for d in dirs if d in [0,2,4,6]] or [random.choice([0,2,4,6])])
                    else:
                        new_directions[y, x] = random.choice([0,2,4,6])
                else:
                    next_grid[y, x] = DEAD
                    new_directions[y, x] = 0
            else:
                next_grid[y, x] = self_val - 1
                new_directions[y, x] = self_dir
    moved_grid = np.zeros_like(next_grid)
    moved_dirs = np.zeros_like(new_directions)
    moved_alive = np.zeros_like(new_alive_counts)
    for y in range(HEIGHT):
        for x in range(WIDTH):
            val = next_grid[y, x]
            if val == DEAD:
                continue
            alive_age = new_alive_counts[y, x]
            if val == ALIVE:
                dir = new_directions[y, x]
                dxdy = dir_map.get(dir,(0,0))
                nx = wrap(x + dxdy[0], WIDTH)
                ny = wrap(y + dxdy[1], HEIGHT)
                moved_grid[ny, nx] = ALIVE
                moved_dirs[ny, nx] = dir
                moved_alive[ny, nx] = alive_age
                moved_grid[y, x] = DEATH_1
                moved_dirs[y, x] = dir
                moved_alive[y, x] = 0
            else:
                moved_grid[y, x] = val
                moved_dirs[y, x] = new_directions[y, x]
                moved_alive[y, x] = alive_age
    current[:, :] = moved_grid[:, :]
    directions[:, :] = moved_dirs[:, :]
    alive_counts[:, :] = moved_alive[:, :]

def draw():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            self_val = current[y, x]
            alive = alive_counts[y, x]
            if self_val == DEAD:
                color = (0, 0, 0)
            if self_val == ALIVE:
                if alive >= 50:
                    color = (255, 0, 0)
                elif alive >= 2:
                    color = (255, 255, 0)
                else:
                    color = (255, 255, 255)
            elif self_val == DEATH_1:
                color = (0, 0, 255)
            elif self_val == DEATH_2:
                color = (32, 32, 32)
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    rndrule()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    rndrule()
                elif event.key == pygame.K_ESCAPE:
                    running = False
        step()
        draw()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()