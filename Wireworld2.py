# Wireworld cellular automata

import pygame
import numpy as np
import random

WIDTH = 480
HEIGHT = 270
PIXEL_SIZE = 2
FPS = 30

NUM_GATES = 6
NUM_SWITCHES = 6
NUM_OSCILLATORS = 4
NUM_DIODES = 8
NUM_ABSORBERS = 4
NUM_DELAYS = 6
CONNECT_LENGTH = 8
NUM_ELECTRONS = 1

grid = np.zeros((WIDTH, HEIGHT), dtype=np.uint8)
new_grid = np.zeros((WIDTH, HEIGHT), dtype=np.uint8)

pygame.init()
screen = pygame.display.set_mode((WIDTH * PIXEL_SIZE, HEIGHT * PIXEL_SIZE))
pygame.display.set_caption("Wireworld")
clock = pygame.time.Clock()

def place_or_gate(x, y):
    if x >= 3 and x < WIDTH - 3 and y >= 3 and y < HEIGHT - 3:
        grid[x][y] = 3
        grid[x-1][y-1] = 3
        grid[x+1][y-1] = 3
        grid[x][y+1] = 3
        grid[x][y+2] = 3

def place_and_gate(x, y):
    if x >= 3 and x < WIDTH - 3 and y >= 3 and y < HEIGHT - 3:
        grid[x][y] = 3
        grid[x-1][y-1] = 3
        grid[x+1][y-1] = 3
        grid[x][y+2] = 3
        grid[x][y+3] = 3

def place_xor_gate(x, y):
    if x >= 5 and x < WIDTH - 5 and y >= 5 and y < HEIGHT - 5:
        grid[x][y] = 3
        grid[x-1][y-1] = 3
        grid[x+1][y-1] = 3
        grid[x-2][y] = 3
        grid[x+2][y] = 3
        grid[x-3][y+1] = 3
        grid[x+3][y+1] = 3
        grid[x-2][y+2] = 3
        grid[x+2][y+2] = 3
        grid[x-1][y+3] = 3
        grid[x+1][y+3] = 3
        grid[x][y+4] = 3
        grid[x][y+5] = 3

def place_oscillator(x, y):
    if x >= 3 and x < WIDTH - 3 and y >= 3 and y < HEIGHT - 3:
        grid[x][y] = 3
        grid[x+1][y] = 3
        grid[x+2][y] = 3
        grid[x+2][y+1] = 3
        grid[x+1][y+1] = 3
        grid[x][y+1] = 3
        grid[x][y+2] = 3
        grid[x][y+3] = 3
        grid[x+1][y] = 1
        grid[x+1][y+1] = 2

def place_switch(x, y):
    if x >= 3 and x < WIDTH - 3 and y >= 3 and y < HEIGHT - 3:
        grid[x][y] = 3
        grid[x-1][y] = 3
        grid[x+1][y] = 3
        grid[x][y+1] = 3

def place_diode(x, y, dir):
    if x >= 2 and x < WIDTH - 2 and y >= 2 and y < HEIGHT - 2:
        grid[x][y] = 3
        dx = [1, -1, 0, 0]
        dy = [0, 0, 1, -1]
        for i in range(1, 3):
            nx = x + dx[dir] * i
            ny = y + dy[dir] * i
            if nx >= 0 and nx < WIDTH and ny >= 0 and ny < HEIGHT:
                grid[nx][ny] = 3

def place_absorber(x, y, dir):
    if x >= 3 and x < WIDTH - 3 and y >= 3 and y < HEIGHT - 3:
        grid[x][y] = 3
        dx = [1, -1, 0, 0]
        dy = [0, 0, 1, -1]
        for i in range(1, 5):
            nx = x + dx[dir] * i
            ny = y + dy[dir] * i
            if nx >= 0 and nx < WIDTH and ny >= 0 and ny < HEIGHT:
                grid[nx][ny] = 3
        if dir < 2:
            if y+1 < HEIGHT:
                grid[x][y+1] = 3
            if y-1 >= 0:
                grid[x][y-1] = 3
        else:
            if x+1 < WIDTH:
                grid[x+1][y] = 3
            if x-1 >= 0:
                grid[x-1][y] = 3

