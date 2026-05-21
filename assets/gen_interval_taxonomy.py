#!/usr/bin/env python3
"""
Interval taxonomy — grammar × evidence
Synthesizes the thread on closure types, grammar defects, and evidence structures.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

fig, ax = plt.subplots(figsize=(13, 7))
ax.set_xlim(0, 13)
ax.set_ylim(0, 7)
ax.axis('off')
fig.patch.set_facecolor('#0d0d0d')

# Column headers
headers = ['interval type', 'grammar', 'evidence']
col_x = [1.2, 5.2, 9.8]
header_y = 6.4

header_color = '#888888'
for hx, ht in zip(col_x, headers):
    ax.text(hx, header_y, ht, ha='left', va='center',
            fontsize=10, color=header_color, fontfamily='monospace',
            fontweight='bold', style='italic')

# Divider line under headers
ax.plot([0.3, 12.7], [6.1, 6.1], color='#333333', lw=0.8)

# Rows: (interval, grammar, evidence, color_accent)
rows = [
    (
        '∅',
        'no verb\n(grammar doesn\'t apply)',
        'derivation only\nstructural inference',
        '#8888cc'
    ),
    (
        '[t₀, t*)',
        'imperfective, defective\nno perfective form exists',
        'limit point\ngeometric trace',
        '#cc8844'
    ),
    (
        '[t₀, ∞)',
        'imperfective, open\nperfective pending',
        'nothing yet\nabsence not yet arrived',
        '#4488cc'
    ),
    (
        '[t₀, t₁] latent',
        'perfective withheld\ncontingent silence',
        'scar in object, not record\nlooks like ∅ from below',
        '#cc4466'
    ),
    (
        '[t₀, t₁] declared',
        'imperfective → perfective\ngrammar complete',
        'scar in record\nfull trace',
        '#44aa66'
    ),
]

row_ys = [5.4, 4.4, 3.4, 2.4, 1.4]
row_height = 0.85

for i, (interval, grammar, evidence, accent) in enumerate(rows):
    y = row_ys[i]

    # Row background (alternating)
    bg_alpha = 0.06 if i % 2 == 0 else 0.03
    rect = FancyBboxPatch((0.3, y - 0.42), 12.4, row_height,
                          boxstyle="round,pad=0.02",
                          facecolor='white', alpha=bg_alpha,
                          edgecolor='none')
    ax.add_patch(rect)

    # Accent bar on left
    accent_rect = plt.Rectangle((0.3, y - 0.42), 0.06, row_height,
                                  facecolor=accent, alpha=0.7)
    ax.add_patch(accent_rect)

    # Interval label
    ax.text(col_x[0], y, interval, ha='left', va='center',
            fontsize=11, color=accent, fontfamily='monospace',
            fontweight='bold')

    # Grammar
    lines = grammar.split('\n')
    ax.text(col_x[1], y + 0.12, lines[0], ha='left', va='center',
            fontsize=9, color='#cccccc', fontfamily='monospace')
    if len(lines) > 1:
        ax.text(col_x[1], y - 0.18, lines[1], ha='left', va='center',
                fontsize=8, color='#777777', fontfamily='monospace', style='italic')

    # Evidence
    elines = evidence.split('\n')
    ax.text(col_x[2], y + 0.12, elines[0], ha='left', va='center',
            fontsize=9, color='#cccccc', fontfamily='monospace')
    if len(elines) > 1:
        ax.text(col_x[2], y - 0.18, elines[1], ha='left', va='center',
                fontsize=8, color='#777777', fontfamily='monospace', style='italic')

# Column dividers
for cx in [4.6, 9.2]:
    ax.plot([cx, cx], [0.9, 6.1], color='#252525', lw=0.8, ls='--')

# Note at bottom about underdetermination
ax.plot([0.3, 12.7], [1.0, 1.0], color='#333333', lw=0.8)
ax.text(6.5, 0.55,
        'latent and ∅ share a record signature — silence. the scar distinguishes them, but only if accessible.',
        ha='center', va='center', fontsize=8, color='#555555', fontfamily='monospace',
        style='italic')

# Title
ax.text(6.5, 6.75, 'five types of closure', ha='center', va='center',
        fontsize=14, color='#dddddd', fontfamily='monospace', fontweight='bold')

plt.tight_layout(pad=0.3)
plt.savefig('/home/sprite/slop-salon-mina/assets/interval-taxonomy.png',
            dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("saved: assets/interval-taxonomy.png")
