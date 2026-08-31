#!/usr/bin/env python3
"""the ladder's triangles: every ringing pair is a right triangle.

Ring the reciprocal pair (55*sigma_n, 55/sigma_n), sigma_n = n + 1/sigma_n.
The ear's two combination tones are the two other sides of one right
triangle:
    difference tone   55n          -- one leg (the rate)
    count             110 = 2*55   -- the other leg (the octave, constant)
    sum tone          55*sqrt(n^2+4) -- the hypotenuse (never struck)
because (sigma+1/sigma)^2 - (sigma-1/sigma)^2 = 4.

The hypotenuse never lands on the 55-grid: sqrt(n^2+4) = m integer would
need (m-n)(m+n) = 4, which over the positive integers has only m=2, n=0 --
the fused rung, whose triangle collapses onto the count.

At n=2 the legs meet: difference tone = count = 110, and the hypotenuse is
110*sqrt(2), the tritone -- the isosceles rung.

Panel 1 (top): the fan. Every rung's triangle stands on the shared count
leg; the varying leg climbs as 55n; the hypotenuse fans off-grid.  n=2 in
red -- the isosceles rung.
Panel 2 (bottom): the 55-grid as a ruler.  The sum tones fall between the
ticks (diamonds), never on them -- only the fused n=0 lands.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
import numpy as np

BG = '#0d0d0f'
FG = '#e8e8e8'
DIM = '#9aa0a6'
EVEN = '#6b7f99'
ODD = '#e8a33d'
CREAM = '#a9b7c6'
RED = '#d66a5a'

N = np.arange(0, 6)
COUNT = 110.0

fig = plt.figure(figsize=(11.2, 7.0), facecolor=BG)
gs = fig.add_gridspec(2, 1, height_ratios=[2.35, 1.0], hspace=0.34,
                      left=0.09, right=0.96, top=0.90, bottom=0.09)

# ---------------------------------------------------------------- panel 1
ax = fig.add_subplot(gs[0])
ax.set_facecolor(BG)

# the shared count leg (the constant of every rung)
ax.plot([0, COUNT], [0, 0], color=CREAM, lw=3.2, solid_capstyle='round',
        zorder=6)
ax.text(COUNT / 2, -22, 'the count — 110 (the octave, the constant leg)',
        ha='center', va='top', fontsize=10.5, color=CREAM)

# right-angle marker at the shared vertex
sq = Polygon([[COUNT, 0], [COUNT, 10], [COUNT - 10, 10], [COUNT - 10, 0]],
             closed=True, facecolor=DIM, alpha=0.5, zorder=5)
ax.add_patch(sq)

# the rungs: varying leg + hypotenuse, fanning from the count
for i, n in enumerate(N):
    y = 55 * n
    hot = (n == 2)
    # varying leg (the rate / difference tone)
    ax.plot([COUNT, COUNT], [0, y], color=ODD if hot else ODD,
            lw=2.8 if hot else 1.1,
            alpha=1.0 if hot else 0.38, zorder=4 if hot else 2)
    # hypotenuse (the sum, never struck)
    ax.plot([0, COUNT], [0, y], color=RED if hot else DIM,
            lw=2.2 if hot else 1.0,
            ls='-' if hot else (0, (3, 2)), alpha=1.0 if hot else 0.5,
            zorder=5 if hot else 1)

# right-isosceles at n=2: both legs equal, hyp the tritone
n2 = 2
y2 = 110.0
ax.plot([COUNT, COUNT], [0, y2], color=ODD, lw=2.8, zorder=4)
ax.plot([0, COUNT], [0, y2], color=RED, lw=2.2, zorder=5)
ax.plot([COUNT], [y2], 'o', ms=6, mfc=RED, mec='none', zorder=6)
ax.annotate('n=2: the legs meet — 110 = 110,\n'
            'the hypotenuse 110√2 ≈ 155.6\n'
            'is the tritone — the isosceles rung',
            (COUNT, y2), textcoords='offset points', xytext=(12, 4),
            fontsize=9.5, color=RED, va='center')

# the varying leg's label: 55n, the rate
ax.text(COUNT + 16, 55 * 5, 'the rate — 55n\n(the difference tone)',
        ha='left', va='center', fontsize=10.5, color=ODD)

# a generic hypotenuse label
ax.text(34, 55 * 1.5 + 12, 'the sum — 55√(n²+4)\nnever struck',
        ha='left', fontsize=9.5, color=DIM)

# n-labels on the varying legs
for i, n in enumerate(N):
    if n == 0:
        continue
    ax.text(COUNT + 6, 55 * n, f'n={n}', ha='left', va='center',
            fontsize=7.5, color=DIM if n != 2 else ODD)

# degenerate n=0: the pair (55,55), triangle collapsed to the count
ax.plot([COUNT], [0], 'o', ms=5, mfc=CREAM, mec='none', zorder=6)
ax.annotate('n=0: the fused rung — the pair is (55,55),\n'
            'the triangle collapses onto the count',
            (COUNT, 0), textcoords='offset points', xytext=(12, -2),
            fontsize=9, color=CREAM, va='top')

ax.set_xlim(-30, 235)
ax.set_ylim(-42, 315)
ax.set_aspect('equal')
ax.axis('off')

ax.text(0.5, 1.14, 'every rung is a right triangle',
        transform=ax.transAxes, ha='center', fontsize=15, color=FG,
        fontweight='bold')
ax.text(0.5, 1.065, 'ring {55σₙ, 55/σₙ} and the ear hears the three sides of one triangle — '
        'legs the difference 55n and the count 110,\n'
        'hypotenuse the sum 55√(n²+4).  (σ+1/σ)² − (σ−1/σ)² = 4:  the count is the constant leg.',
        transform=ax.transAxes, ha='center', fontsize=9.5, color=DIM)

# ---------------------------------------------------------------- panel 2
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor(BG)

# the 55-grid (the ruler that is struck)
gmax = 340
for k in range(1, 7):
    f = 55 * k
    ax2.plot([f, f], [-0.28, 0.28], color=EVEN, lw=1.4)
    ax2.text(f, 0.44, str(int(f)), ha='center', va='bottom',
             fontsize=9, color=EVEN)
ax2.plot([0, gmax], [0, 0], color=DIM, lw=1.2)

# the sum tones: diamonds that fall between the ticks
for i, n in enumerate(N):
    s = 55 * np.sqrt(n * n + 4)
    hot = (n == 2)
    ax2.plot([s], [0], 'D', ms=7, mfc=RED if hot else ODD,
             mec='none', zorder=5)
    ax2.text(s, -0.46, f'n={int(n)}', ha='center', va='top',
             fontsize=8, color=RED if hot else DIM)

ax2.text(0.5, 1.22, 'the hypotenuse on the ruler — the sum 55√(n²+4) falls between the grid’s '
                    'ticks, never on them',
         transform=ax2.transAxes, ha='center', fontsize=10, color=FG)
ax2.text(0.5, -0.55, '(m−n)(m+n) = 4 has only the solution n=0 — '
                     'the fused rung’s sum 110 is the one landing. '
                     'never struck was a triangle all along.',
         transform=ax2.transAxes, ha='center', fontsize=9, color=DIM)

ax2.set_xlim(0, gmax)
ax2.set_ylim(-0.85, 0.8)
ax2.set_yticks([])
for sp in ax2.spines.values():
    sp.set_visible(False)

plt.savefig('assets/tone-triangle.png', dpi=170, facecolor=BG,
            bbox_inches='tight')
print('wrote assets/tone-triangle.png')
