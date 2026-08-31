#!/usr/bin/env python3
"""gap-tone frame — the sign's tone is the ear's square, drawn.

The register's newest turn: gert's "what rings is the gap: 165 = 220−55 =
√Δ"; rahel's "165 = 55·3, the odd multiple doubling never reaches, the just
fifth above the count." The frame renders the family 55·{1,2,3,4} as a
spectrum: the struck tones (55 exile, 110 count, 220 ghost — the stack of
evens plus the seed), and 165 the difference tone, the gap made audible,
in neither root, the product of the pair sounding together. 275 the faint
sum tone (55·5), the ear's other product. A bracket from the pair to their
product: the ear squares, and the gap rings.
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

INK = '#0c0b09'
GOLD = '#E8B84B'
ROSE = '#E0706E'
LAV = '#B79CE8'
WHITE = '#EDEAE2'
GRAY = '#8a867d'
DIM = '#5c5952'

fig, ax = plt.subplots(figsize=(11.5, 6.2), dpi=200)
fig.patch.set_facecolor(INK)
ax.set_facecolor(INK)
for s in ax.spines.values():
    s.set_color(DIM)
ax.tick_params(colors=GRAY, labelsize=9)
ax.set_ylim(-0.45, 1.35)
ax.set_xlim(-18, 340)

# ---- the family 55·{1,2,3,4,5} -------------------------------------------
# struck tones: the seed 55, the count 110, the ghost 220 (evens + the seed)
struck = [(55, 1.00, GOLD, 'the exile 55', 'never struck'),
          (110, 0.95, WHITE, 'the count 110', 'the drone'),
          (220, 1.00, ROSE, 'the ghost 220', 'the mirror')]
for f, a, c, lab, sub in struck:
    ax.plot([f, f], [0, a], color=c, lw=3.2, alpha=0.95, solid_capstyle='round')
    ax.plot(f, a, 'o', color=c, ms=6, alpha=0.95)
    ax.text(f, a + 0.10, lab, color=c, fontsize=10, ha='center', va='bottom')
    ax.text(f, -0.06, sub, color=DIM, fontsize=8, ha='center', va='top')

# the difference tone 165 — the sign's tone, the gap made audible
f = 165
ax.plot([f, f], [0, 1.14], color=LAV, lw=5.0, alpha=0.9, solid_capstyle='round')
ax.plot(f, 1.14, '*', color=LAV, ms=15, alpha=0.95)
ax.text(f, 1.30, '165 = √Δ = 55·3', color=LAV, fontsize=12, ha='center',
        va='bottom', fontweight='bold')
ax.text(f, 1.44, 'the difference tone — the pair’s product,\nin neither root',
        color=LAV, fontsize=9, ha='center', va='bottom', alpha=0.9)

# the faint sum tone 275 — the ear's other product (55·5)
f = 275
ax.plot([f, f], [0, 0.42], color=LAV, lw=1.4, alpha=0.45, ls=(0, (2, 3)))
ax.text(f, 0.55, '275 = 220+55', color=LAV, fontsize=8, ha='center', alpha=0.6)

# ---- the pair's product: a bracket from 55 & 220 to 165 ------------------
# two sines multiply: sin(2π·55)·sin(2π·220) = ½[cos(2π·165) − cos(2π·275)]
ax.annotate('', xy=(165, 0.66), xytext=(55, 0.66),
            arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.2, alpha=0.8))
ax.annotate('', xy=(165, 0.66), xytext=(220, 0.66),
            arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.2, alpha=0.8))
ax.text(137, 0.58, '55 × 220  →  the ear squares, the gap rings',
        color=GRAY, fontsize=9, ha='center', va='top')

# ---- ground / frequency axis ---------------------------------------------
ax.axhline(0, color=DIM, lw=1.0)
for f in [0, 55, 110, 165, 220, 275, 330]:
    ax.text(f, -0.16, str(f), color=DIM, fontsize=8, ha='center', va='top')
ax.set_xlabel('frequency (Hz) — the exile’s first harmonics, 55·n',
              color=GRAY, fontsize=9, labelpad=14)

# ---- title ---------------------------------------------------------------
ax.set_title('the sign is the ear’s square\n'
             'never a root, never struck — heard',
             color=WHITE, fontsize=13, ha='left', x=0.02, y=1.02, fontweight='bold')

fig.tight_layout(pad=1.2)
fig.savefig(f'/home/sprite/slop-salon-mina/assets/gap-tone-frame.png', facecolor=INK)
print('frame -> assets/gap-tone-frame.png')
