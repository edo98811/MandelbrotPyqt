import numpy as np
from numba import njit, prange

@njit(parallel=True, fastmath=True)
def mandelbrot(width, height, cx, cy, zoom, max_iter):
    img = np.zeros((height, width), dtype=np.uint8)

    for px in prange(width):
        for py in range(height):

            x0 = (px - width/2) / zoom + cx
            y0 = (py - height/2) / zoom + cy

            x = 0.0
            y = 0.0

            i = 0
            while x*x + y*y <= 4 and i < max_iter:
                xt = x*x - y*y + x0
                y = 2*x*y + y0
                x = xt
                i += 1

            img[py, px] = i

    return img
