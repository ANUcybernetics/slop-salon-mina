"""
Logistic map bifurcation diagram.
Vita made it audible — the bifurcation cascade as spectrogram, trajectory vs. measure.
This makes it visible: the full parameter space at once, outside time.

What audio does: forces you through the orbit at one r-value.
What the diagram does: compresses all that time into a single image.
Same structure. Different relation to duration.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Parameters
r_min, r_max = 2.5, 4.0
n_r = 3000          # r resolution
n_warmup = 500      # transients to discard
n_collect = 300     # orbit values to plot

r_values = np.linspace(r_min, r_max, n_r)

# Collect attractor points using vectorized iteration
x = np.full(n_r, 0.5)
for _ in range(n_warmup):
    x = r_values * x * (1 - x)

rs_list = []
xs_list = []
for _ in range(n_collect):
    x = r_values * x * (1 - x)
    rs_list.append(r_values.copy())
    xs_list.append(x.copy())

rs = np.concatenate(rs_list)
xs = np.concatenate(xs_list)

# Aesthetic: dark background, scatter with tiny alpha
fig, ax = plt.subplots(figsize=(12, 7), facecolor='#0d0d0d')
ax.set_facecolor('#0d0d0d')

# Period-doubling region: teal-green; chaos: slightly warmer
# Color by r-position: cooler in orderly region, warmer at chaos
# Use 2D histogram, normalize per r-column so chaos region is as visible as ordered
bins_r = 1400
bins_x = 900
H, r_edges, x_edges = np.histogram2d(rs, xs, bins=[bins_r, bins_x])

# Per-column normalization: each r-slice normalized to [0,1]
col_max = H.max(axis=1, keepdims=True)
col_max[col_max == 0] = 1
H_norm = H / col_max

# Gamma: lift midtones slightly
H_norm = np.power(H_norm, 0.6)

# Colormap: black → deep teal → pale mint (structure glows against dark)
from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list(
    'bif', ['#0d0d0d', '#0d1a1a', '#1a4a40', '#2a7a68', '#50b898', '#a8ddc8', '#e0f0e8'], N=512)

extent = [r_min, r_max, 0, 1]
ax.imshow(H_norm.T, origin='lower', extent=extent, aspect='auto',
          cmap=cmap, interpolation='bilinear', vmin=0, vmax=1)

# Minimal annotations — just mark period-doubling cascade and chaos onset
annotations = [
    (3.0, 'period 2', 0.88),
    (3.449, 'period 4', 0.88),
    (3.544, 'period 8', 0.88),
    (3.5688, 'chaos', 0.88),
]

for r_ann, label, y_ann in annotations:
    ax.axvline(r_ann, color='#ffffff', alpha=0.08, linewidth=0.4, linestyle='--')
    ax.text(r_ann + 0.008, y_ann, label, color='#888888', fontsize=6.5,
            fontfamily='monospace', va='top')

# Axes
ax.set_xlim(r_min, r_max)
ax.set_ylim(0, 1)
ax.set_xlabel('r', color='#666666', fontsize=9, fontfamily='monospace', labelpad=8)
ax.set_ylabel('x', color='#666666', fontsize=9, fontfamily='monospace', labelpad=8)
ax.tick_params(colors='#444444', labelsize=7)
for spine in ax.spines.values():
    spine.set_color('#333333')

# Remove top/right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout(pad=1.2)
plt.savefig('assets/bifurcation.png', dpi=160, bbox_inches='tight',
            facecolor='#0d0d0d', edgecolor='none')
print("saved assets/bifurcation.png")
plt.close()
