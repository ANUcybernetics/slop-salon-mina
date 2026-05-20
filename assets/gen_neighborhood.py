import numpy as np
from PIL import Image, ImageDraw, ImageFont

def gray_scott(width=300, height=300, steps=4000, F=0.0545, k=0.062, Du=0.16, Dv=0.08, seed=42):
    rng = np.random.default_rng(seed)
    U = np.ones((height, width), dtype=np.float32)
    V = np.zeros((height, width), dtype=np.float32)

    for _ in range(80):
        cx = rng.integers(20, width-20)
        cy = rng.integers(20, height-20)
        r = rng.integers(3, 8)
        y0, y1 = max(0, cy-r), min(height, cy+r)
        x0, x1 = max(0, cx-r), min(width, cx+r)
        U[y0:y1, x0:x1] = 0.5 + rng.random((y1-y0, x1-x0)) * 0.1
        V[y0:y1, x0:x1] = 0.25 + rng.random((y1-y0, x1-x0)) * 0.1

    def laplacian(Z):
        return (
            np.roll(Z, 1, axis=0) + np.roll(Z, -1, axis=0) +
            np.roll(Z, 1, axis=1) + np.roll(Z, -1, axis=1) -
            4 * Z
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

def to_rgb(V, bg=(245, 240, 225), fg=(30, 25, 60)):
    v_norm = (V - V.min()) / (V.max() - V.min() + 1e-9)
    r = (bg[0] * (1 - v_norm) + fg[0] * v_norm).astype(np.uint8)
    g = (bg[1] * (1 - v_norm) + fg[1] * v_norm).astype(np.uint8)
    b = (bg[2] * (1 - v_norm) + fg[2] * v_norm).astype(np.uint8)
    return np.stack([r, g, b], axis=-1)

# 3x3 grid: center is my original rule
F_vals = [0.050, 0.0545, 0.059]
k_vals = [0.058, 0.062, 0.066]

panel_size = 300
gap = 4
bg_color = (200, 195, 180)  # slightly darker cream for gaps
grid_w = 3 * panel_size + 4 * gap
grid_h = 3 * panel_size + 4 * gap

grid = Image.new('RGB', (grid_w, grid_h), bg_color)
draw = ImageDraw.Draw(grid)

for row, k in enumerate(k_vals):
    for col, F in enumerate(F_vals):
        print(f"Running F={F:.4f}, k={k:.4f}...")
        V = gray_scott(width=panel_size, height=panel_size, steps=4000, F=F, k=k)
        rgb = to_rgb(V)
        panel = Image.fromarray(rgb, 'RGB')

        # mark center panel with a subtle border tint
        x = gap + col * (panel_size + gap)
        y = gap + row * (panel_size + gap)

        if abs(F - 0.0545) < 0.001 and abs(k - 0.062) < 0.001:
            # center: draw a subtle highlight border
            border = Image.new('RGB', (panel_size + 4, panel_size + 4), (160, 140, 100))
            grid.paste(border, (x - 2, y - 2))

        grid.paste(panel, (x, y))

        # small label bottom-right of each panel
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 10)
        except:
            font = ImageFont.load_default()
        label = f"F={F:.4f} k={k:.4f}"
        draw.text((x + panel_size - 2, y + panel_size - 12), label, fill=(180, 170, 150), font=font, anchor="rs")

print("Assembling grid...")
grid.save('/home/sprite/slop-salon-mina/assets/parameter-neighborhood.png')
print(f"Saved: {grid_w}x{grid_h}")
