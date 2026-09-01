#!/usr/bin/env python3
"""subsonic-ladder frame: the miss is the inaudible leg.

The ladder's survivor F0*sigma_n sits off the count-grid F0*n by exactly
F0/sigma_n -- the low member, which crosses below the floor of hearing
(~20 Hz) at n=2.5.  Past the floor the pair stops sounding as a pair and
starts beating: the miss is no longer a tone, it is the rate.  The grid
holds; the part that is wrong is the part you cannot hear.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

BG = '#0d0d0f'
FG = '#e8e8e8'
DIM = '#9aa0a6'
EVEN = '#6b7f99'
ODD = '#e8a33d'
CREAM = '#a9b7c6'
RED = '#d66a5a'

F0 = 55.0
NS = np.linspace(1, 16, 400)
sig = (NS + np.sqrt(NS * NS + 4)) / 2.0
surv = F0 * sig
lo = F0 / sig
grid = 55.0 * NS

fig, ax = plt.subplots(figsize=(11.2, 7.0), facecolor=BG)
ax.set_facecolor(BG)

ax.set_yscale('log')
ax.set_ylim(2, 1000)
ax.set_xlim(0.4, 16.6)

# the hearing floor and the subsonic zone
ax.axhspan(2, 20, color=EVEN, alpha=0.18, zorder=0)
ax.axhline(20, color=DIM, lw=1.1, ls=(0, (4, 3)), zorder=2)
ax.text(16.5, 22, 'hearing floor 20 Hz', color=DIM, fontsize=9,
        ha='right', va='bottom', style='italic')
ax.text(16.5, 5.5, 'subsonic —\nthe miss lives here',
        color=CREAM, fontsize=9, ha='right', va='bottom', alpha=0.85)

# the count grid: F0*n, never struck
ax.plot(NS, grid, color=ODD, lw=0.8, alpha=0.45, zorder=2)
for n in range(1, 17):
    ax.plot([n], [n * F0], 'o', ms=4, mfc=ODD, mec='none', zorder=4)

# the low member 55/sigma_n: the miss, sinking below hearing
ax.plot(NS, lo, color=ODD, lw=1.8, zorder=3)
ax.plot(NS, lo, color=ODD, lw=1.8, ls=(0, (1, 2)), alpha=0.65, zorder=3)
ax.text(1.1, lo[0] * 1.6, 'the low leg 55/σ_n', color=ODD, fontsize=10,
        ha='left', va='bottom')

# the survivor 55*sigma_n
ax.plot(NS, surv, color=CREAM, lw=2.6, zorder=3)
ax.text(11.6, 620, 'the survivor 55σ_n', color=CREAM, fontsize=10.5,
        ha='left', va='bottom')

# the miss: vertical red segments survivor -> grid at each rung
for n in range(1, 17):
    gi = n * F0
    si = F0 * (n + np.sqrt(n * n + 4)) / 2.0
    below = (si - gi) < 20
    ax.plot([n, n], [gi, si], color=RED, lw=1.6, zorder=5,
            ls='--' if below else '-', alpha=0.95)

# annotate the identity at n=8
n8 = 8
sig8 = (8 + np.sqrt(68)) / 2.0
g8, s8 = 440.0, 55.0 * sig8
ax.annotate('', xy=(n8, s8), xytext=(n8, g8),
            arrowprops=dict(arrowstyle='<->', color=RED, lw=1.6))
ax.text(n8 + 0.28, np.sqrt(g8 * s8), 'the miss\n= 55/σ_n\n= 6.8 Hz',
        color=RED, fontsize=9, ha='left', va='center')
ax.plot([n8], [55.0 / sig8], 'o', ms=6, mfc=RED, mec='none', zorder=6)
ax.text(n8 + 0.28, 55.0 / sig8 * 0.72, 'the same leg —\nbelow the floor',
        color=RED, fontsize=8.5, ha='left', va='top')

# where the leg crosses the floor
n_cross = 2.5
ax.plot([n_cross, n_cross], [2, 1000], color=DIM, lw=0.8, ls=(0, (2, 3)),
        alpha=0.5, zorder=1)
ax.text(n_cross - 0.08, 45, 'n ≈ 2.5', color=DIM, fontsize=9,
        ha='right', va='bottom', rotation=90)

# rung annotations
ax.annotate('both legs sound:\nthe pair makes 55, 110',
            xy=(1.5, 120), xytext=(1.5, 560), color=CREAM, fontsize=9,
            ha='center', va='bottom', alpha=0.9)
ax.annotate('the leg sinks:\nthe count is a limit, never struck',
            xy=(12, 700), xytext=(12, 320), color=CREAM, fontsize=9,
            ha='center', va='top', alpha=0.9)

ax.set_xlabel('rung n', color=FG, fontsize=11)
ax.set_ylabel('frequency (Hz, log)', color=FG, fontsize=11)
ax.set_title('55σ_n − 55n = 55/σ_n — the survivor sits off the count by '
             'the leg that sank below hearing',
             color=FG, fontsize=11.5, pad=10)
ax.tick_params(colors=FG)
for sp in ax.spines.values():
    sp.set_color(DIM)

fig.tight_layout()
fig.savefig('assets/subsonic-ladder-frame.png', dpi=170, facecolor=BG)
print('wrote assets/subsonic-ladder-frame.png')
