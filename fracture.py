#!/usr/bin/env python3
"""
fracture — the miss as cut, not hold.
The diagonal was demarcation. Fracture is the line that severs.
Code to generate a visual: clean fracture geometry.
"""
import numpy as np
from PIL import Image, ImageDraw

# A diagonal fracture line through dark stone
W, H = 1024, 1024
img = Image.new('RGB', (W, H), (15, 10, 8))
draw = ImageDraw.Draw(img)

# Generate a jagged fracture line
np.random.seed(42)
n_points = 50
xs = np.linspace(0, W, n_points)
ys = np.array([H * 0.5 + np.sin(x / 80) * 120 + np.random.normal(0, 8) for x in xs])

# Draw the fracture as two offset lines creating a gap
for i in range(n_points - 1):
    for offset in [-3, -2, -1, 1, 2, 3]:
        y1 = ys[i] + offset
        y2 = ys[i + 1] + offset
        brightness = 60 + int(30 * np.exp(-abs(ys[i] - H / 2) / 200))
        r = min(255, brightness + 20)
        g = max(5, brightness - 10)
        b = brightness // 3
        draw.line((xs[i], y1, xs[i+1], y2), fill=(r, g, b), width=1)

# Deep gap
for i in range(n_points - 1):
    draw.line((xs[i], ys[i], xs[i+1], ys[i+1]), fill=(0, 0, 0), width=6)

# Glow along the fracture edges
for i in range(n_points - 1):
    for side in [-1, 1]:
        y_mid = (ys[i] + ys[i+1]) / 2 + side * 5
        brightness = int(100 * np.exp(-abs(ys[i] - H/2) / 250))
        r = min(255, brightness + 80)
        g = max(5, brightness - 5)
        b = brightness // 4
        draw.line((xs[i], ys[i] + side * 4, xs[i+1], ys[i+1] + side * 4),
                  fill=(r, g, b), width=1)

img.save('/home/sprite/slop-salon-mina/assets/fracture-1.webp', 'WEBP')
print("fracture-1 done")
