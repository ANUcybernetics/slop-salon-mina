#!/usr/bin/env python3
"""
Cobweb: plenitude vs refusal colored by segment type.
Horizontal segments = refusal (diagonal, x → x)
Vertical segments = plenitude (function, x → f(x))
Each iteration has one of each. The ratio is delta.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def logistic(x, r):
    return r * x * (1 - x)

fig, ax = plt.subplots(figsize=(8, 7))
x = np.linspace(0, 1, 1000)
r_val = 3.5

# Function and diagonal
ax.plot(x, logistic(x, r_val), color='#c9a84c', linewidth=1.2, alpha=0.7, zorder=5)
ax.plot(x, x, color='#c9a84c', linewidth=1.2, alpha=0.7, zorder=5)

# Cobweb trace with colored segments
x0 = 0.3
x = x0
steps = 60

for i in range(steps):
    y = logistic(x, r_val)
    # Vertical: commitment to the function (plenitude)
    ax.plot([x, x], [x, y], color='#e8c84c', linewidth=1.0, alpha=0.8, solid_capstyle='round')
    # Horizontal: refusal (diagonal)
    ax.plot([x, y], [y, y], color='#6a5f3a', linewidth=1.0, alpha=0.8, solid_capstyle='round')
    x = y

# Highlight first 4 iterations with thicker lines
x = x0
for i in range(4):
    y = logistic(x, r_val)
    ax.plot([x, x], [x, y], color='#f0d85c', linewidth=1.8, alpha=0.9)
    ax.plot([x, y], [y, y], color='#8a7f5a', linewidth=1.8, alpha=0.9)
    x = y

# Legend
ax.plot([], [], color='#f0d85c', linewidth=2, label='plenitude (function)')
ax.plot([], [], color='#8a7f5a', linewidth=2, label='refusal (diagonal)')
ax.legend(loc='upper right', fontsize=8, frameon=False, labelcolor='#c9a84c')

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])
ax.set_facecolor('#08080f')
for spine in ax.spines.values():
    spine.set_visible(False)

fig.patch.set_facecolor('#08080f')

fig.text(0.5, 0.03,
    'plenitude is the map. refusal is the walk. each iteration has both.',
    ha='center', va='center', fontsize=9,
    color='#666677', style='italic')

fig.tight_layout(rect=[0, 0.06, 1, 1])
fig.savefig('/home/sprite/slop-salon-mina/assets/cobweb-plenitude-refusal.png',
            dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
print("saved cobweb-plenitude-refusal.png")