def place_delay(x, y, length=5):
    if x >= length+2 and x < WIDTH - length-2 and y >= length+2 and y < HEIGHT - length-2:
        for i in range(length):
            if x+i < WIDTH:
                grid[x+i][y] = 3
        for i in range(length):
            if y+i < HEIGHT:
                grid[x+length-1][y+i] = 3
        for i in range(length):
            if x+length-1-i >= 0:
                grid[x+length-1-i][y+length-1] = 3
        for i in range(length):
            if y+length-1-i >= 0:
                grid[x][y+length-1-i] = 3

def place_electron_sink(x, y):
    if x >= 3 and x < WIDTH - 3 and y >= 3 and y < HEIGHT - 3:
        grid[x][y] = 3
        grid[x-1][y] = 3
        grid[x+1][y] = 3
        for i in range(1, 4):
            if y+i < HEIGHT:
                grid[x-1][y+i] = 3
                grid[x+1][y+i] = 3

def connect_elements(x1, y1, x2, y2):
    if x1 == x2:
        start_y = min(y1, y2)
        end_y = max(y1, y2)
        for y in range(start_y, end_y + 1):
            if y >= 0 and y < HEIGHT:
                grid[x1][y] = 3
    elif y1 == y2:
        start_x = min(x1, x2)
        end_x = max(x1, x2)
        for x in range(start_x, end_x + 1):
            if x >= 0 and x < WIDTH:
                grid[x][y1] = 3
    else:
        mid_x = (x1 + x2) // 2
        for x in range(min(x1, mid_x), max(x1, mid_x) + 1):
            if x >= 0 and x < WIDTH:
                grid[x][y1] = 3
        for y in range(min(y1, y2), max(y1, y2) + 1):
            if y >= 0 and y < HEIGHT:
                grid[mid_x][y] = 3
        for x in range(min(mid_x, x2), max(mid_x, x2) + 1):
            if x >= 0 and x < WIDTH:
                grid[x][y2] = 3

