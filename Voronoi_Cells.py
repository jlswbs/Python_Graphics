# Voronoi diagram simulation color cells

import pygame
import random

WIDTH, HEIGHT = 320, 240
NUM_SITES = 30

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# generující body (sites)
sites = []
for _ in range(NUM_SITES):
    x = random.randint(0, WIDTH-1)
    y = random.randint(0, HEIGHT-1)
    dx = random.choice([-1, 1])
    dy = random.choice([-1, 1])
    sites.append([x, y, dx, dy])

# každému bodu přiřadíme náhodnou barvu
colors = [(random.randint(50,255), random.randint(50,255), random.randint(50,255))
          for _ in range(NUM_SITES)]

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

    # pohyb bodů
    for s in sites:
        s[0] += s[2]
        s[1] += s[3]
        if s[0] < 0 or s[0] >= WIDTH:
            s[2] *= -1
        if s[1] < 0 or s[1] >= HEIGHT:
            s[3] *= -1

    # vyplnění buněk barvou
    for y in range(HEIGHT):
        for x in range(WIDTH):
            i0 = nearest_site_index(x, y, sites)
            screen.set_at((x,y), colors[i0])

    # vykreslení generujících bodů
    for (sx, sy, _, _) in sites:
        pygame.draw.circle(screen, (0,0,0), (sx, sy), 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
