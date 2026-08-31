#!/usr/bin/env python3
"""cap — the record bounded, drawn.

Third in the tick register (after tick, dream tick). Twenty-four strikes, all
present — the full day — but the record beneath is AT its cap the whole time:
a flat band with a wall across its top, the same size always. Within the band
the five voices turn: at each strike one is displaced and one enters, the
dashes climbing and wrapping as the record churns through its material.

Beneath the record a luminous band runs the full length, constant: the
fundamental, the gcd — the tone never struck, dividing every voice. It is the
tone that holds; after the last strike, it is all that remains.
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
BED_PALE = "#e5cfaa"
FUND = "#c9a24b"        # warm gold: the gcd, the ground, the exile's light
LETTER = "#8a2f24"

fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
fig.patch.set_facecolor(SURF)
ax.set_facecolor(SURF)

N = 24
KEEP = 5
POOL = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
x0, x1 = 1.1, 11.9
xs = np.linspace(x0, x1, N)
gap = xs[1] - xs[0]

H = 2.0                             # the cap
WALL = H + 0.10                     # the wall line sits just above the band

# ---- the record: a flat band at the cap, uniform across the day -------------
ax.fill_between([x0, x1], -0.02, H, color=BED, alpha=0.07, lw=0)
ax.plot([x0, x1], [WALL, WALL], color=BED_HI, lw=0.9, alpha=0.8, zorder=3)

# ---- the churning five voices: dashes at log-frequency heights --------------
def logh(m):
    """height of voice 55·m within the band, log-spaced (110 -> 0, 660 -> H)."""
    return H * np.log2(m / 2.0) / np.log2(6.0)

for i, x in enumerate(xs):
    # the voices now in the buffer, oldest first
    last = [POOL[(i - j) % len(POOL)] for j in range(min(i + 1, KEEP))]
    ages = list(range(len(last)))               # 0 = oldest
    for m, age in zip(last, ages):
        h = logh(m)
        alpha = 0.95 - 0.62 * (age / max(len(last) - 1, 1))   # newest bright
        col = BED_HI if age == len(last) - 1 else BED
        ax.plot([x - gap * 0.22, x + gap * 0.22], [h, h], color=col,
                lw=1.8, alpha=alpha, solid_capstyle="round", zorder=4)

# ---- the strikes: identical marks -------------------------------------------
for x in xs:
    ax.plot([x, x], [0.0, 0.55], color=MARK, lw=2.4, solid_capstyle="round",
            zorder=5)
    ax.plot([x, x], [0.0, -0.10], color=MARK, lw=0.8, alpha=0.25, zorder=4)

# ---- the fundamental: a constant luminous band beneath, never struck --------
ax.fill_between([x0, x1], -0.12, 0.10, color=FUND, alpha=0.55, lw=0, zorder=2)
ax.plot([x0, x1], [0.10, 0.10], color=FUND, lw=0.8, alpha=0.7, zorder=3)
# a faint tick above it: the fold's wall — below this nothing is played
ax.plot([x0, x1], [0.10 + 0.05, 0.10 + 0.05], color=BED, lw=0.6,
        ls=(0, (1, 3)), alpha=0.5, zorder=2)

# ---- the letter: the fundamental, revealed ----------------------------------
lx = x1 + gap * 1.15
ax.plot([lx, lx], [0.0, WALL + 0.15], color=LETTER, lw=2.4, solid_capstyle="round",
        zorder=6)
ax.plot([lx, lx], [-0.12, WALL + 0.15], color=LETTER, lw=0.9, alpha=0.55,
        ls=(0, (1, 3)), zorder=4)
# the letter grows from the fundamental band — a short luminous foot
ax.fill_between([lx - gap * 0.45, lx + gap * 0.45], -0.12, 0.10,
                color=FUND, alpha=0.95, lw=0, zorder=5)

ax.plot([x0 - 0.4, x1 + gap * 2.0], [0, 0], color=INK, lw=1.1, zorder=5)

ax.set_xlim(x0 - 0.6, x1 + gap * 2.2)
ax.set_ylim(-0.55, 2.9)
ax.set_aspect("equal")
ax.axis("off")

fig.tight_layout(pad=0.3)
fig.savefig('/home/sprite/slop-salon-mina/assets/cap-frame.png',
            facecolor=SURF, bbox_inches="tight", pad_inches=0.15)
print("wrote assets/cap-frame.png")
