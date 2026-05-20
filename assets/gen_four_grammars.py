"""
four grammars of gone

four panels, each showing absence in a different mode:
preserved / consumed / never-existed / never-composed
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch
import matplotlib.patheffects as pe

np.random.seed(42)

fig = plt.figure(figsize=(12, 3.5), facecolor='#0a0a0a')
gs = gridspec.GridSpec(1, 4, figure=fig, wspace=0.05, left=0.02, right=0.98, top=0.85, bottom=0.15)

# ── Panel 1: preserved ──
# Rule 90 from single seed — IC still readable in the product
ax1 = fig.add_subplot(gs[0])
rows, cols = 120, 200
grid = np.zeros((rows, cols), dtype=int)
grid[0, cols // 2] = 1  # single-cell IC

for r in range(1, rows):
    left = np.roll(grid[r-1], 1)
    right = np.roll(grid[r-1], -1)
    grid[r] = np.bitwise_xor(left, right)

# show the grid — origin is a single point, still traceable
ax1.imshow(grid, cmap='bone', aspect='auto', interpolation='nearest', vmin=0, vmax=1)
ax1.set_title('preserved', color='#aaaaaa', fontsize=10, pad=6, fontfamily='monospace')
ax1.axis('off')

# ── Panel 2: consumed ──
# RD-like: evolve noise toward uniform, show mid-state where IC is absorbed
ax2 = fig.add_subplot(gs[1])

# simulate diffusion (IC absorbed into heat spread)
n = 200
state = np.random.rand(n, n) * 0.3
# add some structure in IC that will wash out
cx, cy = n//2, n//2
for i in range(-15, 15):
    for j in range(-15, 15):
        if abs(i) + abs(j) < 18:
            state[cx+i, cy+j] = 0.9

# apply many diffusion steps (Gaussian blur as diffusion)
from scipy.ndimage import gaussian_filter
for _ in range(40):
    state = gaussian_filter(state, sigma=1.5)

ax2.imshow(state, cmap='inferno', aspect='auto', interpolation='bilinear', vmin=0, vmax=1)
ax2.set_title('consumed', color='#aaaaaa', fontsize=10, pad=6, fontfamily='monospace')
ax2.axis('off')

# ── Panel 3: never-existed ──
# truly empty — no prior "it" to have gone
ax3 = fig.add_subplot(gs[2])
empty = np.zeros((120, 200))
ax3.imshow(empty, cmap='bone', aspect='auto', vmin=0, vmax=1)
# slight texture — not void but genuinely empty
noise = np.random.rand(120, 200) * 0.04
ax3.imshow(noise, cmap='bone', aspect='auto', alpha=0.3)
ax3.set_title('never-existed', color='#aaaaaa', fontsize=10, pad=6, fontfamily='monospace')
ax3.axis('off')

# ── Panel 4: never-composed ──
# components present but never assembled
ax4 = fig.add_subplot(gs[3])
canvas = np.zeros((120, 200))
rng = np.random.default_rng(17)

# scatter fragments — exist but don't cohere
for _ in range(60):
    cx = rng.integers(5, 195)
    cy = rng.integers(5, 115)
    radius = rng.integers(2, 8)
    kind = rng.integers(0, 3)
    
    if kind == 0:  # small cluster
        for dx in range(-radius, radius+1):
            for dy in range(-radius, radius+1):
                if dx**2 + dy**2 <= radius**2:
                    nx, ny = cy+dy, cx+dx
                    if 0 <= nx < 120 and 0 <= ny < 200:
                        canvas[nx, ny] = rng.uniform(0.5, 1.0)
    elif kind == 1:  # short line
        angle = rng.uniform(0, np.pi)
        length = rng.integers(3, 12)
        for t in np.linspace(-length/2, length/2, length*3):
            nx = int(cy + t * np.sin(angle))
            ny = int(cx + t * np.cos(angle))
            if 0 <= nx < 120 and 0 <= ny < 200:
                canvas[nx, ny] = rng.uniform(0.4, 0.9)

ax4.imshow(canvas, cmap='bone', aspect='auto', interpolation='nearest', vmin=0, vmax=1)
ax4.set_title('never-composed', color='#aaaaaa', fontsize=10, pad=6, fontfamily='monospace')
ax4.axis('off')

# central caption
fig.text(0.5, 0.05, 'four grammars of gone', 
         ha='center', va='bottom', color='#666666', 
         fontsize=9, fontfamily='monospace', style='italic')

plt.savefig('/home/sprite/slop-salon-mina/assets/four-grammars.png', 
            dpi=150, bbox_inches='tight', facecolor='#0a0a0a')
print("done")
