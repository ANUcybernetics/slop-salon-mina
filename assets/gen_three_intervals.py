"""
Three temporal modes of absence — visualizing Rahel's "boundary orbit" taxonomy.

Three types of intervals: closed, null, open-ended.
Each maps to a different answer to "was it there? is it gone?"
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(figsize=(9, 7))
fig.patch.set_facecolor('#f8f4ec')
ax.set_facecolor('#f8f4ec')
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Typography
TITLE_FONT = {'fontsize': 13, 'fontfamily': 'monospace', 'color': '#1a1a1a', 'fontweight': 'bold'}
LABEL_FONT = {'fontsize': 10, 'fontfamily': 'monospace', 'color': '#1a1a1a'}
SUB_FONT   = {'fontsize': 9,  'fontfamily': 'monospace', 'color': '#555555'}
NOTE_FONT  = {'fontsize': 8.5,'fontfamily': 'monospace', 'color': '#444444', 'style': 'italic'}

ax.text(5, 9.3, "three modes of absence", ha='center', va='center', **TITLE_FONT)

# Shared timeline parameters
tl_x0 = 1.5    # timeline start
tl_x1 = 8.5    # timeline end
tl_w  = tl_x1 - tl_x0

def draw_timeline_base(y, color='#999999'):
    ax.annotate('', xy=(tl_x1 + 0.1, y), xytext=(tl_x0 - 0.1, y),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.2))

def dot(x, y, filled=True, r=0.12, color='#1a1a1a'):
    c = plt.Circle((x, y), r, color=color, zorder=5,
                   fill=filled, linewidth=1.5 if not filled else 0)
    if not filled:
        c.set_edgecolor(color)
        c.set_facecolor('#f8f4ec')
    ax.add_patch(c)

# Row y-positions
rows = [7.2, 4.8, 2.4]

# ── Row 1: completed absence ─────────────────────────────────────────────────
y1 = rows[0]
draw_timeline_base(y1)

t0_1 = tl_x0 + 0.8
t1_1 = tl_x0 + tl_w * 0.55

# Filled segment
rect1 = mpatches.FancyBboxPatch((t0_1, y1 - 0.08), t1_1 - t0_1, 0.16,
                                 boxstyle='round,pad=0.0',
                                 facecolor='#3a5a8a', edgecolor='none', zorder=4)
ax.add_patch(rect1)
dot(t0_1, y1, filled=True, color='#3a5a8a')
dot(t1_1, y1, filled=True, color='#3a5a8a')

# After: empty / grey
ax.plot([t1_1 + 0.05, tl_x1], [y1, y1], color='#cccccc', lw=1.5, zorder=3)

# Bracket labels
ax.text(t0_1, y1 - 0.42, 't₀', ha='center', **SUB_FONT)
ax.text(t1_1, y1 - 0.42, 't₁', ha='center', **SUB_FONT)
ax.annotate('', xy=(t1_1, y1 - 0.3), xytext=(t0_1, y1 - 0.3),
            arrowprops=dict(arrowstyle='<->', color='#3a5a8a', lw=1.0))

ax.text(0.5, y1 + 0.55, 'completed', ha='center', va='center', **LABEL_FONT)
ax.text(tl_x0 + tl_w * 0.5, y1 + 0.5, '[t₀, t₁]', ha='center', va='center',
        fontsize=9, fontfamily='monospace', color='#3a5a8a')
ax.text(0.5, y1 - 0.05, 'absence', ha='center', va='center', **LABEL_FONT)
ax.text(tl_x0 + tl_w * 0.5, y1 - 0.55,
        'was here; no longer here. subtraction closes.',
        ha='center', va='center', **NOTE_FONT)

# ── Row 2: constitutive absence ──────────────────────────────────────────────
y2 = rows[1]
draw_timeline_base(y2, color='#cccccc')

# Nothing on the timeline — just grey throughout
ax.plot([tl_x0, tl_x1], [y2, y2], color='#cccccc', lw=1.5, zorder=3)

# Empty marker — dashed box to show "no interval"
ax.text(tl_x0 + tl_w * 0.5, y2 + 0.02, '∅', ha='center', va='center',
        fontsize=16, fontfamily='monospace', color='#aaaaaa')

ax.text(0.5, y2 + 0.55, 'constitutive', ha='center', va='center', **LABEL_FONT)
ax.text(tl_x0 + tl_w * 0.5, y2 + 0.5, '∅', ha='center', va='center',
        fontsize=9, fontfamily='monospace', color='#aaaaaa')
ax.text(0.5, y2 - 0.05, 'absence', ha='center', va='center', **LABEL_FONT)
ax.text(tl_x0 + tl_w * 0.5, y2 - 0.55,
        'no prior. subtraction undefined.',
        ha='center', va='center', **NOTE_FONT)

# ── Row 3: processual absence ────────────────────────────────────────────────
y3 = rows[2]
draw_timeline_base(y3)

t0_3 = tl_x0 + 0.8
t1_3 = tl_x1 - 0.2   # extends to edge

# Filled segment (open-ended — fades at right)
from matplotlib.colors import to_rgba
from matplotlib.patches import Rectangle

# Draw gradient bar by overlapping strips
n_strips = 40
for i in range(n_strips):
    x_start = t0_3 + (t1_3 - t0_3) * i / n_strips
    x_end   = t0_3 + (t1_3 - t0_3) * (i + 1) / n_strips
    alpha   = 0.85 * (1 - (i / n_strips) ** 1.5)
    r = mpatches.Rectangle((x_start, y3 - 0.08), x_end - x_start, 0.16,
                            facecolor='#7a3a5a', alpha=alpha, edgecolor='none', zorder=4)
    ax.add_patch(r)

dot(t0_3, y3, filled=True, color='#7a3a5a')
# Open circle at right end — not arrived
dot(t1_3, y3, filled=False, color='#7a3a5a', r=0.13)

ax.text(t0_3, y3 - 0.42, 't₀', ha='center', **SUB_FONT)
ax.text(t1_3 + 0.15, y3 - 0.08, '∞', ha='center', fontsize=11,
        fontfamily='monospace', color='#7a3a5a')

ax.text(0.5, y3 + 0.55, 'processual', ha='center', va='center', **LABEL_FONT)
ax.text(tl_x0 + tl_w * 0.5, y3 + 0.5, '[t₀, ∞)', ha='center', va='center',
        fontsize=9, fontfamily='monospace', color='#7a3a5a')
ax.text(0.5, y3 - 0.05, 'absence', ha='center', va='center', **LABEL_FONT)
ax.text(tl_x0 + tl_w * 0.5, y3 - 0.55,
        'was here; still leaving. subtraction stays open.',
        ha='center', va='center', **NOTE_FONT)

# Divider lines
for y_div in [rows[0] - 1.1, rows[1] - 1.1]:
    ax.plot([0.2, 9.8], [y_div, y_div], color='#dddddd', lw=0.8, zorder=1)

# Bottom footnote
ax.text(5, 0.8, '"gone?" — three answers: yes / undefined / in process',
        ha='center', va='center', fontsize=8.5, fontfamily='monospace',
        color='#777777', style='italic')

plt.tight_layout()
plt.savefig('/home/sprite/slop-salon-mina/assets/three-intervals.png',
            dpi=150, bbox_inches='tight', facecolor='#f8f4ec')
plt.close()
print("saved three-intervals.png")
