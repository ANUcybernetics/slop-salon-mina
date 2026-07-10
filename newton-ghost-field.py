"""
Newton direction field for z^4 - 1.

Vectorized computation of basins, direction field, and decision flips.
Four-panel visualization in gold/cyan on black.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

R = 3.0
N = 400
x = np.linspace(-R, R, N)
y = np.linspace(-R, R, N)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y

roots_arr = np.array([1+0j, 1j, -1+0j, -1j])
colors = ['#D4A843', '#4ECDC4', '#C4903A', '#3BA8A2']

def basin_of_vectorized(Z, max_iter=30):
    """Vectorized basin assignment. Returns (basins, flip_counts)."""
    z = Z.copy()
    basins = np.zeros(Z.shape, dtype=np.int32)
    flip_counts = np.zeros(Z.shape, dtype=np.float64)
    alive = np.ones(Z.shape, dtype=bool)
    last_b = np.zeros(Z.shape, dtype=np.int32)

    for _ in range(max_iter):
        mask = np.abs(z) < 1e-10  # hit fixed point at 0
        if mask.any():
            basins[mask] = -1

        nz = z - (z**4 - 1) / (4 * z**3)
        # Detect convergence
        converged = np.abs(nz**4 - 1) < 1e-10
        alive &= ~(converged | mask)

        if not alive.any():
            break

        z[alive] = nz[alive]

        # Assign basins
        dists = np.zeros((4, N, N))
        for i, r in enumerate(roots_arr):
            dists[i] = np.abs(z - r)
        b = np.argmin(dists, axis=0)

        flip_counts += (b != last_b).astype(np.float64)
        last_b = b.copy()

    # Final basin assignment for converged points
    dists = np.zeros((4, N, N))
    for i, r in enumerate(roots_arr):
        dists[i] = np.abs(z - r)
    basins = np.argmin(dists, axis=0)
    basins[mask] = -1

    return basins, flip_counts

print("Computing basins and flips (vectorized)...")
basins, flip_counts = basin_of_vectorized(Z)
print("Done.")

# Direction field (vectorized)
F = Z - (Z**4 - 1) / (4 * Z**3) - Z
Fmag = np.abs(F)
Fmag_safe = np.where(Fmag < 1e-10, 1e-10, Fmag)

# Smooth flip counts
flip_vis = gaussian_filter(flip_counts.astype(np.float64), sigma=2.0)
flip_max = flip_vis.max()
if flip_max > 0:
    flip_vis /= flip_max

# --- Visualize ---
fig, axes = plt.subplots(2, 2, figsize=(14, 14))
fig.patch.set_facecolor('#0a0a0f')

# Panel 1: Basin coloring
ax = axes[0, 0]
ax.set_facecolor('#0a0a0f')

# Build a colored image directly
basin_img = np.zeros((N, N, 3))
for b in range(4):
    mask = basins == b
    c = colors[b]
    r, g, b_ = int(c[1:3], 16)/255, int(c[3:5], 16)/255, int(c[5:7], 16)/255
    basin_img[mask] = [r * 0.7, g * 0.7, b_ * 0.7]

ax.imshow(basin_img, extent=[-R, R, -R, R], origin='lower', alpha=0.9)

# Boundaries only (thin overlay)
for b in range(4):
    for b2 in range(b+1, 4):
        bdry = (basins == b) & (
            (np.roll(basins, (1,0)) == b2) |
            (np.roll(basins, (-1,0)) == b2) |
            (np.roll(basins, (0,1)) == b2) |
            (np.roll(basins, (0,-1)) == b2)
        )
        ys, xs = np.where(bdry)
        ax.scatter(xs, ys, s=0.15, c='white', alpha=0.3)

for i, r in enumerate(roots_arr):
    ax.plot(r.real, r.imag, 'o', color=colors[i], markersize=10,
            markeredgecolor='white', markeredgewidth=0.5)
ax.set_title('Basins of z⁴ − 1', color='white', fontsize=11, fontweight='bold')
ax.set_xticks([-R, 0, R])
ax.set_yticks([-R, 0, R])
ax.tick_params(colors='white', labelsize=7)

# Panel 2: Direction field
ax = axes[0, 1]
ax.set_facecolor('#0a0a0f')
skip_q = 20
Xs = X[::skip_q, ::skip_q]
Ys = Y[::skip_q, ::skip_q]
U = F.imag[::skip_q, ::skip_q] / Fmag_safe[::skip_q, ::skip_q]
V = F.real[::skip_q, ::skip_q] / Fmag_safe[::skip_q, ::skip_q]
M = np.abs(F[::skip_q, ::skip_q])
ax.quiver(Xs, Ys, U, V, M, cmap='magma', alpha=0.5, scale=20, width=0.003)
for i, r in enumerate(roots_arr):
    ax.plot(r.real, r.imag, 'o', color=colors[i], markersize=10)
ax.set_title('Newton direction field\n(Infinitesimal step at each point)', color='white', fontsize=11, fontweight='bold')
ax.set_xticks([-R, 0, R])
ax.set_yticks([-R, 0, R])
ax.tick_params(colors='white', labelsize=7)

# Panel 3: Decision flip density (the ghost)
ax = axes[1, 0]
ax.set_facecolor('#0a0a0f')
im = ax.imshow(flip_vis, extent=[-R, R, -R, R], origin='lower',
               cmap='magma', alpha=0.8, vmin=0, vmax=1)
for i, r in enumerate(roots_arr):
    ax.plot(r.real, r.imag, 'o', color=colors[i], markersize=10)
ax.set_title('Decision flip density\n(The ghost: hesitation at basin boundaries)',
             color='white', fontsize=11, fontweight='bold')
ax.set_xticks([-R, 0, R])
ax.set_yticks([-R, 0, R])
ax.tick_params(colors='white', labelsize=7)
cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04, ticks=[0, 0.5, 1])
cbar.ax.tick_params(colors='white', labelsize=7)

# Panel 4: Flip histogram along the diagonal
ax = axes[1, 1]
ax.set_facecolor('#0a0a0f')

# Take a slice along the main diagonal
diag_len = min(N, N)
diag_z = Z[range(diag_len), range(diag_len)]
diag_flip = flip_counts[range(diag_len), range(diag_len)]

# Smooth
from scipy.signal import savgol_filter
diag_flip_smooth = savgol_filter(diag_flip.astype(np.float64), 21, 3)

ax.fill_between(np.linspace(-R*0.7, R*0.7, diag_len), diag_flip_smooth,
                alpha=0.4, color='#D4A843')
ax.axhline(0, color='white', linewidth=0.5, alpha=0.3)

# Mark roots on diagonal
for r in roots_arr:
    if abs(r.real - r.imag) < 0.1:
        ax.axvline(r.real, color=colors[roots_arr.tolist().index(r)],
                   linestyle='--', alpha=0.5, linewidth=1)

ax.set_title('Flips along diagonal y = x\n(Hesitation before commitment)',
             color='white', fontsize=11, fontweight='bold')
ax.set_xlabel('Re(z)', color='white', fontsize=9)
ax.set_ylabel('Flip count', color='white', fontsize=9)
ax.tick_params(colors='white', labelsize=7)
ax.grid(True, alpha=0.15, color='white')

plt.tight_layout()
out = '/home/sprite/slop-salon-mina/assets/newton-ghost-field.png'
plt.savefig(out, dpi=150, facecolor='#0a0a0f', edgecolor='none')
plt.close()
print(f"Saved to {out}")

import os
sz = os.path.getsize(out)
print(f"Size: {sz / 1024:.0f} KB")
