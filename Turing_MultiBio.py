# Multi-scale Turing patterns slow biological growth

import numpy as np
import pygame
import math
import random

WIDTH  = 320
HEIGHT = 240
SCR = WIDTH * HEIGHT

BIO_GROWTH = 1.5
BIO_DAMP   = 0.1

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multi-scale Turing Patterns")
clock = pygame.time.Clock()

def randomf(a, b):
    return a + random.random() * (b - a)

grid          = np.zeros(SCR, dtype=np.float32)
blurBuffer    = np.zeros(SCR, dtype=np.float32)
bestVariation = np.zeros(SCR, dtype=np.float32)
bestLevel     = np.zeros(SCR, dtype=np.int32)
direction     = np.zeros(SCR, dtype=bool)
bioVelocity   = np.zeros(SCR, dtype=np.float32)

base        = randomf(1.5, 1.9)
stepScale  = randomf(0.02, 0.06)
stepOffset = randomf(0.01, 0.03)
blurFactor = randomf(0.7, 0.9)

levels = int(math.log(max(WIDTH, HEIGHT)) / math.log(base)) - 1
blurlevels = int((levels + 1) * blurFactor)

radii = []
stepSizes = []

maxRadius = min(WIDTH, HEIGHT) // 3

for i in range(levels):
    r = int(base ** i)
    r = min(r, maxRadius)
    radii.append(r)
    stepSizes.append(math.log(r) * stepScale + stepOffset)

grid[:] = np.random.uniform(-1.0, 1.0, SCR)
bioVelocity[:] = 0.0
bestVariation[:] = np.inf

surface = pygame.Surface((WIDTH, HEIGHT))

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    activator = grid.copy()

    for level in range(levels - 1):
        radius = radii[level]

        if level <= blurlevels:
            for y in range(HEIGHT):
                for x in range(WIDTH):
                    t = y * WIDTH + x
                    if y == 0 and x == 0:
                        blurBuffer[t] = activator[t]
                    elif y == 0:
                        blurBuffer[t] = blurBuffer[t - 1] + activator[t]
                    elif x == 0:
                        blurBuffer[t] = blurBuffer[t - WIDTH] + activator[t]
                    else:
                        blurBuffer[t] = (
                            blurBuffer[t - 1]
                            + blurBuffer[t - WIDTH]
                            - blurBuffer[t - WIDTH - 1]
                            + activator[t]
                        )

        inhibitor = np.zeros_like(grid)

        for y in range(HEIGHT):
            for x in range(WIDTH):
                minx = max(0, x - radius)
                maxx = min(WIDTH - 1, x + radius)
                miny = max(0, y - radius)
                maxy = min(HEIGHT - 1, y + radius)

                area = (maxx - minx + 1) * (maxy - miny + 1)

                nw = miny * WIDTH + minx
                ne = miny * WIDTH + maxx
                sw = maxy * WIDTH + minx
                se = maxy * WIDTH + maxx

                t = y * WIDTH + x
                inhibitor[t] = (
                    blurBuffer[se]
                    - blurBuffer[sw]
                    - blurBuffer[ne]
                    + blurBuffer[nw]
                ) / area

        diff = np.abs(activator - inhibitor)

        if level == 0:
            bestVariation[:] = diff
            bestLevel[:] = level
            direction[:] = activator > inhibitor
        else:
            mask = diff < bestVariation
            bestVariation[mask] = diff[mask]
            bestLevel[mask] = level
            direction[mask] = activator[mask] > inhibitor[mask]

        activator = inhibitor

    for i in range(SCR):
        target = 1.0 if direction[i] else -1.0
        step = stepSizes[bestLevel[i]] * BIO_GROWTH
        force = step * target
        bioVelocity[i] = bioVelocity[i] * BIO_DAMP + force
        grid[i] += bioVelocity[i]

    smallest = grid.min()
    largest  = grid.max()
    rng = (largest - smallest) * 0.5 + 1e-6

    image = ((grid - smallest) / rng - 1.0)
    image = np.clip(128 + 127 * image, 0, 255).astype(np.uint8)

    frame = image.reshape((HEIGHT, WIDTH))

    rgb = np.repeat(frame[:, :, None], 3, axis=2)
    rgb = np.transpose(rgb, (1, 0, 2))

    pygame.surfarray.blit_array(surface, rgb)
    screen.blit(surface, (0, 0))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()