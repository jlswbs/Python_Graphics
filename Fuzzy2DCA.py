# 2D fuzzy logic wolfram CA

import numpy as np
import pygame

WIDTH, HEIGHT = 320, 240
FPS = 60

SIGMA = 0.18
RULE_OFFSET = 0.1
RULE_SCALE  = 0.9

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
        frame = (state * 255).astype(np.uint8)
        rgb = np.dstack([frame, frame, frame])
        surf = pygame.surfarray.make_surface(rgb.swapaxes(0,1))
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