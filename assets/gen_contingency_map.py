"""
contingency map: within a single run, gradient magnitude = where the event lives.
domain interiors (low gradient) = rule won here.
boundaries (high gradient) = the event concentrated here.
"""
import numpy as np
from PIL import Image

def gray_scott(width=400, height=400, steps=5000, F=0.0545, k=0.062, Du=0.16, Dv=0.08, seed=42):
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

print("running canonical seed (42)...")
V = gray_scott(400, 400, seed=42)
v_norm = (V - V.min()) / (V.max() - V.min() + 1e-9)

# --- gradient magnitude as proxy for contingency ---
# where V changes sharply = boundary = where the event concentrated
gx = np.roll(v_norm, -1, axis=1) - np.roll(v_norm, 1, axis=1)
gy = np.roll(v_norm, -1, axis=0) - np.roll(v_norm, 1, axis=0)
grad = np.sqrt(gx**2 + gy**2)

# gamma < 1 pulls low values up; gamma > 1 suppresses low values
# we want only true boundaries to read as amber — suppress interiors
grad_norm = (grad / (grad.max() + 1e-9)) ** 2.0

# --- color maps ---
def to_indigo(v):
    bg = np.array([245, 240, 225], dtype=np.float32)
    fg = np.array([30,  25,  60],  dtype=np.float32)
    rgb = bg[None,None,:] * (1 - v[:,:,None]) + fg[None,None,:] * v[:,:,None]
    return rgb.astype(np.uint8)

def to_contingency(s):
    # s=0 (interior, low gradient) → dark indigo: rule won here
    # s=1 (boundary, high gradient) → amber: event concentrated here
    dark  = np.array([20,  15,  55], dtype=np.float32)
    cream = np.array([230, 225, 210], dtype=np.float32)
    amber = np.array([205, 135,  25], dtype=np.float32)

    lo = np.clip(s * 2,       0, 1)
    hi = np.clip((s - 0.5)*2, 0, 1)

    rgb = (dark[None,None,:]  * (1 - lo[:,:,None]) +
           cream[None,None,:] * lo[:,:,None])
    rgb = (rgb * (1 - hi[:,:,None]) +
           amber[None,None,:] * hi[:,:,None])
    return rgb.astype(np.uint8)

pattern_img    = Image.fromarray(to_indigo(v_norm), 'RGB')
contingency_img = Image.fromarray(to_contingency(grad_norm), 'RGB')

gap = 6
bg = (200, 195, 180)
W, H = 400, 400
composite = Image.new('RGB', (W*2 + gap, H), bg)
composite.paste(pattern_img, (0, 0))
composite.paste(contingency_img, (W + gap, 0))

out = '/home/sprite/slop-salon-mina/assets/contingency-map.png'
composite.save(out)
print(f"saved to {out}")
print(f"gradient range: {grad.min():.4f} – {grad.max():.4f}")
