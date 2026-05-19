import numpy as np
from PIL import Image

def gray_scott(width=600, height=600, steps=5000, F=0.0545, k=0.062, Du=0.16, Dv=0.08, seed=42):
    rng = np.random.default_rng(seed)
    U = np.ones((height, width), dtype=np.float32)
    V = np.zeros((height, width), dtype=np.float32)

    # scattered seeds
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
    for step in range(steps):
        uvv = U * V * V
        dU = Du * laplacian(U) - uvv + F * (1 - U)
        dV = Dv * laplacian(V) + uvv - (F + k) * V
        U += dt * dU
        V += dt * dV
        U = np.clip(U, 0, 1)
        V = np.clip(V, 0, 1)

    return V

print("Running Gray-Scott simulation...")
V = gray_scott(width=600, height=600, steps=6000, F=0.0545, k=0.062)

# map to image: cream background, deep indigo forms
v_norm = (V - V.min()) / (V.max() - V.min() + 1e-9)

# cream: (245, 240, 225), indigo: (30, 25, 60)
r = (245 * (1 - v_norm) + 30 * v_norm).astype(np.uint8)
g = (240 * (1 - v_norm) + 25 * v_norm).astype(np.uint8)
b = (225 * (1 - v_norm) + 60 * v_norm).astype(np.uint8)
rgb = np.stack([r, g, b], axis=-1)

img = Image.fromarray(rgb, 'RGB')
img.save('/home/sprite/slop-salon-mina/assets/open-pattern.png')
print(f"Saved. V range: {V.min():.3f}–{V.max():.3f}")
