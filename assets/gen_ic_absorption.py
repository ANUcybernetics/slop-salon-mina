"""
IC absorption: same rule, two very different initial conditions.
Rule 90 keeps the IC (or buries it unrecoverably).
RD erases it — the rule absorbs the IC into a family of patterns.

Left: sparse IC (3 seeds)
Right: dense IC (80 seeds, random)
Both: same F, k — same rule. Both at 5000 steps.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def gray_scott(width=360, height=360, steps=8000, F=0.0545, k=0.062,
               Du=0.16, Dv=0.08, seed=42, dense=True):
    rng = np.random.default_rng(seed)
    U = np.ones((height, width), dtype=np.float32)
    V = np.zeros((height, width), dtype=np.float32)

    if dense:
        for _ in range(80):
            cx = rng.integers(20, width-20)
            cy = rng.integers(20, height-20)
            r = rng.integers(3, 8)
            y0, y1 = max(0, cy-r), min(height, cy+r)
            x0, x1 = max(0, cx-r), min(width, cx+r)
            U[y0:y1, x0:x1] = 0.5 + rng.random((y1-y0, x1-x0)) * 0.1
            V[y0:y1, x0:x1] = 0.25 + rng.random((y1-y0, x1-x0)) * 0.1
    else:
        # 4x3 evenly-spaced seeds with larger radii so they propagate and merge
        cols, rows = 4, 3
        for row in range(rows):
            for col in range(cols):
                cx = int(width  * (col + 0.5) / cols)
                cy = int(height * (row + 0.5) / rows)
                r = 12
                y0, y1 = max(0, cy-r), min(height, cy+r)
                x0, x1 = max(0, cx-r), min(width, cx+r)
                U[y0:y1, x0:x1] = 0.5 + rng.random((y1-y0, x1-x0)) * 0.1
                V[y0:y1, x0:x1] = 0.25 + rng.random((y1-y0, x1-x0)) * 0.1

    def laplacian(Z):
        return (
            np.roll(Z, 1, axis=0) + np.roll(Z, -1, axis=0) +
            np.roll(Z, 1, axis=1) + np.roll(Z, -1, axis=1) - 4 * Z
        )

    dt = 1.0
    for _ in range(steps):
        uvv = U * V * V
        dU = Du * laplacian(U) - uvv + F * (1 - U)
        dV = Dv * laplacian(V) + uvv - (F + k) * V
        U += dt * dU
        V += dt * dV
        U = np.clip(U, 0, 1)
        V = np.clip(V, 0, 1)

    return V


def render_indigo(V):
    v = V.copy()
    v = (v - v.min()) / (v.max() - v.min() + 1e-9)
    bg = np.array([245, 240, 225], dtype=np.float32)
    fg = np.array([30,  25,  60],  dtype=np.float32)
    rgb = bg[None,None,:] * (1 - v[:,:,None]) + fg[None,None,:] * v[:,:,None]
    return Image.fromarray(rgb.astype(np.uint8), 'RGB')


print("sparse IC (3 seeds)...")
V_sparse = gray_scott(dense=False, seed=7)
img_sparse = render_indigo(V_sparse)

print("dense IC (80 seeds)...")
V_dense = gray_scott(dense=True, seed=42)
img_dense = render_indigo(V_dense)

# --- layout ---
W, H = 360, 360
gap = 8
label_h = 36
pad = 24

canvas_w = pad + W + gap + W + pad
canvas_h = pad + H + label_h + pad

bg_color = (235, 230, 215)
text_color = (40, 35, 70)
amber = (190, 120, 20)

canvas = Image.new('RGB', (canvas_w, canvas_h), bg_color)
canvas.paste(img_sparse, (pad, pad))
canvas.paste(img_dense,  (pad + W + gap, pad))

draw = ImageDraw.Draw(canvas)

# try to load a font; fallback to default
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf", 11)
except:
    font = ImageFont.load_default()
    font_small = font

label_y = pad + H + 6

draw.text((pad + W//2, label_y), "12 seeds (grid)", font=font, fill=text_color, anchor="mt")
draw.text((pad + W + gap + W//2, label_y), "80 seeds", font=font, fill=text_color, anchor="mt")

# subtitle line
sub_y = label_y + 16
draw.text((canvas_w // 2, sub_y),
          "same rule  ·  different initial conditions  ·  same family",
          font=font_small, fill=amber, anchor="mt")

out = '/home/sprite/slop-salon-mina/assets/ic-absorption.png'
canvas.save(out)
print(f"saved: {out}")
