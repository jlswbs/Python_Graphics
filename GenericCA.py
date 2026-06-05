# Generic (multirules) Cellular Automaton

import pygame
import numpy as np
import sys
import random

WIDTH, HEIGHT = 320, 240
SCALE = 2
FPS = 60

colors = None


def random_rule():
    birth = sorted(random.sample([1, 2, 3, 4, 5], random.randint(1, 2)))
    survive = sorted(random.sample([1, 2, 3, 4, 5], random.randint(1, 3)))
    states = random.randint(3, 7)
    return birth, survive, states


def generate_random_colors(states):
    palette = np.zeros((states, 3), dtype=np.uint8)

    hue = random.randint(0, 360)
    palette[0] = [255, 255, 180] if random.random() < 0.3 else [255, 220, 100]

    for i in range(1, states):
        angle = (hue + i * (360 // states) + random.randint(-40, 40)) % 360

        if angle < 60:
            r, g, b = 255, random.randint(60, 140), random.randint(30, 80)
        elif angle < 120:
            r, g, b = random.randint(180, 255), 255, random.randint(30, 120)
        elif angle < 180:
            r, g, b = random.randint(20, 100), 255, random.randint(180, 255)
        elif angle < 240:
            r, g, b = random.randint(30, 100), random.randint(80, 180), 255
        elif angle < 300:
            r, g, b = random.randint(140, 255), random.randint(30, 120), 255
        else:
            r, g, b = 255, random.randint(20, 100), random.randint(100, 220)

        dark = max(0, 255 - i * random.randint(22, 38))
        r = int(r * dark / 255)
        g = int(g * dark / 255)
        b = int(b * dark / 255)

        if random.random() < 0.25:
            r, g, b = b, r, g

        palette[i] = [max(40, r), max(30, g), max(50, b)]

    return palette


def print_rule(birth, survive, states, mode_name):
    b_str = "".join(map(str, birth))
    s_str = "".join(map(str, survive))
    print(f"→ New Rule ({mode_name}): B{b_str}/S{s_str}/{states}")


def generate_initial_grid():
    grid = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
    grid[np.random.rand(HEIGHT, WIDTH) < 0.12] = 1
    return grid


def generate_center_grid():
    grid = np.zeros((HEIGHT, WIDTH), dtype=np.uint8)
    cy, cx = HEIGHT // 2, WIDTH // 2
    grid[cy - 1:cy + 2, cx - 1:cx + 2] = 1
    return grid


birth, survive, STATES = random_rule()
colors = generate_random_colors(STATES)
print_rule(birth, survive, STATES, "Random Seed")
grid = generate_initial_grid()

pygame.init()
screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
clock = pygame.time.Clock()

running = True
paused = False
generation = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

            elif event.key == pygame.K_r:
                birth, survive, STATES = random_rule()
                colors = generate_random_colors(STATES)
                print_rule(birth, survive, STATES, "Random Seed")
                grid = generate_initial_grid()
                generation = 0
                paused = False

            elif event.key == pygame.K_s:
                birth, survive, STATES = random_rule()
                colors = generate_random_colors(STATES)
                print_rule(birth, survive, STATES, "Central Seed")
                grid = generate_center_grid()
                generation = 0
                paused = False

    if not paused:
        neighbors = sum(
            np.roll(np.roll((grid == 1).astype(np.uint8), dy, axis=0), dx, axis=1)
            for dy in (-1, 0, 1)
            for dx in (-1, 0, 1)
            if not (dx == 0 and dy == 0)
        )

        new_grid = np.zeros_like(grid)

        birth_condition = np.isin(neighbors, birth)
        new_grid[(grid == 0) & birth_condition] = 1

        survive_condition = np.isin(neighbors, survive)
        new_grid[(grid == 1) & survive_condition] = 1

        dying = (grid == 1) & ~survive_condition
        new_grid[dying] = 2

        fading = (grid >= 2) & (grid < STATES - 1)
        new_grid[fading] = grid[fading] + 1

        grid = new_grid
        generation += 1

    surface_array = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    for i in range(1, STATES):
        surface_array[grid == i] = colors[i - 1]

    surface_array = np.repeat(
        np.repeat(surface_array, SCALE, axis=0),
        SCALE,
        axis=1
    )

    surface = pygame.surfarray.make_surface(
        np.transpose(surface_array, (1, 0, 2))
    )

    screen.blit(surface, (0, 0))

    pygame.display.set_caption(
        f"Generation: {generation} | SPACE=Pause | R=Random Seed | S=Central Seed"
    )

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()