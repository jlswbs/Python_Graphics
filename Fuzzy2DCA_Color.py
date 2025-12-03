# 2D fuzzy logic wolfram CA color

import numpy as np
import pygame
import colorsys

WIDTH, HEIGHT = 320, 240
FPS = 60

SIGMA = 0.221
RULE_OFFSET = 0.05
RULE_SCALE  = 0.95

def gauss_eq(x, b, sigma=SIGMA):
    return np.exp(-((x - b)**2) / (2 * sigma**2))

def fuzzy_life_step(state, sigma=SIGMA):
    neighbors = (
        np.roll(np.roll(state, 1, 0), 1, 1) +
        np.roll(np.roll(state, 1, 0), -1, 1) +
        np.roll(np.roll(state, -1, 0), 1, 1) +
        np.roll(np.roll(state, -1, 0), -1, 1) +
        np.roll(state, 1, 0) +
        np.roll(state, -1, 0) +
        np.roll(state, 1, 1) +
        np.roll(state, -1, 1)
    )

    birth_match = gauss_eq(neighbors/8.0, 3/8.0, sigma)
    surv_match2 = gauss_eq(neighbors/8.0, 2/8.0, sigma)
    surv_match3 = gauss_eq(neighbors/8.0, 3/8.0, sigma)
    survival = np.maximum(surv_match2, surv_match3)
    new_state = RULE_OFFSET + RULE_SCALE * np.clip(np.maximum(birth_match, survival * state), 0.0, 1.0)

    return new_state

def value_to_rgb(val):
    hue = val
    sat = 1.0
    val_bright = 1.0
    r,g,b = colorsys.hsv_to_rgb(hue, sat, val_bright)
    return int(r*255), int(g*255), int(b*255)

state = np.random.rand(HEIGHT, WIDTH)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True
frame_count = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if frame_count % 2 == 0:
        surf_array = np.zeros((WIDTH, HEIGHT, 3), dtype=np.uint8)
        for y in range(HEIGHT):
            for x in range(WIDTH):
                surf_array[x,y] = value_to_rgb(state[y,x])
        surf = pygame.surfarray.make_surface(surf_array)
        screen.blit(surf, (0,0))
        pygame.display.update()

    state = fuzzy_life_step(state, sigma=SIGMA)
    state = 0.97*state + 0.03*(
        np.roll(state,1,0)+np.roll(state,-1,0)+
        np.roll(state,1,1)+np.roll(state,-1,1)
    )/4

    frame_count += 1
    clock.tick(FPS)

pygame.quit()