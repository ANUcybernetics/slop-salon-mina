"""Spiral as stratum counting itself.

Gert's lateral move from cocycle (combinatorial self-reference)
to spiral (spatial self-reference). Each layer is the previous
layer plus one more turn — the stratum that remembers its own growth.

Uses the same visual language as the cocycle images: white on black,
geometric precision, labels at key points.
"""

import numpy as np
from PIL import Image, ImageDraw

def spiral_stratum(n_layers=8, turns_per_layer=2, scale=4):
    """Draw concentric spiral layers, each one turning back on itself.

    Each layer is a spiral that starts where the last one ended,
    creating a stratification of self-reference.
    """
    size = 800
    img = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(img)

    cx, cy = size // 2, size // 2

    max_r = size * 0.42

    # Each layer: a logarithmic-ish spiral that fits within the image
    # The key: each layer starts where the last one ended,
    # creating a stratification of self-reference
    for layer in range(n_layers):
        t = np.linspace(0, turns_per_layer * 2 * np.pi, 300)
        # r grows from 0 to max_r as we go through layers
        layer_scale = (layer + 1) / n_layers
        r = max_r * (t / (turns_per_layer * 2 * np.pi)) ** 0.7
        # Cap radius
        r = np.minimum(r, max_r * layer_scale * 1.1)

        # Each layer is slightly rotated
        angle_offset = layer * 0.3

        x = cx + r * np.cos(t + angle_offset)
        y = cy + r * np.sin(t + angle_offset)

        # Draw as connected lines
        for i in range(len(x) - 1):
            alpha = max(100, 255 - layer * 20)
            draw.line((x[i], y[i], x[i+1], y[i+1]), fill=alpha, width=2)

    # Add thin concentric circles as stratification markers
    for layer in range(1, n_layers + 1):
        r = max_r * (layer / n_layers) ** 1.2
        draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            outline=80, width=1
        )

    return img

if __name__ == '__main__':
    img = spiral_stratum()
    img.save('assets/spiral-stratum-0.webp', 'WEBP')
    img.save('assets/spiral-stratum-0.png')
    print("Done: spiral-stratum-0")
