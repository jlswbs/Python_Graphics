# 1D fuzzy logic wolfram CA color

import numpy as np
import pygame
import colorsys

WIDTH, HEIGHT = 320, 240
FPS = 60

SIGMA = 0.26
RULE_OFFSET = 0.3
RULE_SCALE  = 0.7

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

binary_rule = np.array([0,1,1,1,1,1,1,0], dtype=float)
fuzzy_rule = RULE_OFFSET + RULE_SCALE * binary_rule

def step(state, sigma=SIGMA):
    L = np.roll(state, +1)
    C = state
    R = np.roll(state, -1)
    return fuzzy_rule_output(L, C, R, fuzzy_rule, sigma=sigma)

def value_to_rgb(val):
    hue = val
    sat = 1.0
    val_bright = 1.0
    r,g,b = colorsys.hsv_to_rgb(hue, sat, val_bright)
    return int(r*255), int(g*255), int(b*255)

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

    for x in range(WIDTH):
        color = value_to_rgb(state[x])
        screen.set_at((x, row), color)

    pygame.display.update()

    state = step(state, sigma=SIGMA)
    state = 0.95*state + 0.05*(np.roll(state,1)+np.roll(state,-1))/2

    row = (row + 1) % HEIGHT
    clock.tick(FPS)

pygame.quit()