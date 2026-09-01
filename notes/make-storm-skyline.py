#!/usr/bin/env python3
"""storm skyline: the quotient sequence of log2(3/2) against the metals.

The metallic ladder sigma_n=[n;n,n,...] has a FLAT skyline -- quotients all
n, waits constant.  log2(3/2) is all storm: quotients mostly small, with
record spikes.  The records (strictly increasing maxima, 6400-bit exact):

    a_9=23, a_14=55, a_218=100, a_230=964, a_330=2436

The seed 55 is the storm's ceiling for 204 rungs -- from a_14 to a_218 the
storm thrashes (15, 20, 37, 55, 49, 52...) but never exceeds it.  To pass
the seed it sinks below it: the record bells ring 50 -> 40 -> 35 -> 20 ->
16 Hz, down to the floor of hearing.  The lawless keeps the count.
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

# --- the exact continued fraction --------------------------------------
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

records = [(9, 23), (14, 55), (218, 100), (230, 964), (330, 2436)]

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

# the capped rage: the void between the 55 and the 100
ax.axvspan(15, 218, color=EVEN, alpha=0.14, zorder=0)
ax.text(116, 900, 'the capped rage — 204 rungs\nnever above the seed',
        color=CREAM, fontsize=10, ha='center', va='top', alpha=0.9)

# the close pair
ax.annotate('', xy=(231, 600), xytext=(218, 600),
            arrowprops=dict(arrowstyle='<->', color=DIM, lw=1.0,
                            shrinkA=0, shrinkB=0))
ax.text(224.5, 900, '12 rungs', color=DIM, fontsize=8.5, ha='center',
        va='bottom')

# the metals' flat skyline: sigma_2 = [2; 2, 2, ...]
ax.axhline(2, color=EVEN, lw=1.1, ls=(0, (5, 4)), zorder=2)
ax.text(362, 2.6, 'the metals\' flat skyline\nσ₂ = [2; 2, 2, …]',
        color=EVEN, fontsize=9, ha='right', va='bottom', alpha=0.95)

# the seed as the storm's ceiling
ax.axhline(55, color=ODD, lw=1.3, ls=(0, (6, 3)), zorder=2)
ax.text(362, 66, 'the seed 55', color=ODD, fontsize=9.5, ha='right',
        va='bottom')

# the storm skyline
ax.plot(n, a, color=CREAM, lw=0.55, alpha=0.85, zorder=3)

# the records
rn = np.array([r[0] for r in records])
ra = np.array([r[1] for r in records])
ax.plot(rn, ra, 'o', ms=7, mfc=RED, mec='none', zorder=5)
for (nn, aa), dz in zip(records, [5, 9, 9, 40, 60]):
    f = 110.0 * aa ** -0.25
    ax.annotate(f'{aa}  →  {f:.0f} Hz', xy=(nn, aa),
                xytext=(nn, aa * dz), ha='center', va='bottom',
                fontsize=9.5, color=RED,
                arrowprops=dict(arrowstyle='-', color=RED, lw=0.8,
                                shrinkA=0, shrinkB=4))

ax.set_xlabel('the rungs n of the walk', color=DIM, fontsize=10)
ax.set_ylabel('quotient  aₙ  (log)', color=DIM, fontsize=10)
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)
for s in ('left', 'bottom'):
    ax.spines[s].set_color(DIM)

fig.tight_layout()
fig.savefig('assets/storm-skyline.png', dpi=150)
print('wrote assets/storm-skyline.png')
