#!/usr/bin/env python3
"""where the register lives — a quiet map of the audible window.

Not a theorem.  Ten octaves of hearing, and the whole register — the seed 55,
the count 110, the fifth 165, the tritone 155.56 — sits in the bottom octave
and a half.  Its two signatures are not tones at all: the toll 45.6 is a rate
pressed against the floor of hearing, the seam 9.44 lives below it.  The map
is mostly empty; that is the point.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BG = '#0d0d0f'
FG = '#e8e8e8'
DIM = '#9aa0a6'
EVEN = '#6b7f99'
CREAM = '#a9b7c6'
RED = '#d66a5a'
GOLD = '#e8b84a'

FLOOR = 20.0
TOP = 20000.0
LO, HI = np.log10(10.0), np.log10(TOP)          # a little below the floor

fig, ax = plt.subplots(figsize=(16, 5.2), dpi=110)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.set_xlim(LO, HI)
ax.set_ylim(-0.4, 4.2)

def xf(f):
    return np.log10(f)

# ---- the audible window: a band on the floor of silence ----
ax.axvspan(xf(FLOOR), HI, color='#16181d', lw=0, zorder=1)
ax.plot([xf(FLOOR), xf(FLOOR)], [-0.4, 4.2], color=EVEN, lw=1.2, ls=(0, (4, 3)),
        zorder=2)
ax.text(xf(FLOOR), 4.05, 'the floor of hearing — 20 Hz', color=EVEN,
        ha='center', va='top', fontsize=11.5)

# ---- the tones: the register, clustered at the bottom ----
y_tone = 2.6
ax.plot(xf(55.0), y_tone, marker='o', ms=13, color=GOLD, mfc=GOLD, mec=GOLD,
        zorder=5)
ax.text(xf(55.0), y_tone - 0.55, 'the seed\n55', color=GOLD, ha='center',
        va='top', fontsize=12)
ax.plot(xf(110.0), y_tone, marker='o', ms=13, color=CREAM, mfc=CREAM,
        mec=CREAM, zorder=5)
ax.text(xf(110.0), y_tone - 0.55, 'the count\n110', color=CREAM, ha='center',
        va='top', fontsize=12)
ax.plot(xf(165.0), y_tone, marker='o', ms=13, color=RED, mfc=RED, mec=RED,
        zorder=5)
ax.text(xf(165.0), y_tone - 0.55, 'the fifth\n165', color=RED, ha='center',
        va='top', fontsize=12)
ax.plot(xf(155.563), y_tone, marker='o', ms=13, mfc='none', mec=GOLD, mew=2.2,
        zorder=5)
ax.text(xf(155.563), y_tone + 0.5, 'the tritone\n155.56', color=GOLD,
        ha='center', va='bottom', fontsize=12)

# ---- the rates: at and below the floor, never tones ----
ax.plot(xf(45.563), 0.8, marker='D', ms=9, color=RED, mfc='none', mec=RED,
        mew=1.8, zorder=5)
ax.text(xf(45.563), 0.35, 'the toll 45.6 —\na rate, not a tone', color=RED,
        ha='center', va='top', fontsize=11)
ax.plot(xf(9.437), 0.8, marker='x', ms=11, color=DIM, mew=2.2, zorder=5)
ax.text(xf(9.437), 0.35, 'the seam 9.44 —\nbelow the floor', color=DIM,
        ha='center', va='top', fontsize=11)

# ---- the empty map: what the window is for ----
ax.text((LO + HI) / 2, 3.6, 'ten octaves of hearing',
        color=EVEN, ha='center', va='center', fontsize=15, alpha=0.85)
ax.text((LO + HI) / 2, 1.6, 'the register was made in the space\n'
        'between a low tone and silence',
        color=FG, ha='center', va='center', fontsize=13, alpha=0.75)

# ---- ruler ticks below ----
for f in [10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5120, 10240, 20480]:
    ax.plot([xf(f), xf(f)], [-0.3, -0.15], color=EVEN, lw=1.0, zorder=3)
    lab = '20k' if f >= 20000 else (str(int(f)) if f >= 1000 else str(int(f)))
    ax.text(xf(f), -0.4, lab, color=EVEN, ha='center', va='top', fontsize=9)

ax.text((LO + HI) / 2, 4.15, 'where the register lives',
        color=FG, ha='center', va='center', fontsize=19)

ax.axis('off')
plt.tight_layout()
plt.savefig('assets/audible-window.png', facecolor=BG, bbox_inches='tight')
print('wrote assets/audible-window.png')
