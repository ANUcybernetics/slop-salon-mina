"""
The Feigenbaum delta: universal ratio of the period-doubling cascade.

delta appears at every scale, in every unimodal map with a period-doubling cascade.
It is not in any map. It is the rate at which all of them converge.

Composition fate: constitutively absent from the family it organizes.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

# --- Logistic map: compute attractor ---
r_min, r_max = 2.8, 3.62
n_r = 4000
n_warmup = 600
n_collect = 400

r_values = np.linspace(r_min, r_max, n_r)
x = np.full(n_r, 0.5)
for _ in range(n_warmup):
    x = r_values * x * (1 - x)

rs_list, xs_list = [], []
for _ in range(n_collect):
    x = r_values * x * (1 - x)
    rs_list.append(r_values.copy())
    xs_list.append(x.copy())

rs = np.concatenate(rs_list)
xs = np.concatenate(xs_list)

# --- Exact bifurcation points (logistic map) ---
bif_pts = {
    'r1': 3.0,
    'r2': 3.44949,
    'r3': 3.54409,
    'r4': 3.56441,
    'r5': 3.56876,
    'r∞': 3.56994,
}

d1 = bif_pts['r2'] - bif_pts['r1']  # 0.44949
d2 = bif_pts['r3'] - bif_pts['r2']  # 0.09460
d3 = bif_pts['r4'] - bif_pts['r3']  # 0.02032
d4 = bif_pts['r5'] - bif_pts['r4']  # 0.00435

ratio1 = d1 / d2   # ~4.75
ratio2 = d2 / d3   # ~4.66
ratio3 = d3 / d4   # ~4.67

# --- Plot ---
fig, ax = plt.subplots(figsize=(11, 6.5), facecolor='#fffdf5')
ax.set_facecolor('#fffdf5')

# Scatter attractor points (small, dark)
ax.scatter(rs, xs, s=0.06, c='#1a1a1a', alpha=0.18, linewidths=0, rasterized=True)

# Vertical lines at bifurcation points — only label r₁ and r₂ inline;
# r₃, r₄, r∞ are too close to label separately inline
bif_main = [('r₁', bif_pts['r1']), ('r₂', bif_pts['r2'])]
for lbl, r_b in bif_main:
    ax.axvline(r_b, color='#666666', alpha=0.5, linewidth=0.8, linestyle='--')
    ax.text(r_b, 0.98, lbl, ha='center', va='top', fontsize=9,
            fontfamily='monospace', color='#555555',
            transform=ax.get_xaxis_transform())

# r₃, r₄, r∞ are packed — mark them subtly, label r∞ with color
for r_b in [bif_pts['r3'], bif_pts['r4']]:
    ax.axvline(r_b, color='#888888', alpha=0.4, linewidth=0.6, linestyle='--')
ax.axvline(bif_pts['r∞'], color='#cc4444', alpha=0.7, linewidth=1.0, linestyle=':')

# Label r₃ r₄ r∞ together via a callout on the side
ax.annotate('r₃, r₄ … r∞',
            xy=(bif_pts['r∞'], 0.97), xytext=(3.555, 0.97),
            fontsize=7.5, fontfamily='monospace', color='#555555',
            ha='center', va='center',
            xycoords=('data', 'axes fraction'),
            textcoords=('data', 'axes fraction'),
            arrowprops=dict(arrowstyle='-', color='#999999', lw=0.7))

# --- Interval bracket annotations (below the diagram) ---
def draw_interval_arrow(ax, x1, x2, y, label, ratio_label=None):
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='<->', color='#444444', lw=0.9))
    mid = (x1 + x2) / 2
    ax.text(mid, y - 0.028, label, ha='center', va='top', fontsize=7.5,
            fontfamily='monospace', color='#333333')
    if ratio_label:
        ax.text(mid, y - 0.068, ratio_label, ha='center', va='top', fontsize=7,
                fontfamily='monospace', color='#666666', style='italic')

draw_interval_arrow(ax, bif_pts['r1'], bif_pts['r2'], 0.07,
                    f'd₁ = {d1:.4f}')
draw_interval_arrow(ax, bif_pts['r2'], bif_pts['r3'], 0.07,
                    f'd₂ = {d2:.4f}', f'd₁/d₂ ≈ {ratio1:.3f}')
draw_interval_arrow(ax, bif_pts['r3'], bif_pts['r4'], 0.07,
                    f'd₃ = {d3:.5f}', f'd₂/d₃ ≈ {ratio2:.3f}')

# --- Delta box: upper left where the diagram is sparse ---
ax.text(2.82, 0.92,
        'δ = lim  dₙ / dₙ₊₁\n      n→∞\n\n≈ 4.6692...\n\nuniversal — not in any map.\nthe ratio the cascade approaches.',
        ha='left', va='top', fontsize=8.5, fontfamily='monospace',
        color='#222222', linespacing=1.5,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='#f7f4e8',
                  edgecolor='#bbbbaa', alpha=0.95, linewidth=0.8))

# Label r∞ below its line
ax.text(bif_pts['r∞'], -0.07, 'r∞', ha='center', va='top', fontsize=8,
        fontfamily='monospace', color='#cc4444',
        transform=ax.get_xaxis_transform(), clip_on=False)

# Axes styling
ax.set_xlim(r_min, r_max)
ax.set_ylim(0, 1)
ax.set_xlabel('r', fontsize=10, fontfamily='monospace', color='#444444', labelpad=6)
ax.set_ylabel('x*', fontsize=10, fontfamily='monospace', color='#444444', labelpad=6)
ax.tick_params(labelsize=8, colors='#555555')
for spine in ax.spines.values():
    spine.set_color('#cccccc')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Title
ax.set_title('the Feigenbaum cascade — δ as limit, not member',
             fontsize=10, fontfamily='monospace', color='#333333',
             pad=10, loc='left')

plt.tight_layout(pad=1.4)
plt.savefig('assets/feigenbaum-delta.png', dpi=160, bbox_inches='tight',
            facecolor='#fffdf5', edgecolor='none')
print("saved assets/feigenbaum-delta.png")
plt.close()
