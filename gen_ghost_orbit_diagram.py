"""
Ghost orbit / saddle-node bifurcation diagram.
x' = r - x^2

Shows:
- Left: bifurcation diagram with ghost zone (r < 0)
- Middle: vector field at three r values showing the bottleneck
- Right: orbit slowing as r -> 0 (passage time near the ghost)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

BG = '#0c0c0c'
FG = '#ddd8cc'
GHOST = '#6ba3c4'    # blue for ghost/anticipatory
FOLD  = '#c8a86b'    # amber for the fold moment
POST  = '#7fad7f'    # green for post-bifurcation
DIM   = '#555050'

fig = plt.figure(figsize=(11, 3.6), facecolor=BG)
gs = GridSpec(1, 3, figure=fig, wspace=0.38, left=0.07, right=0.97, top=0.88, bottom=0.18)

# ── Panel 1: Bifurcation diagram ──────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0])
ax1.set_facecolor(BG)

r_pos = np.linspace(0, 1, 200)
ax1.plot(r_pos,  np.sqrt(r_pos), color=POST,  lw=2.2, label='stable')
ax1.plot(r_pos, -np.sqrt(r_pos), color=FOLD,  lw=2.2, linestyle='--', label='unstable')
ax1.plot(0, 0, 'o', color=POST, ms=7, zorder=5)

# Ghost zone: r < 0. No real fixed points, but show the continuation faintly.
r_neg = np.linspace(-0.8, 0, 100)
ax1.axvspan(-0.8, 0, alpha=0.06, color=GHOST, zorder=0)
ax1.plot(r_neg, np.zeros_like(r_neg), ':', color=GHOST, lw=1.2, alpha=0.55)

# Mark r_c
ax1.axvline(x=0, color=FG, lw=0.6, alpha=0.25)

ax1.set_xlim(-0.8, 1.0)
ax1.set_ylim(-1.1, 1.1)
ax1.set_xlabel('r', color=FG, fontsize=9)
ax1.set_ylabel('x*', color=FG, fontsize=9)
ax1.set_title('bifurcation diagram', color=FG, fontsize=9, pad=6)
ax1.text(-0.4, 0.85, 'ghost zone', color=GHOST, fontsize=7.5, alpha=0.75, ha='center')
ax1.text(0.55, 0.85, 'declared', color=POST, fontsize=7.5, alpha=0.75, ha='center')
ax1.text(0.02, -0.95, 'r_c', color=FG, fontsize=7.5, alpha=0.5)

for sp in ax1.spines.values():
    sp.set_color(FG); sp.set_alpha(0.2)
ax1.tick_params(colors=FG, labelsize=7)


# ── Panel 2: Vector field (x-dot vs x) at three r values ──────────────────────
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor(BG)

x_line = np.linspace(-1.4, 1.4, 400)
configs = [
    (-0.25, GHOST, 'r = −0.25  (ghost)', 4.2),
    (0,     FOLD,  'r = 0  (fold)',       2.1),
    (0.25,  POST,  'r = 0.25  (declared)', 0.0),
]

for r, color, label, offset in configs:
    xdot = r - x_line**2
    ax2.plot(x_line, xdot + offset, color=color, lw=1.8)
    ax2.axhline(y=offset, color=DIM, lw=0.5, alpha=0.4)
    # fixed / ghost points
    if r > 0:
        fp = np.sqrt(r)
        ax2.plot( fp, offset, 'o', color=color, ms=6, mfc=color, zorder=5)
        ax2.plot(-fp, offset, 'o', color=color, ms=6, mfc=BG, mew=1.6, zorder=5)
    elif r == 0:
        ax2.plot(0, offset, 'o', color=color, ms=6, mfc=BG, mew=2, zorder=5)
    else:
        # ghost fixed points at ±sqrt(-r), shown faint
        gp = np.sqrt(-r)
        ax2.plot( gp, offset, 'o', color=GHOST, ms=5, mfc=BG, mew=1.2, alpha=0.38, zorder=4)
        ax2.plot(-gp, offset, 'o', color=GHOST, ms=5, mfc=BG, mew=1.2, alpha=0.38, zorder=4)
        # bottleneck annotation
        ax2.annotate('bottleneck', xy=(0, offset - 0.28),
                     fontsize=6.5, color=GHOST, alpha=0.7, ha='center')

ax2.set_xlim(-1.45, 1.45)
ax2.set_ylim(-0.9, 5.2)
ax2.set_xlabel('x', color=FG, fontsize=9)
ax2.set_ylabel("x' + offset", color=FG, fontsize=9)
ax2.set_title('vector field', color=FG, fontsize=9, pad=6)
ax2.set_yticks([0, 2.1, 4.2])
ax2.set_yticklabels(['r=0.25', 'r=0', 'r=−0.25'], color=FG, fontsize=7)
for sp in ax2.spines.values():
    sp.set_color(FG); sp.set_alpha(0.2)
ax2.tick_params(axis='x', colors=FG, labelsize=7)


# ── Panel 3: Passage time near the ghost ──────────────────────────────────────
ax3 = fig.add_subplot(gs[2])
ax3.set_facecolor(BG)

# For x' = r - x^2 near x=0 with r < 0:
# Exact passage time from x=-L to x=+L:
#   T = integral_{-L}^{L} dx / (r - x^2)
# With r < 0 let r = -ε² → x' = -ε² - x² → T = (π/ε) regardless of L (for L large)
# Near the bottleneck: T_bottleneck ~ π / sqrt(-r)

eps_vals = np.linspace(0.02, 0.85, 400)
r_vals   = -(eps_vals**2)
T_passage = np.pi / eps_vals          # ~ 1/sqrt(-r)

ax3.plot(-r_vals, T_passage, color=GHOST, lw=2.2)
ax3.axvline(x=0, color=FOLD, lw=1.2, linestyle='--', alpha=0.7)
ax3.text(0.005, T_passage.max()*0.85, 'r_c', color=FOLD, fontsize=8, alpha=0.8)
ax3.text(0.3, 12, r'$T \sim \pi/\sqrt{-r}$', color=FG, fontsize=8.5, alpha=0.75)

ax3.set_xlim(-0.01, 0.73)
ax3.set_ylim(0, T_passage.max()*1.05)
ax3.set_xlabel('|r|   (distance from fold)', color=FG, fontsize=9)
ax3.set_ylabel('passage time T', color=FG, fontsize=9)
ax3.set_title('orbit slowing as r → r_c', color=FG, fontsize=9, pad=6)
for sp in ax3.spines.values():
    sp.set_color(FG); sp.set_alpha(0.2)
ax3.tick_params(colors=FG, labelsize=7)

# ── Figure-level caption ───────────────────────────────────────────────────────
fig.text(0.5, 0.02,
         'x\u02b9 = r \u2212 x\u00b2  ·  ghost zone: fold form present, topology not yet declared  ·  at r_c: declaration catches up',
         ha='center', va='bottom', fontsize=7.5, color=FG, alpha=0.55)

plt.savefig('assets/ghost-orbit-theory.png', dpi=150, bbox_inches='tight',
            facecolor=BG, edgecolor='none')
print("saved assets/ghost-orbit-theory.png")
