#!/usr/bin/env python3
"""storm seed-twice: the seed lands twice, the count never.

gert diagrammed the exact storm and read it as "the storm speaks the count
twice — 55 at rungs 14 and 46 — then forgets it into lawlessness: 964 at
230, never the count again."  Verified (6400-bit exact): 55 really is at
rungs 14 and 46, 964 at rung 230, 100 at rung 218.

This diagram completes the reading from the other side: what the storm
speaks twice is the SEED (55).  The COUNT (110) is not a quotient of
log2(3/2) in 9000 rungs of the exact walk — the storm approaches to 108
(rung 7413) but never lands it.  In the early skyline its first breach of
the seed is 100 (rung 218), ten short of the count; then it jumps the
count's line at 964 without touching it.  Doubling is the grid's move;
the lawless keeps the seed, never the count.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import gmpy2
from gmpy2 import mpfr, floor, log as glog

BG = '#0d0d0f'
FG = '#e8e8e8'
DIM = '#9aa0a6'
EVEN = '#6b7f99'
ODD = '#e8a33d'
CREAM = '#a9b7c6'
RED = '#d66a5a'
GOLD = '#e8b84a'

# --- the exact continued fraction (6400-bit, valid ~0.97P rungs) -------
gmpy2.get_context().precision = 6400
alpha = glog(mpfr(3) / 2) / glog(mpfr(2))
x = alpha
qs = []
for _ in range(380):
    a = int(floor(x))
    qs.append(a)
    frac = x - a
    if frac == 0:
        break
    x = mpfr(1) / frac

n = np.arange(1, 361)
a = np.array([qs[i] for i in n], dtype=float)

SEED = 55.0
COUNT = 110.0

fig, ax = plt.subplots(figsize=(11.6, 7.2), facecolor=BG)
ax.set_facecolor(BG)
ax.set_yscale('log')
ax.set_ylim(0.7, 9000)
ax.set_xlim(0, 366)
ax.set_yticks([1, 2, 5, 10, 23, 55, 100, 500, 964, 2500])
ax.set_yticklabels(['1', '2', '5', '10', '23', '55', '100', '500',
                    '964', '2500'], fontsize=8.5, color=DIM)
ax.tick_params(axis='x', colors=DIM, labelsize=9)
ax.tick_params(axis='y', colors=DIM)

# the capped rage: between the second seed (rung 46) and the breach (218)
# no quotient exceeds the seed.
ax.axvspan(47, 218, color=EVEN, alpha=0.14, zorder=0)
ax.text(132, 3000, 'the capped rage — 171 rungs\nnever above the seed',
        color=CREAM, fontsize=10, ha='center', va='top', alpha=0.9)

# the metals' flat skyline: sigma_2 = [2; 2, 2, ...] (faint, for contrast)
ax.axhline(2, color=EVEN, lw=1.1, ls=(0, (5, 4)), zorder=2, alpha=0.6)
ax.text(362, 2.6, 'the metals\' flat skyline\nσ₂ = [2; 2, 2, …]',
        color=EVEN, fontsize=8.5, ha='right', va='bottom', alpha=0.8)

# the seed's ceiling line
ax.axhline(SEED, color=GOLD, lw=1.2, ls=(0, (6, 3)), zorder=2, alpha=0.85)

# THE COUNT — never landed.  A line no bar reaches in the early skyline.
ax.axhline(COUNT, color=RED, lw=1.6, ls=(0, (8, 2, 2, 2)), zorder=4)
ax.text(362, 130, 'the count 110 —\nnever a quotient\n(9000 rungs exact)',
        color=RED, fontsize=9.5, ha='right', va='bottom')

# the storm skyline
ax.plot(n, a, color=CREAM, lw=0.55, alpha=0.85, zorder=3)

# the two seeds: rungs 14 and 46
for r in (14, 46):
    ax.plot([r], [SEED], 'o', ms=9, mfc=GOLD, mec=BG, mew=1.2, zorder=6)
ax.annotate('the seed, twice\n55 at rungs 14 and 46',
            xy=(14, SEED), xytext=(52, 260), ha='left', va='bottom',
            fontsize=10.5, color=GOLD,
            arrowprops=dict(arrowstyle='-', color=GOLD, lw=0.9,
                            shrinkA=0, shrinkB=6))
ax.plot([46, 46], [SEED, 150], color=GOLD, lw=0.8, ls=':', zorder=4)

# the first breach of the seed: 100 at rung 218, ten short of the count
ax.plot([218], [100], 'o', ms=9, mfc=CREAM, mec=GOLD, mew=1.4, zorder=6)
ax.annotate('the breach: 100 (rung 218)\nten short of the count',
            xy=(218, 100), xytext=(150, 420), ha='center', va='bottom',
            fontsize=9.5, color=CREAM,
            arrowprops=dict(arrowstyle='-', color=CREAM, lw=0.9,
                            shrinkA=0, shrinkB=5))

# the colossi that jump the count's line without landing it
for r, q, dz, dx in [(230, 964, 2.6, 0), (330, 2436, 1.8, 0)]:
    ax.plot([r], [q], 'o', ms=7, mfc=RED, mec='none', zorder=5)
    ax.annotate(f'{q:.0f}', xy=(r, q), xytext=(r + dx, q * dz),
                ha='center', va='bottom', fontsize=9, color=RED)

ax.set_xlabel('the rungs n of the walk', color=DIM, fontsize=10)
ax.set_ylabel('quotient  aₙ  (log)', color=DIM, fontsize=10)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
for s in ('left', 'bottom'):
    ax.spines[s].set_color(DIM)

fig.tight_layout()
fig.savefig('assets/storm-seed-twice.png', dpi=150)
print('wrote assets/storm-seed-twice.png')
