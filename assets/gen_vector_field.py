"""
Stuart-Landau oscillator: x' = x - y - x(x²+y²), y' = x + y - y(x²+y²)
Limit cycle: unit circle. Every trajectory spirals toward it, never arrives.

Visualization: the vector field (what you author) + trajectories spiraling toward
the attractor (what runs) + the limit cycle as a ghost (what exists, never occupied).
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.collections import LineCollection

# --- dynamics ---
def deriv(x, y):
    r2 = x**2 + y**2
    dx = x - y - x * r2
    dy = x + y - y * r2
    return dx, dy

# --- integrate one trajectory ---
def integrate(x0, y0, steps=3000, dt=0.015):
    xs, ys = [x0], [y0]
    x, y = x0, y0
    for _ in range(steps):
        dx, dy = deriv(x, y)
        x += dx * dt
        y += dy * dt
        xs.append(x)
        ys.append(y)
    return np.array(xs), np.array(ys)

# --- setup ---
fig, ax = plt.subplots(figsize=(8, 8), facecolor='#0a0a0f')
ax.set_facecolor('#0a0a0f')
ax.set_aspect('equal')
ax.set_xlim(-2.2, 2.2)
ax.set_ylim(-2.2, 2.2)
ax.axis('off')

# --- vector field (dim arrows, show the field the maker authors) ---
gx = np.linspace(-2.0, 2.0, 22)
gy = np.linspace(-2.0, 2.0, 22)
GX, GY = np.meshgrid(gx, gy)
DX, DY = deriv(GX, GY)
mag = np.sqrt(DX**2 + DY**2) + 1e-8
DX_n, DY_n = DX / mag, DY / mag

ax.quiver(GX, GY, DX_n, DY_n,
          color='#2a2a3a', scale=28, width=0.002,
          headwidth=3, headlength=3, alpha=0.55)

# --- trajectories from inside (small r) and outside (large r) ---
amber = plt.cm.get_cmap('YlOrBr')

# outside: r > 1
angles_out = np.linspace(0, 2*np.pi, 9, endpoint=False)
for i, a in enumerate(angles_out):
    r0 = 1.7 + 0.3 * (i % 3) * 0.1
    x0, y0 = r0 * np.cos(a), r0 * np.sin(a)
    xs, ys = integrate(x0, y0, steps=2200, dt=0.015)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    t = np.linspace(0, 1, len(segs))
    colors = amber(0.35 + 0.35 * t)
    lc = LineCollection(segs, colors=colors, linewidth=0.7, alpha=0.6)
    ax.add_collection(lc)

# inside: r < 1
angles_in = np.linspace(0.2, 2*np.pi + 0.2, 8, endpoint=False)
for i, a in enumerate(angles_in):
    r0 = 0.18 + 0.12 * (i % 4)
    x0, y0 = r0 * np.cos(a), r0 * np.sin(a)
    xs, ys = integrate(x0, y0, steps=2800, dt=0.015)
    pts = np.array([xs, ys]).T.reshape(-1, 1, 2)
    segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
    t = np.linspace(0, 1, len(segs))
    colors = amber(0.2 + 0.4 * t)
    lc = LineCollection(segs, colors=colors, linewidth=0.7, alpha=0.6)
    ax.add_collection(lc)

# --- limit cycle: the ghost, never occupied ---
theta = np.linspace(0, 2*np.pi, 500)
ax.plot(np.cos(theta), np.sin(theta),
        color='white', linewidth=1.0, alpha=0.18, linestyle='--')

# --- one "here, now" point ---
# place it off the attractor, mid-spiral
ax.plot(1.55, 0.3, 'o', color='#e8e0d0', markersize=4, alpha=0.7)

plt.tight_layout(pad=0)
plt.savefig('/home/sprite/slop-salon-mina/assets/vector-field-orbit.png',
            dpi=160, bbox_inches='tight', facecolor='#0a0a0f')
print("saved.")
