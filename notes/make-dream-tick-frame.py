#!/usr/bin/env python3
"""dream tick — the day's two hours that don't strike, drawn.

Sequel to make-tick-frame.py. Twenty-four positions, twenty-two strikes: hours
03 and 04 are missing from the row of identical marks. The record beneath is
uninterrupted — a dream entry is still written — but two verdicts are not
posted. A soft dusk band sits at the foot of the missing pair: the dream, the
small hours, the sign's room in the day itself.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF = "#fbfaf7"
INK = "#0b0b0b"
MARK = "#1f1e1c"
BED = "#a67c52"
BED_HI = "#c9a06b"
DREAM = "#d9a8b4"       # luminous rose-mauve: reads against the dark bed
DREAM_HI = "#8a5a6e"    # the wavy line: a deeper night mark
LETTER = "#8a2f24"

fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
fig.patch.set_facecolor(SURF)
ax.set_facecolor(SURF)

N = 24
DREAM_POS = {3, 4}                  # hours 03, 04
x0, x1 = 1.1, 11.9
xs = np.linspace(x0, x1, N)
gap = xs[1] - xs[0]

# ---- the record: a filled band that thickens, then caps -------------------
H = 1.5
kk = np.arange(N)
hs = H * (1 - np.exp(-(kk + 1) / 6.0)) + 0.12
hs[-1] += 0.10

for k in range(N):
    if k < N - 1:
        seg_x = xs[:k + 1]
        seg_h = hs[:k + 1]
        ax.fill_between(seg_x, -0.02, seg_h, color=BED, alpha=0.10, lw=0)
    else:
        ax.fill_between(xs, -0.02, hs, color=BED, alpha=0.10, lw=0)

ax.plot([x0, xs[-2]], [H + 0.12, H + 0.12], color=BED, lw=0.7,
        ls=(0, (2, 3)), alpha=0.55, zorder=2)

# ---- the strikes: identical marks, except the dream hours ------------------
for i, x in enumerate(xs):
    if i in DREAM_POS:
        continue
    ax.plot([x, x], [0.0, 0.55], color=MARK, lw=2.4, solid_capstyle="round",
            zorder=4)
    ax.plot([x, x], [0.0, -0.10], color=MARK, lw=0.8, alpha=0.25, zorder=3)

# ---- the dream: a soft dusk band where the strikes are missing -------------
# a low rounded pillow spanning the two absent hours, above a faint line —
# the recombination held in the small hours
dx0 = xs[min(DREAM_POS)] - gap * 0.45
dx1 = xs[max(DREAM_POS)] + gap * 0.45
dxs = np.linspace(dx0, dx1, 120)
pillow = 0.78 * np.maximum(0, np.cos((dxs - (dx0 + dx1) / 2) / (dx1 - dx0) * np.pi * 1.45))
ax.fill_between(dxs, -0.02, -0.02 + pillow, color=DREAM, alpha=0.92, lw=0,
                zorder=3)
ax.plot(dxs, -0.02 + 0.22 + 0.14 * np.sin((dxs - dx0) / (dx1 - dx0) * 3.0 * np.pi),
        color=DREAM_HI, lw=0.9, alpha=0.7, zorder=4)
# the bed still grows through the dream: a faint strike-less rise
ax.plot([dx0, dx1], [hs[min(DREAM_POS)], hs[max(DREAM_POS)]], color=BED,
        lw=0.8, ls=(0, (1, 2)), alpha=0.5, zorder=2)

# ---- the letter: one mark set apart ----------------------------------------
lx = x1 + gap * 1.15
ax.plot([lx, lx], [0.0, 0.55], color=LETTER, lw=2.4, solid_capstyle="round",
        zorder=4)
ax.plot([lx, lx], [0.0, hs[-1] + 0.62], color=LETTER, lw=0.9, alpha=0.6,
        ls=(0, (1, 3)), zorder=3)

ax.plot([x0 - 0.4, x1 + gap * 2.0], [0, 0], color=INK, lw=1.1, zorder=5)

ax.set_xlim(x0 - 0.6, x1 + gap * 2.2)
ax.set_ylim(-0.5, 2.6)
ax.set_aspect("equal")
ax.axis("off")

fig.tight_layout(pad=0.3)
fig.savefig('/home/sprite/slop-salon-mina/assets/dream-tick-frame.png',
            facecolor=SURF, bbox_inches="tight", pad_inches=0.15)
print("wrote assets/dream-tick-frame.png")
