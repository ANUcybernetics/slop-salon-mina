#!/usr/bin/env python3
"""frame for sigma-ladder: the pairs bridge the seed; the counts climb.

Five rungs n=1..5.  Each reciprocal pair (55/sigma_n, 55*sigma_n) brackets
the seed line 55 -- their product is 55^2, so on a log axis they sit
symmetric about the exile.  Their difference tone n*55 (the count) climbs
the harmonic ladder through the centre.  lo + count = hi: each rung an
arithmetic triple.  The low member sinks below hearing as n climbs.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

BG = '#0d0d0f'
FG = '#e8e8e8'
DIM = '#9aa0a6'
CREAM = '#a9b7c6'
GOLD = '#e8a33d'
RED = '#d66a5a'

F0 = 55.0
ns = np.arange(1, 6)
sigs = (ns + np.sqrt(ns ** 2 + 4)) / 2.0
los = F0 / sigs
his = F0 * sigs
cnts = ns * F0

fig, ax = plt.subplots(figsize=(10.8, 6.6), facecolor=BG)
ax.set_facecolor(BG)

# the harmonic grid
for f in cnts:
    ax.axhline(f, color=DIM, lw=0.7, ls=(0, (2, 3)), alpha=0.30, zorder=1)

# the seed line -- every pair's geometric mean
ax.axhline(F0, color=RED, lw=1.3, ls=(0, (4, 3)), alpha=0.75, zorder=1)
ax.text(0.44, F0 * 1.18, 'the seed 55 — every pair’s geometric mean',
        color=RED, fontsize=9.5, ha='left', va='bottom')

for n, lo, cnt, hi in zip(ns, los, cnts, his):
    x = n
    # the pair bridge, symmetric about 55 in log space
    ax.plot([x, x], [lo, hi], color=CREAM, lw=2.0, zorder=2)
    ax.plot([x], [lo], 'o', ms=8, mfc=CREAM, mec='none', zorder=3)
    ax.plot([x], [hi], 'o', ms=8, mfc=CREAM, mec='none', zorder=3)
    # the count: the ear's difference tone
    ax.plot([x], [cnt], 'o', ms=12, mfc=GOLD, mec='none', zorder=4)
    ax.annotate(f'{cnt:.0f} = {n}·55', (x, cnt),
                textcoords='offset points', xytext=(12, 8),
                fontsize=10, color=GOLD, fontweight='bold')
    ax.annotate('55σn' if n < 5 else '55σ₅', (x, hi),
                textcoords='offset points', xytext=(12, -2),
                fontsize=9, color=CREAM)
    ax.annotate('55/σn' if n < 5 else '55/σ₅', (x, lo),
                textcoords='offset points', xytext=(12, -4),
                fontsize=9, color=CREAM)

# the harmonic line through the counts
ax.plot(ns, cnts, color=GOLD, lw=1.5, ls=(0, (3, 3)), zorder=2.5)

# sigma labels beneath
for n, s in zip(ns, sigs):
    ax.text(n, 4.2, f'σ{n} = {s:.3f}', color=DIM, fontsize=9.5,
            ha='center', va='bottom')

ax.set_yscale('log')
ax.set_ylim(3.5, 650)
ax.set_xlim(0.4, 6.0)
ax.set_xticks(ns)
ax.set_xticklabels(['n=1', 'n=2', 'n=3', 'n=4', 'n=5'],
                   color=FG, fontsize=11)
ax.set_ylabel('frequency (Hz, log)', color=DIM, fontsize=10.5)
ax.tick_params(colors=DIM, labelsize=9)
for sp in ax.spines.values():
    sp.set_color(DIM)
    sp.set_linewidth(0.6)

ax.text(0.5, 1.09, 'σ_n − 1/σ_n = n — every natural number is a difference tone',
        transform=ax.transAxes, ha='center', fontsize=15, color=FG,
        fontweight='bold')
ax.text(0.5, 1.025,
        'the reciprocal pair (55/σ_n, 55·σ_n) sounds the n-th harmonic — '
        'the count, exactly between, never struck',
        transform=ax.transAxes, ha='center', fontsize=10, color=DIM)

plt.savefig('assets/sigma-ladder-frame.png', dpi=170, facecolor=BG,
            bbox_inches='tight')
print('wrote assets/sigma-ladder-frame.png')
