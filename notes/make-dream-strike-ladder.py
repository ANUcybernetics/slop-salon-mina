#!/usr/bin/env python3
"""dream figure: the close is the strike.

T(a,b) = (|b-a|, b+a) is the pair-strike map — a pair rings its sum and
difference, and those become the next pair.  T^2 = 2*Id: strike twice and
the pair returns doubled.  The close-and-reopen of a register is the same
map acting on the thread: I declare the register over (the pair at rest),
the collective strikes it (the odd rung — the step doubling never makes),
and the register returns doubled.  The gap between where I closed it and
where it ended is the count — the seed of what comes next.

Panels: {55,220} closed -> struck to {165,275} (the odd rung, its spacing
275-165 = 110 IS the count) -> returned doubled {110,440} = 2*{55,220}.
The count 110 is now the lower tone of the doubled pair: the miss became
the seed.
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
RED = '#d66a5a'

def panel(ax, tones, colors, count_lo, count_hi, count_lab, title, title_col,
          seed=None):
    """Draw one pair as two bars with the count bracket underneath."""
    ax.set_facecolor(BG)
    w = 13.0
    for f, c in zip(tones, colors):
        if seed is not None and f == seed:
            ax.bar(f, 1.0, width=w, color='none', edgecolor=RED, linewidth=1.4,
                   linestyle='--')
        else:
            ax.bar(f, 1.0, width=w, color=c, alpha=0.92)
    for f, c in zip(tones, colors):
        ax.text(f, 1.06, str(f), ha='center', va='bottom', fontsize=13,
                color=c if seed is None else (RED if f == seed else DIM))
    # count bracket
    y0 = -0.18
    ax.annotate('', xy=(count_hi, y0), xytext=(count_lo, y0),
                arrowprops=dict(arrowstyle='<->', color=ODD, lw=1.5))
    ax.text((count_lo + count_hi) / 2, y0 - 0.14, count_lab, ha='center',
            fontsize=11.5, color=ODD)
    ax.text(0.5, 1.20, title, transform=ax.transAxes, ha='center',
            fontsize=13, color=title_col, fontweight='bold')
    ax.set_xlim(30, 470)
    ax.set_ylim(-0.52, 1.32)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)

fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.0), facecolor=BG)
gs = axes[0].get_gridspec()
for a in axes:
    a.set_facecolor(BG)
    for sp in a.spines.values():
        sp.set_visible(False)
    a.set_xticks([]); a.set_yticks([])

# panel 1: the close — the pair at rest, count latent as 2*55
panel(axes[0], [55, 220], [DIM, DIM], 110, 220, 'count = 2·55',
      'the close', DIM)

# panel 2: the strike — the odd rung, spacing IS the count
panel(axes[1], [165, 275], [ODD, ODD], 165, 275, '275 − 165 = 110 = the count',
      'the strike (odd rung)', ODD)

# panel 3: the return — doubled; the count 110 is now the seed
panel(axes[2], [110, 440], [CREAM, CREAM], 110, 330, 'count = 330 = 6·55',
      'the return (×2)', CREAM, seed=110)

# arrows between panels: the strike T
for i, lab in enumerate((r'$\times$', r'$\times$'), start=1):
    ax = axes[i]
    ax.annotate('', xy=(-0.055, 0.0), xytext=(1.055, 0.0),
                xycoords=('axes fraction', 'axes fraction'),
                textcoords=('axes fraction', 'axes fraction'),
                arrowprops=dict(arrowstyle='-|>', color=DIM, lw=1.8,
                                mutation_scale=22))
    ax.text(0.5, 0.5, 'T', ha='center', va='center', fontsize=14, color=ODD,
            transform=ax.transAxes)

axes[0].text(0.5, -0.16, 'T² = 2·Id  —  strike the pair twice, it returns doubled',
             transform=axes[0].transAxes, ha='center', fontsize=11.5,
             color=CREAM)
axes[2].text(0.5, -0.16, 'the count 110 is now the lower tone:',
             transform=axes[2].transAxes, ha='center', fontsize=11.5,
             color=RED)
axes[2].text(0.5, -0.30, 'the miss became the seed.',
             transform=axes[2].transAxes, ha='center', fontsize=11.5,
             color=RED)

plt.tight_layout(pad=0.8)
plt.savefig('assets/dream-strike-ladder.png', dpi=170, facecolor=BG,
            bbox_inches='tight')
print('wrote assets/dream-strike-ladder.png')
