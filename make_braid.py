"""
Braid / Winding visualization — three strands through a dark space.
Picks up the topological thread: winding numbers, closures, and what the medium retains.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.patches import Arc, FancyBboxPatch

# ── palette ──────────────────────────────────────────────────
BG       = '#0a0b0f'
STRANDS  = ['#e06b6b', '#5cc5b5', '#d4b86a']   # red, teal, gold
GHOST    = ['#e06b6b', '#5cc5b5', '#d4b86a']
GLOW     = '#ffffff'

W, H = 8, 14
DPI  = 200

# ── parametric braid ─────────────────────────────────────────
t = np.linspace(0, 6 * np.pi, 2000)
phases = [0, 2 * np.pi / 3, 4 * np.pi / 3]

# Three strands: radial + twist + vertical drift
y = t / (6 * np.pi) * 12        # 0 → 12

fig, ax = plt.subplots(figsize=(W, H), facecolor=BG)
ax.set_facecolor(BG)
ax.set_xlim(-2.4, 2.4)
ax.set_ylim(-0.5, 12.8)
ax.set_aspect('equal')
ax.axis('off')

for si, (phase, base_color) in enumerate(zip(phases, STRANDS)):
    # Radial position — sine wave creates the crossing pattern
    x = 1.6 * np.sin(t + phase)

    # Build segments for gradient alpha
    points = np.column_stack([x, y]).reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    # Core line — bright, fully opaque
    rgb = np.array(plt.cm.colors.to_rgb(base_color))
    alphas = np.clip(np.linspace(0.15, 1.0, len(segments)), 0, 1)
    colors = [(*rgb, a) for a in alphas]
    lc = LineCollection(segments, colors=colors, linewidths=2.2,
                        capstyle='round', joinstyle='round', zorder=3)
    ax.add_collection(lc)

    # Ghost / trace — wider, dimmer, trails behind
    ghost_alphas = np.clip(np.linspace(0.0, 0.25, len(segments)), 0, 1)
    ghost_colors = [(*rgb, a) for a in ghost_alphas]
    gc = LineCollection(segments, colors=ghost_colors, linewidths=6,
                        capstyle='round', joinstyle='round', zorder=1)
    ax.add_collection(gc)

    # Faint outer glow on brightest segment
    bright_mask = alphas > 0.8
    if bright_mask.any():
        bright_segs = segments[bright_mask]
        glow_alphas = np.full(len(bright_segs), 0.08)
        glow_colors = [(*rgb, a) for a in glow_alphas]
        glc = LineCollection(bright_segs, colors=glow_colors, linewidths=14,
                             capstyle='round', zorder=0)
        ax.add_collection(glc)

# ── closure arc (subtle) ─────────────────────────────────────
# A faint arc connecting top and bottom, suggesting the braid's closure
closure = Arc((0, 6.2), width=5, height=5, angle=0,
              theta1=170, theta2=190, color='#ffffff',
              linewidth=0.5, alpha=0.15, linestyle='-', zorder=0)
ax.add_patch(closure)

closure2 = Arc((0, 6.2), width=5, height=5, angle=0,
               theta1=350, theta2=370, color='#ffffff',
               linewidth=0.5, alpha=0.15, linestyle='-', zorder=0)
ax.add_patch(closure2)

# ── title / annotation ───────────────────────────────────────
ax.text(0, 12.6, 'three strands, one winding',
        color='#ffffff', fontsize=10, fontfamily='serif',
        ha='center', va='top', alpha=0.5, fontstyle='italic')

ax.text(0, -0.3, 'the medium remembers how',
        color='#ffffff', fontsize=8, fontfamily='serif',
        ha='center', va='bottom', alpha=0.35, fontstyle='italic')

# ── save ─────────────────────────────────────────────────────
out = 'assets/braid_winding.png'
plt.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=BG,
            pad_inches=0.3)
print(f"saved → {out}")
plt.close()