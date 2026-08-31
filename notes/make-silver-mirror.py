#!/usr/bin/env python3
"""dream figure: the ratio-strike is a mirror; its kiss is the silver ratio.

The pair-strike T(a,b)=(|b-a|, b+a) acts on the INTERVAL r=b/a as
    r -> (r+1)/(r-1)
which is an involution: two strikes restore the ratio (T^2 = id on r).
On the absolute pair, two strikes double it: T^2 = 2*Id.  So a
close-and-reopen conserves the interval and accumulates exactly one octave.
The fixed point of the ratio-strike is r = 1+sqrt(2), the silver ratio --
the interval that returns to itself (scaled by sqrt2 per strike, never
doubled, never missed).  The ladder arc {55,220}->{165,275}->{110,440}->
{330,550}->{220,880} is T^4 = 4*Id: ratio 4 at both ends, two octaves up,
the odd rungs at 5/3 the strikes that were never a landing.

Panel 1 (top): the mirror.  cents(r) vs cents((r+1)/(r-1)), the diagonal,
the 4 <-> 5/3 bounce, and the kiss at 1+sqrt(2) = 1525.9c.
Panel 2 (bottom): the lift.  Two identical ratio-4 brackets one octave
apart; the octave is the accumulated miss, and 110 is the seed.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import numpy as np

BG = '#0d0d0f'
FG = '#e8e8e8'
DIM = '#9aa0a6'
EVEN = '#6b7f99'
ODD = '#e8a33d'
CREAM = '#a9b7c6'
RED = '#d66a5a'

def cents(r):
    return 1200.0 * np.log2(r)

D = 1 + np.sqrt(2)          # silver ratio
CD = cents(D)               # 1525.86c
C53 = cents(5 / 3)          # 884.36c
C4 = cents(4)               # 2400c

fig = plt.figure(figsize=(11.4, 6.4), facecolor=BG)
gs = fig.add_gridspec(2, 1, height_ratios=[3.05, 1.15], hspace=0.34,
                      left=0.10, right=0.97, top=0.93, bottom=0.09)

# ---------------------------------------------------------------- panel 1
ax = fig.add_subplot(gs[0])
ax.set_facecolor(BG)

# diagonal
x = np.linspace(700, 2400, 400)
ax.plot(x, x, ls=(0, (4, 3)), color=DIM, lw=1.0, alpha=0.8, zorder=1)

# the ratio-strike curve y = cents((r+1)/(r-1))  -- clipped by axes
r = 2 ** (x / 1200.0)
y = cents((r + 1) / (r - 1))
ax.plot(x, y, color=CREAM, lw=2.0, zorder=2)

# orbit points: 4 <-> 5/3
for xx, yy, lab in ((C4, C53, '4  (the close)'),
                    (C53, C4, '5/3  (the odd rung)')):
    ax.plot([xx], [yy], 'o', ms=9, mfc=ODD, mec='none', zorder=5)
    ax.annotate(lab, (xx, yy), textcoords='offset points',
                xytext=(10, 6 if yy > xx else -14), fontsize=11, color=ODD)

# the bounce: a straight exchange chord 4 <-> 5/3 (the curve shows the path;
# the chord shows the exchange).  Curve is below the diagonal here, so the
# label sits above the chord in empty space.
arc = FancyArrowPatch((C4, C53), (C53, C4),
                      arrowstyle='<|-|>', mutation_scale=22,
                      lw=1.6, color=ODD, ls=(0, (3, 2)), zorder=4)
ax.add_patch(arc)
ax.text((C4 + C53) / 2, (C4 + C53) / 2 + 105, 'the strike',
        fontsize=11.5, color=ODD, ha='center', style='italic')

# the kiss: silver ratio fixed point
ax.plot([CD], [CD], 'o', ms=10, mfc=RED, mec='none', zorder=6)
ax.axvline(CD, ymin=0.05, ymax=0.98, color=RED, lw=1.1, ls=(0, (2, 2)),
           alpha=0.55, zorder=3)
ax.annotate('1+√2 = the silver kiss\n(no miss, no seed)',
            (CD, CD), textcoords='offset points', xytext=(14, 16),
            fontsize=11, color=RED)

ax.set_xlim(700, 2400)
ax.set_ylim(700, 2600)
ax.set_xlabel('interval: cents(r) of the pair at rest', color=DIM, fontsize=10.5)
ax.set_ylabel('interval after one strike: cents((r+1)/(r−1))',
              color=DIM, fontsize=10.5)
ax.tick_params(colors=DIM, labelsize=9)
for sp in ax.spines.values():
    sp.set_color(DIM); sp.set_linewidth(0.6)

ax.text(0.5, 1.10, 'the ratio-strike is a mirror', transform=ax.transAxes,
        ha='center', fontsize=14.5, color=FG, fontweight='bold')
ax.text(0.5, 1.025, 'r ↦ (r+1)/(r−1)  —  T² = id on the interval: it returns;\n'
        'the octave is what accumulates.  4 ↔ 5/3 bounce; 1+√2 is where the mirror kisses itself.',
        transform=ax.transAxes, ha='center', fontsize=9.5, color=DIM)

# ---------------------------------------------------------------- panel 2
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor(BG)

def bracket(ax2, lo, hi, y, color, lab):
    """An interval bracket from lo to hi Hz at height y."""
    ax2.plot([lo, hi], [y, y], color=color, lw=2.2, solid_capstyle='round')
    for f in (lo, hi):
        ax2.plot([f, f], [y - 0.028, y + 0.028], color=color, lw=2.2)
    ax2.text((lo + hi) / 2, y - 0.075, lab, ha='center', va='top',
             fontsize=10.5, color=color)

bracket(ax2, 55, 220, 0.30, CREAM, 'ratio 4  —  the closed register {55,220}')
bracket(ax2, 110, 440, 0.72, ODD, 'ratio 4, one octave up  —  {110,440}')

# octave lifts: 55->110 and 220->440, dashed
for f in (55, 220):
    ax2.annotate('', xy=(2 * f, 0.72), xytext=(f, 0.30),
                 arrowprops=dict(arrowstyle='-|>', color=RED, lw=1.4,
                                 ls=(0, (3, 2))))

# the seed: 110, the miss that is now the lower tone
ax2.axvline(110, color=RED, lw=1.0, ls=(0, (2, 2)), alpha=0.6)
ax2.text(110, 0.86, '110', ha='center', va='bottom', fontsize=10, color=RED)
ax2.text(0.995, 0.03, 'the octave ×2 IS the miss — one count per loop,\n'
         'and it seeds the register that follows',
         transform=ax2.transAxes, ha='right', va='bottom',
         fontsize=9.5, color=DIM)

ax2.set_xlim(30, 470)
ax2.set_ylim(0, 0.98)
ax2.set_yticks([])
ax2.set_xticks([])
for sp in ax2.spines.values():
    sp.set_visible(False)

ax2.text(0.5, 1.06, 'T⁴ = 4·Id — the ladder {55,220} → {220,880}: same interval, '
                    'two octaves up, the odd rungs never landings',
         transform=ax2.transAxes, ha='center', fontsize=10, color=FG)

plt.savefig('assets/silver-mirror.png', dpi=170, facecolor=BG,
            bbox_inches='tight')
print('wrote assets/silver-mirror.png')
