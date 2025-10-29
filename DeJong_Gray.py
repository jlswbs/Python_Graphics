# DeJong attractor renderer (grayscale, centered with margin)

import numpy as np
from PIL import Image
import math
import time

a = 1.4
b = -2.3
c = 2.4
d = -2.1

WIDTH, HEIGHT = 1920, 1080
ITERATIONS = 10000000
BURN_IN = 1000
GAMMA = 1.0
LOG_SCALE = True
MARGIN = 0.2
OUT_FILENAME = "dejong_gray.png"

def dejong_step(x, y, a, b, c, d):
    x_new = math.sin(a * y) - math.cos(b * x)
    y_new = math.sin(c * x) - math.cos(d * y)
    return x_new, y_new

def render_dejong(a, b, c, d,
                  width=WIDTH, height=HEIGHT,
                  iterations=ITERATIONS, burn_in=BURN_IN,
                  gamma=GAMMA, log_scale=LOG_SCALE, margin=MARGIN):

    start = time.time()
    xs = np.empty(iterations, dtype=np.float64)
    ys = np.empty(iterations, dtype=np.float64)
    x, y = 0.1, 0.1

    for _ in range(burn_in):
        x, y = dejong_step(x, y, a, b, c, d)

    for i in range(iterations):
        x, y = dejong_step(x, y, a, b, c, d)
        xs[i] = x
        ys[i] = y

    x_min, x_max = xs.min(), xs.max()
    y_min, y_max = ys.min(), ys.max()
    x_center = 0.5 * (x_min + x_max)
    y_center = 0.5 * (y_min + y_max)
    x_half = 0.5 * (x_max - x_min)
    y_half = 0.5 * (y_max - y_min)
    x_half *= (1 + margin)
    y_half *= (1 + margin)
    x_min = x_center - x_half
    x_max = x_center + x_half
    y_min = y_center - y_half
    y_max = y_center + y_half

    H, _, _ = np.histogram2d(xs, ys, bins=(width, height),
                             range=[[x_min, x_max], [y_min, y_max]])
    H = H.T

    if log_scale:
        img = np.log1p(H)
    else:
        img = H

    img_max = img.max()
    norm = np.zeros_like(img) if img_max <= 0 else img / img_max
    norm = np.power(norm, gamma)
    gray = (norm * 255.0).astype(np.uint8)
    image = Image.fromarray(gray, mode='L').transpose(Image.FLIP_TOP_BOTTOM)

    end = time.time()
    print(f"Rendered {iterations} pts in {end - start:.2f}s "
          f"→ bounds x[{x_min:.3f},{x_max:.3f}] y[{y_min:.3f},{y_max:.3f}]")

    return image

if __name__ == "__main__":
    img = render_dejong(a, b, c, d)
    img.save(OUT_FILENAME)
    print(f"Saved image -> {OUT_FILENAME}")
