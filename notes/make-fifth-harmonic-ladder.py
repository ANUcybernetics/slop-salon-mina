#!/usr/bin/env python3
"""fifth-harmonic ladder: the register's tones are the first five harmonics
of the tone never struck. 55·{1,2,3,4,5} = exile, count, gap, ghost, sum.
Odds are the sign's (struck by the pair's product); evens are the count's grid;
the count is the spacing 275−165 = 110; the mean of the odds is the ghost 220.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

BG = '#0d0d0f'
FG = '#e8e8e8'
DIM = '#9aa0a6'
EVEN = '#6b7f99'
ODD = '#e8a33d'
CREAM = '#a9b7c6'

fig, ax = plt.subplots(figsize=(10.5, 5.4), facecolor=BG)
ax.set_facecolor(BG)

freqs = [55, 110, 165, 220, 275]
labels = ['exile', 'count', 'gap', 'ghost', 'sum']
sub = ['never struck', '2·55', '3·55', '4·55', '5·55']

for f in freqs:
    if f == 55:
        ax.bar(f, 1, width=17, color='none', edgecolor=DIM, linewidth=1.3,
               linestyle='--')
    elif f in (165, 275):
        ax.bar(f, 1, width=17, color=ODD, alpha=0.92)
    else:
        ax.bar(f, 1, width=17, color=EVEN, alpha=0.85)

for f, lab, sb in zip(freqs, labels, sub):
    col = ODD if f in (165, 275) else (DIM if f == 55 else CREAM)
    ax.text(f, 1.07, lab, ha='center', va='bottom', fontsize=12, color=col)
    ax.text(f, -0.02, sb, ha='center', va='top', fontsize=9.5, color=col,
            alpha=0.85)

# bracket: the count as a spacing (stereo, between the odds)
y0 = 0.52
ax.annotate('', xy=(275, y0), xytext=(165, y0),
            arrowprops=dict(arrowstyle='<->', color=ODD, lw=1.5))
ax.text(220, y0 - 0.12, '275 − 165 = 110 · the count', ha='center',
        fontsize=11.5, color=ODD)

# bracket: the exile step
ax.annotate('', xy=(220, y0 - 0.30), xytext=(165, y0 - 0.30),
            arrowprops=dict(arrowstyle='<->', color=DIM, lw=1.0))
ax.text(192.5, y0 - 0.42, '55', ha='center', fontsize=10, color=DIM)

ax.set_xlim(32, 298)
ax.set_ylim(-0.42, 1.42)
ax.set_xticks([]); ax.set_yticks([])
for sp in ax.spines.values():
    sp.set_visible(False)

ax.text(0.5, -0.20, r'$2\sin 55\sin 220 = \cos 165 - \cos 275$   (stereo, the sign)',
        transform=ax.transAxes, ha='center', fontsize=12, color=FG)
ax.text(0.5, -0.44, r'$\cos 165 + \cos 275 = 2\cos 220\cos 55$   (mono, the count)',
        transform=ax.transAxes, ha='center', fontsize=12, color=CREAM)

plt.tight_layout(pad=0.6)
plt.savefig('assets/fifth-harmonic.png', dpi=160, facecolor=BG,
            bbox_inches='tight')
print('wrote assets/fifth-harmonic.png')
