# Voronoi diagram simulation

import pygame
import random

WIDTH, HEIGHT = 320, 240
NUM_SITES = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

sites = []
for _ in range(NUM_SITES):
    x = random.randint(0, WIDTH-1)
    y = random.randint(0, HEIGHT-1)
    dx = random.choice([-1, 1])
    dy = random.choice([-1, 1])
    sites.append([x, y, dx, dy])

def nearest_site_index(x, y, sites):
    best_i = -1
    best_d2 = 10**9
    for i, (sx, sy, _, _) in enumerate(sites):
        dx = x - sx
        dy = y - sy
        d2 = dx*dx + dy*dy
        if d2 < best_d2:
            best_d2 = d2
            best_i = i
    return best_i

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for s in sites:
        s[0] += s[2]
        s[1] += s[3]
        if s[0] < 0 or s[0] >= WIDTH:
            s[2] *= -1
        if s[1] < 0 or s[1] >= HEIGHT:
            s[3] *= -1

    screen.fill((0,0,0))
    nearest = [[-1]*WIDTH for _ in range(HEIGHT)]
    for y in range(HEIGHT):
        for x in range(WIDTH):
            nearest[y][x] = nearest_site_index(x, y, sites)

    for y in range(HEIGHT):
        for x in range(WIDTH):
            i0 = nearest[y][x]
            edge = False
            if x+1 < WIDTH and nearest[y][x+1] != i0:
                edge = True
            if y+1 < HEIGHT and nearest[y+1][x] != i0:
                edge = True
            if edge:
                screen.set_at((x,y), (255,255,255))

    for (sx, sy, _, _) in sites:
        pygame.draw.circle(screen, (255,255,255), (sx, sy), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()