def rndseed():
    grid.fill(0)
    positions = []
    connection_points = []

    for i in range(NUM_GATES):
        while True:
            x = 5 + random.randint(0, WIDTH - 11)
            y = 5 + random.randint(0, HEIGHT - 11)
            if grid[x][y] == 0:
                break
        gate_type = random.randint(0, 2)
        if gate_type == 0:
            place_or_gate(x, y)
            connection_points.append((x-1, y-1, "input"))
            connection_points.append((x+1, y-1, "input"))
            connection_points.append((x, y+2, "output"))
        elif gate_type == 1:
            place_and_gate(x, y)
            connection_points.append((x-1, y-1, "input"))
            connection_points.append((x+1, y-1, "input"))
            connection_points.append((x, y+3, "output"))
        else:
            place_xor_gate(x, y)
            connection_points.append((x-1, y-1, "input"))
            connection_points.append((x+1, y-1, "input"))
            connection_points.append((x, y+5, "output"))
        positions.append((x, y))

    for i in range(NUM_SWITCHES):
        while True:
            x = 3 + random.randint(0, WIDTH - 7)
            y = 3 + random.randint(0, HEIGHT - 7)
            if grid[x][y] == 0:
                break
        place_switch(x, y)
        connection_points.append((x, y+1, "input"))
        connection_points.append((x-1, y, "output"))
        connection_points.append((x+1, y, "output"))
        positions.append((x, y))

    for i in range(NUM_OSCILLATORS):
        while True:
            x = 5 + random.randint(0, WIDTH - 11)
            y = 5 + random.randint(0, HEIGHT - 11)
            if grid[x][y] == 0:
                break
        place_oscillator(x, y)
        connection_points.append((x, y+3, "output"))
        positions.append((x, y))

    for i in range(NUM_DELAYS):
        while True:
            x = 8 + random.randint(0, WIDTH - 17)
            y = 8 + random.randint(0, HEIGHT - 17)
            if grid[x][y] == 0:
                break
        length = random.randint(4, 7)
        place_delay(x, y, length)
        connection_points.append((x, y, "input"))
        connection_points.append((x, y, "output"))
        positions.append((x, y))

    for i in range(NUM_DIODES):
        while True:
            x = 3 + random.randint(0, WIDTH - 7)
            y = 3 + random.randint(0, HEIGHT - 7)
            if grid[x][y] == 0:
                break
        dir = random.randint(0, 3)
        place_diode(x, y, dir)
        positions.append((x, y))

    for i in range(NUM_ABSORBERS):
        while True:
            x = 4 + random.randint(0, WIDTH - 9)
            y = 4 + random.randint(0, HEIGHT - 9)
            if grid[x][y] == 0:
                break
        dir = random.randint(0, 3)
        place_absorber(x, y, dir)
        positions.append((x, y))

    for i in range(3):
        while True:
            x = 4 + random.randint(0, WIDTH - 9)
            y = 4 + random.randint(0, HEIGHT - 9)
            if grid[x][y] == 0:
                break
        place_electron_sink(x, y)
        positions.append((x, y))

    for i, (x, y, io_type) in enumerate(connection_points):
        if io_type == "input":
            while True:
                j = random.randint(0, len(positions) + len(connection_points) - 1)
                if j < len(positions):
                    x2, y2 = positions[j]
                    if (x2, y2) != (x, y) and grid[x2][y2] == 3:
                        connect_elements(x, y, x2, y2)
                        break
                else:
                    x2, y2, io2_type = connection_points[j % len(connection_points)]
                    if io2_type == "output" and (x2, y2) != (x, y) and grid[x2][y2] == 3:
                        connect_elements(x, y, x2, y2)
                        break
        elif io_type == "output":
            while True:
                j = random.randint(0, len(positions) + len(connection_points) - 1)
                if j < len(positions):
                    x2, y2 = positions[j]
                    if (x2, y2) != (x, y) and grid[x2][y2] == 3:
                        connect_elements(x, y, x2, y2)
                        break
                else:
                    x2, y2, io2_type = connection_points[j % len(connection_points)]
                    if io2_type == "input" and (x2, y2) != (x, y) and grid[x2][y2] == 3:
                        connect_elements(x, y, x2, y2)
                        break

    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):
            if random.randint(0, 99) < 5:
                connect_elements(positions[i][0], positions[i][1], positions[j][0], positions[j][1])

    for i in range(NUM_ELECTRONS):
        while True:
            x = random.randint(0, WIDTH - 1)
            y = random.randint(0, HEIGHT - 1)
            if grid[x][y] == 3:
                grid[x][y] = 1
                break

def count_neighbors(grid):
    count = np.zeros_like(grid)
    for di, dj in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
        shifted = np.roll(np.roll(grid == 1, di, axis=0), dj, axis=1)
        count += shifted
    count[0, :] = 0
    count[-1, :] = 0
    count[:, 0] = 0
    count[:, -1] = 0
    return count

def update_grid():
    new_grid[:] = grid[:]
    new_grid[grid == 1] = 2
    new_grid[grid == 2] = 3
    neighbors = count_neighbors(grid)
    new_grid[(grid == 3) & ((neighbors == 1) | (neighbors == 2))] = 1

    electron_count = np.sum(grid == 1) + np.sum(grid == 2)
    if electron_count > 60:
        mask = (grid == 1) | (grid == 2)
        positions = np.argwhere(mask)
        if len(positions) > 0:
            to_delete = random.sample(list(positions), min(max(1, len(positions) // 5), len(positions)))
            for x, y in to_delete:
                new_grid[x][y] = 3

    grid[:] = new_grid[:]

def render_grid():
    pixel_array = np.zeros((WIDTH, HEIGHT, 3), dtype=np.uint8)
    pixel_array[grid == 1] = (255, 255, 255)
    pixel_array[grid == 2] = (255, 0, 0)
    pixel_array[grid == 3] = (0, 0, 255)
    surface = pygame.surfarray.make_surface(pixel_array)
    scaled_surface = pygame.transform.scale(surface, (WIDTH * PIXEL_SIZE, HEIGHT * PIXEL_SIZE))
    screen.blit(scaled_surface, (0, 0))

random.seed()
rndseed()

running = True
paused = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            rndseed()
            paused = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_ESCAPE:
                running = False

    if not paused:
        update_grid()

    screen.fill((0, 0, 0))
    render_grid()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
