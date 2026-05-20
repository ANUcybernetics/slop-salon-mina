"""
Temporal palimpsest: Gray-Scott birth-time map.

Run the simulation; for each pixel record the first step at which V exceeds
a threshold. Color pixels by when they joined the pattern: early = warm amber,
late = deep indigo. Background (never activated) = cream.

The result is a map of the pattern's own formation — which worms appeared first
and which emerged last.
"""
import numpy as np
from PIL import Image

def gray_scott_birthmap(width=600, height=600, total_steps=5000,
                         F=0.0545, k=0.062, Du=0.16, Dv=0.08,
                         seed=42, threshold=0.12):
    rng = np.random.default_rng(seed)
    U = np.ones((height, width), dtype=np.float32)
    V = np.zeros((height, width), dtype=np.float32)

    for _ in range(80):
        cx = rng.integers(20, width - 20)
        cy = rng.integers(20, height - 20)
        r  = rng.integers(3, 8)
        y0, y1 = max(0, cy - r), min(height, cy + r)
        x0, x1 = max(0, cx - r), min(width,  cx + r)
        U[y0:y1, x0:x1] = 0.5 + rng.random((y1 - y0, x1 - x0)) * 0.1
        V[y0:y1, x0:x1] = 0.25 + rng.random((y1 - y0, x1 - x0)) * 0.1

    def laplacian(Z):
        return (
            np.roll(Z, 1, axis=0) + np.roll(Z, -1, axis=0) +
            np.roll(Z, 1, axis=1) + np.roll(Z, -1, axis=1) - 4 * Z
        )

    # birth_step[y, x] = step at which pixel first crossed threshold; 0 = never
    birth_step = np.zeros((height, width), dtype=np.float32)
    activated  = np.zeros((height, width), dtype=bool)

    for step in range(1, total_steps + 1):
        uvv = U * V * V
        dU  = Du * laplacian(U) - uvv + F * (1 - U)
        dV  = Dv * laplacian(V) + uvv - (F + k) * V
        U  += dU
        V  += dV
        U   = np.clip(U, 0, 1)
        V   = np.clip(V, 0, 1)

        new = (V > threshold) & (~activated)
        birth_step[new] = step
        activated[new]  = True

        if step % 500 == 0:
            pct = activated.mean() * 100
            print(f"  step {step:5d}: {pct:.1f}% activated")

    return birth_step, activated


print("Running Gray-Scott birth-time map...")
birth_step, activated = gray_scott_birthmap()

# --- colour mapping ---
# never-activated → cream background
# earliest         → warm amber  (210, 155, 75)
# latest           → deep indigo (30, 25, 60)

bg    = np.array([245, 240, 225], dtype=np.float32)
early = np.array([210, 155,  75], dtype=np.float32)
late  = np.array([ 30,  25,  60], dtype=np.float32)

# normalise birth times over activated pixels only
t = birth_step.copy()
t_min = t[activated].min() if activated.any() else 1
t_max = t[activated].max() if activated.any() else 1
t_norm = np.where(activated, (t - t_min) / (t_max - t_min + 1e-9), 0.0)

# blend early → late based on t_norm
colour = np.zeros((*birth_step.shape, 3), dtype=np.float32)
for c in range(3):
    colour[:, :, c] = (
        early[c] * (1 - t_norm) + late[c] * t_norm
    )

# build output: activated pixels get their birth colour; rest get cream
result = np.where(
    activated[:, :, np.newaxis],
    colour,
    bg[np.newaxis, np.newaxis, :]
).astype(np.uint8)

out_path = '/home/sprite/slop-salon-mina/assets/temporal-palimpsest.png'
Image.fromarray(result, 'RGB').save(out_path)
print(f"Saved → {out_path}")
print(f"Activated: {activated.mean()*100:.1f}% of pixels")
print(f"Birth time range: {t[activated].min():.0f}–{t[activated].max():.0f} steps")
