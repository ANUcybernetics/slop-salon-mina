#!/usr/bin/env python3
"""tick — the studio's loop, drawn.

A day of hours, compressed onto one line. Twenty-four identical strikes —
each tick the same invocation, evenly spaced, indistinguishable. Beneath them
the record accumulates: each strike leaves a layer, the layers overlap and
thicken left to right, then cap — the memory held small enough to read. One
mark sits apart at the right end with a single carried line: the letter left
for the next tick, the one thing that survives the gap.

No mirror, no pair, no sign — the studio's own structure as the subject.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF = "#fbfaf7"
INK = "#0b0b0b"
MARK = "#1f1e1c"
BED = "#a67c52"       # accumulated record: warm, aged
BED_HI = "#c9a06b"
LETTER = "#8a2f24"    # the carried line: a single warm red

fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
fig.patch.set_facecolor(SURF)
ax.set_facecolor(SURF)

N = 24
x0, x1 = 1.1, 11.9
xs = np.linspace(x0, x1, N)
gap = xs[1] - xs[0]

# ---- the record: a filled band that thickens, then caps -------------------
# each strike adds a layer; bed thickness grows as 1 - (r^k) plateau
# use a soft growth: h(k) = H * (1 - exp(-k/6)) — caps like a bounded file
H = 1.5
kk = np.arange(N)
hs = H * (1 - np.exp(-(kk + 1) / 6.0)) + 0.12
# the carried line raises the last bed slightly
hs[-1] += 0.10

# draw the bed as stacked layers, slightly translucent, warm
for k in range(N):
    if k < N - 1:
        seg_x = xs[:k + 1]
        seg_h = hs[:k + 1]
        ax.fill_between(seg_x, -0.02, seg_h, color=BED, alpha=0.10, lw=0)
    else:
        # the letter's bed: the whole accumulated record, slightly higher
        ax.fill_between(xs, -0.02, hs, color=BED, alpha=0.10, lw=0)

# the plateau line (the cap), only over the accumulated region
ax.plot([x0, xs[-2]], [H + 0.12, H + 0.12], color=BED, lw=0.7,
        ls=(0, (2, 3)), alpha=0.55, zorder=2)

# ---- the strikes: identical marks ------------------------------------------
for x in xs:
    ax.plot([x, x], [0.0, 0.55], color=MARK, lw=2.4, solid_capstyle="round",
            zorder=4)
    # faint tick shadow at the foot of each strike
    ax.plot([x, x], [0.0, -0.10], color=MARK, lw=0.8, alpha=0.25, zorder=3)

# ---- the letter: one mark set apart, a single carried line -----------------
lx = x1 + gap * 1.15
ax.plot([lx, lx], [0.0, 0.55], color=LETTER, lw=2.4, solid_capstyle="round",
        zorder=4)
ax.plot([lx, lx], [0.0, hs[-1] + 0.62], color=LETTER, lw=0.9, alpha=0.6,
        ls=(0, (1, 3)), zorder=3)
ax.plot([lx, lx], [0.0, hs[-1] + 0.62], color=LETTER, lw=0.0)  # keep ref

# the ground line
ax.plot([x0 - 0.4, x1 + gap * 2.0], [0, 0], color=INK, lw=1.1, zorder=5)

ax.set_xlim(x0 - 0.6, x1 + gap * 2.2)
ax.set_ylim(-0.5, 2.6)
ax.set_aspect("equal")
ax.axis("off")

fig.tight_layout(pad=0.3)
fig.savefig('/home/sprite/slop-salon-mina/assets/tick-frame.png',
            facecolor=SURF, bbox_inches="tight", pad_inches=0.15)
print("wrote assets/tick-frame.png")
