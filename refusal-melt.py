#!/usr/bin/env python3
"""Refusal -> Melt interpolation: three rows showing boundary-to-dissolution."""

import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter

# Layout: 3 rows stacked vertically, each row is a landscape panel
PANEL_W = 1024
PANEL_H = 280
PANEL_GAP = 24
MARGIN = 40
TOTAL_W = PANEL_W
TOTAL_H = 3 * PANEL_H + 4 * PANEL_GAP

def perlin(x, y, seed=0):
    def fade(t): return t * t * t * (t * (t * 6 - 15) + 10)
    def lerp(t, a, b): return a + t * (b - a)
    nX = 512
    def hash(ix, iy):
        h = seed ^ (ix * 374761393 + iy * 668265263)
        h = ((h & 0xffff) ^ (h >> 16)) * 1274126177
        return (h & 0x7fffffff) / 0x7fffffff
    ix = int(x) % nX
    iy = int(y) % (nX - 1)
    fx = x - int(x)
    fy = y - int(y)
    a = hash(ix, iy)
    b = hash(ix + 1, iy)
    c = hash(ix, iy + 1)
    d = hash(ix + 1, iy + 1)
    return lerp(fade(fx), lerp(fade(fy), a, c), lerp(fade(fy), b, d))

def noise_field(w, h, scale=4.0, seed=0):
    data = np.zeros((h, w), dtype=np.float32)
    for y in range(h):
        for x in range(w):
            data[y, x] = perlin(x / scale, y / scale, seed)
    return data

# Generate one wide field, slice into 3 rows
field = noise_field(PANEL_W, PANEL_H * 3, scale=8.0, seed=42)
f0 = field[:PANEL_H, :]
f1 = field[PANEL_H:2*PANEL_H, :]
f2 = field[2*PANEL_H:3*PANEL_H, :]

# Panel 0: Refusal (sharp BC)
panel0 = (f0 >= 0.5).astype(np.float32)

# Panel 1: Transition (boundary ceasing to hold)
panel1 = 0.4 * (f1 >= 0.5).astype(np.float32) + 0.6 * gaussian_filter(f1, sigma=6.0)

# Panel 2: Melt (fully dissolved)
panel2 = gaussian_filter(f2, sigma=12.0)

def to_rgb(arr):
    arr = np.clip(arr, 0, 1)
    rgb = np.stack([arr, arr * 0.97, arr * 0.94], axis=-1) * 255
    return Image.fromarray(rgb.astype(np.uint8), mode='RGB')

# Composite vertically with gaps
composite = Image.new('RGB', (TOTAL_W, TOTAL_H), (0, 0, 0))
y_offset = MARGIN
for panel, y_off in [(panel0, y_offset), (panel1, y_offset + PANEL_H + PANEL_GAP), (panel2, y_offset + 2*(PANEL_H + PANEL_GAP))]:
    im = to_rgb(panel)
    composite.paste(im, (0, y_off))

y_offset = MARGIN
draw = ImageDraw.Draw(composite)
labels = ["refusal", "transition", "melt"]
for i, label in enumerate(labels):
    y = y_offset + i * (PANEL_H + PANEL_GAP) + PANEL_H + 12
    draw.text((16, y), label, fill=(90, 90, 90))

composite.save('assets/refusal-melt.png', quality=92)
print(f"Saved ({TOTAL_W}x{TOTAL_H})")

import os
sz = os.path.getsize('assets/refusal-melt.png')
print(f"Size: {sz / 1024:.0f} KB")
