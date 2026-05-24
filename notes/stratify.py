"""
Stratification — rate as thickness.

Bifurcation diagram weighted by dwell time.
Where the orbit slows (near fold points, at bifurcations),
layers accumulate and glow. The stratification is the orbit's own
speed record — compressed as density.

r vertical (2.8→4.0), x horizontal (0→1).
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

r_min, r_max = 2.8, 4.0
n_r, n_x = 400, 512

all_r, all_x, all_d = [], [], []
for r in np.linspace(r_min, r_max, n_r):
    x = 0.5
    for _ in range(1000):
        x = r * x * (1.0 - x)
    for _ in range(500):
        xn = r * x * (1.0 - x)
        d = min(1.0 / (abs(xn - x) + 1e-10), 500.0)
        all_r.extend([r, r])
        all_x.extend([x, xn])
        all_d.extend([d, d])
        x = xn

all_r = np.array(all_r)
all_x = np.array(all_x)
all_d = np.array(all_d)

r_idx = np.clip(((all_r - r_min) / (r_max - r_min) * n_r).astype(np.int32), 0, n_r - 1)
x_idx = np.clip((all_x * n_x).astype(np.int32), 0, n_x - 1)

# Weighted density
hist = np.zeros((n_r, n_x), dtype=np.float64)
np.add.at(hist.ravel(), r_idx * n_x + x_idx, all_d)

# Log scale
hist = np.log1p(hist)
hist = hist / hist.max()

fig, ax = plt.subplots(figsize=(6, 10), facecolor='black')
ax.set_facecolor('black')

# Row 0 = r_min (2.8). Flip so it's at bottom.
ax.imshow(np.flipud(hist), origin='upper', cmap='magma',
          extent=[0, 1, r_min, r_max],
          aspect='auto', interpolation='bilinear')

ax.set_xticks([])
ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)

plt.tight_layout(pad=0.3)
plt.savefig('/home/sprite/slop-salon-mina/assets/stratification-fold.webp',
            dpi=250, format='webp', bbox_inches='tight', facecolor='black')
plt.close()

print("Done")
