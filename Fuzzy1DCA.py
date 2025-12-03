# 1D fuzzy logic wolfram CA

import numpy as np
import pygame

WIDTH, HEIGHT = 320, 240
FPS = 60

SIGMA = 0.295
RULE_OFFSET = 0.2
RULE_SCALE  = 0.8

def gauss_eq(x, b, sigma=SIGMA):
    return np.exp(-((x - b)**2) / (2 * sigma**2))

def fuzzy_rule_output(L, C, R, rule_vals, sigma=SIGMA, eps=1e-8):
    patterns = np.array([
        [1,1,1],
        [1,1,0],
        [1,0,1],
        [1,0,0],
        [0,1,1],
        [0,1,0],
        [0,0,1],
        [0,0,0],
    ], dtype=int)

    S = np.stack([L, C, R], axis=-1)
    m = np.exp(-((S[..., None] - patterns.T[None, ...])**2) / (2 * sigma**2))
    d = np.prod(m, axis=1)
    rule = np.asarray(rule_vals)[None, :]
    num = np.sum(d * rule, axis=1)
    den = np.sum(d, axis=1) + eps
    y = num / den
    return np.clip(y, 0.0, 1.0)

binary_rule = np.array([0,0,0,1,1,1,1,0], dtype=float)
fuzzy_rule = RULE_OFFSET + RULE_SCALE * binary_rule

def step(state, sigma=SIGMA):
    L = np.roll(state, +1)
    C = state
    R = np.roll(state, -1)
    return fuzzy_rule_output(L, C, R, fuzzy_rule, sigma=sigma)

state = np.random.rand(WIDTH)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True
row = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    line = (state * 255).astype(np.uint8)
    for x in range(WIDTH):
        color = line[x]
        screen.set_at((x, row), (color, color, color))

    pygame.display.update()

    state = step(state, sigma=SIGMA)
    state = 0.95*state + 0.05*(np.roll(state,1)+np.roll(state,-1))/2

    row = (row + 1) % HEIGHT
    clock.tick(FPS)

pygame.quit()