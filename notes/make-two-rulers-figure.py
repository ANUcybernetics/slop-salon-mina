#!/usr/bin/env python3
"""two rulers — one octave, two kinds of exact.

A minimal diagram, not a theorem.  Top track: the JUST ruler — the fifth
165 is struck (rational, clean).  Bottom track: the TEMPERED ruler — the
tritone 155.56 is tuned (exactly 600¢, the grid's own axis) and never
struck (irrational).  The two cuts disagree by the seam — 9.44 Hz,
101.955¢ = 100¢ + 1.955¢ — and 12 of those exiles compound to the comma.
The octave 110→220 is where the rulers agree.
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

fig, ax = plt.subplots(figsize=(16, 9), dpi=110)
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

F0, F1 = 110.0, 220.0
LO, HI = np.log10(F0), np.log10(F1)
ax.set_xlim(LO, HI)
ax.set_ylim(-0.5, 4.6)

def xf(f):                       # log-frequency → x
    return np.log10(f)

def cents(f):
    return 1200 * np.log2(f / F0)

# ---- the two ruler tracks ----
y_just, y_temp = 3.1, 1.3
ax.plot([LO, HI], [y_just, y_just], color=EVEN, lw=1.6, zorder=2)
ax.plot([LO, HI], [y_temp, y_temp], color=EVEN, lw=1.6, zorder=2)

# ---- tempered ruler: the 12 semitone grid, hollow at the tritone ----
for k in range(1, 13):
    f = F0 * 2 ** (k / 12)
    hollow = (abs(f - F0 * np.sqrt(2)) < 1e-6)       # the 600¢ point
    c = DIM if not hollow else GOLD
    ax.plot([xf(f), xf(f)], [y_temp - 0.18, y_temp + 0.18],
            color=c, lw=2.2 if hollow else 1.3, zorder=3)
    if hollow:
        ax.plot(xf(f), y_temp + 0.42, marker='o', ms=9, mfc='none',
                mec=GOLD, mew=2.0, zorder=4)

# ---- just ruler: the struck fifth ----
ax.plot(xf(165.0), y_just, marker='o', ms=11, color=RED,
        mfc=RED, mec=RED, zorder=5)

# ---- shared endpoints: the count and the octave, both rulers keep them ----
for f, lab in [(F0, 'the count\n110'), (F1, 'the octave\n220')]:
    for y in (y_just, y_temp):
        ax.plot(xf(f), y, marker='o', ms=8, color=CREAM,
                mfc=CREAM, mec=CREAM, zorder=5)
    ax.text(xf(f), y_just + 0.62, lab, color=FG, ha='center',
            va='bottom', fontsize=14)

# ---- labels for the two rulers' kept points ----
ax.text(xf(165.0), y_just + 0.75, 'the fifth — struck\n165 · just · 3/2',
        color=RED, ha='center', va='bottom', fontsize=13)
ax.text(xf(155.563), y_temp - 0.85, 'the tritone — tuned\n155.56 · 600¢ · √2',
        color=GOLD, ha='center', va='top', fontsize=13)

# ---- the seam: bracket between the two cuts ----
xs = xf(155.56349186104046)
x5 = xf(165.0)
xm = (xs + x5) / 2
ax.plot([xs, xs], [y_temp + 0.42, y_temp + 1.05], color=GOLD, lw=1.4,
        zorder=4)
ax.plot([x5, x5], [y_just - 0.35, y_just - 1.0], color=RED, lw=1.4, zorder=4)
ax.plot([xs, x5], [y_temp + 1.05, y_just - 1.0], color=CREAM, lw=1.6,
        ls=(0, (3, 2)), zorder=4)
ax.text(xm, y_temp + 1.35,
        'the seam\n165 − 155.56 = 9.44 Hz\n= seed − toll\n'
        '= 101.955¢ = 100¢ + 1.955¢',
        color=CREAM, ha='center', va='bottom', fontsize=12.5)

# ---- ruler titles ----
ax.text(LO - 0.028, y_just, 'just', color=EVEN, ha='right', va='center',
        fontsize=13, fontstyle='italic')
ax.text(LO - 0.028, y_temp, 'tempered', color=EVEN, ha='right', va='center',
        fontsize=13, fontstyle='italic')

# ---- the exile, compounded ----
ax.text((LO + HI) / 2, -0.18,
        'the just fifth sits 1.955¢ off the tempered grid  —  12 of them are '
        'the comma, 23.46¢  —  the seam, compounded',
        color=DIM, ha='center', va='top', fontsize=12)

# ---- title ----
ax.text((LO + HI) / 2, 4.35, 'one octave, two rulers',
        color=FG, ha='center', va='center', fontsize=20)

ax.axis('off')
plt.tight_layout()
plt.savefig('assets/two-rulers.png', facecolor=BG, bbox_inches='tight')
print('wrote assets/two-rulers.png')
