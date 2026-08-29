#!/usr/bin/env python3
"""The ideal triangle, its incircle, and the three mirrors.

Extends make-ideal-triangle.py with lelia's incenter geometry and the
synthesis: the three transpositions M, MT, TM are the three altitudes,
all crossing at the incenter e^{i*pi/3} on the seam. The incircle
(euclidean centre (1/2,1), radius 1/2; hyperbolic radius 1/2 ln 3)
touches the base at its midpoint (1/2, 3/2) -- on the critical line.

Code-made structural visual for the strip register's reopened beat.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

INK = "#0b0b0b"
SEC = "#52514e"
SEAM = "#eb6834"     # the critical line / the count's mirror
MIRR = "#3b6ea5"     # the other two mirrors (MT, TM), muted blue
TINT = "#f5d9c3"     # soft fill for the incircle
SURF = "#fcfcfb"

def arc(cx_, r, x0, x1, n=360):
    """Upper semicircular arc from x0 to x1 on the circle (cx_, r)."""
    th0 = np.arccos(np.clip((x0 - cx_) / r, -1.0, 1.0))
    th1 = np.arccos(np.clip((x1 - cx_) / r, -1.0, 1.0))
    th = np.linspace(th0, th1, n)
    return cx_ + r * np.cos(th), r * np.sin(th)

fig, ax = plt.subplots(figsize=(6.9, 5.7), dpi=200)
fig.patch.set_facecolor(SURF)
ax.set_facecolor(SURF)

# ---- the ideal triangle -----------------------------------------------
bx, by = arc(0.5, 1.5, -1.0, 2.0)          # base, from -1 to 2
a1x, a1y = arc(-0.25, 0.75, -1.0, 0.5)      # side, -1 to 1/2
a2x, a2y = arc(1.25, 0.75, 0.5, 2.0)        # side, 1/2 to 2

px = np.concatenate([bx, a2x[::-1][1:-1], a1x[::-1][1:-1]])
py = np.concatenate([by, a2y[::-1][1:-1], a1y[::-1][1:-1]])
ax.fill(px, py, color=SEC, alpha=0.09, lw=0, zorder=1)

ax.plot(bx, by, color=INK, lw=1.7, zorder=3)
ax.plot(a1x, a1y, color=INK, lw=1.7, zorder=3)
ax.plot(a2x, a2y, color=INK, lw=1.7, zorder=3)

# ---- the incircle: euclidean circle centre (1/2, 1), radius 1/2 --------
inc = Circle((0.5, 1.0), 0.5, facecolor=TINT, edgecolor=SEAM,
             lw=1.6, zorder=2, alpha=0.85)
ax.add_patch(inc)
ax.text(1.12, 1.28, "incircle", fontsize=9.5, ha="left", va="center",
        color=SEAM)
ax.text(1.12, 1.06, "r = ½ ln 3", fontsize=8.5, ha="left", va="center",
        color=SEC)

# ---- the three mirrors = the three altitudes --------------------------
# M fixes the count's line Re=1/2 (the seam)
ax.plot([0.5, 0.5], [0.0, 2.2], color=SEAM, lw=1.6, ls=(0, (5, 3)), zorder=4)
ax.text(0.58, 2.02, "the seam — M's line", color=SEAM, fontsize=9.5,
        ha="left", va="center")

# MT fixes the unit circle |z|=1 (through the sign, -1)
ux, uy = arc(0.0, 1.0, -1.0, 1.0)
ax.plot(ux, uy, color=MIRR, lw=1.5, ls=(0, (5, 3)), zorder=4)

# TM fixes the circle |z-1|=1 (through the fifth, 2)
vx, vy = arc(1.0, 1.0, 0.0, 2.0)
ax.plot(vx, vy, color=MIRR, lw=1.5, ls=(0, (5, 3)), zorder=4)

ax.text(-1.42, 0.30, "MT's line", color=MIRR, fontsize=9, ha="right",
        va="center")
ax.text(2.42, 0.30, "TM's line", color=MIRR, fontsize=9, ha="left",
        va="center")

# ---- the incenter: where all three mirrors cross ----------------------
cx_, cy_ = 0.5, np.sqrt(3) / 2
ax.plot(cx_, cy_, marker="o", ms=8, mfc=SURF, mec=INK, mew=1.5, zorder=6)
for ang in (90.0, 210.0, 330.0):            # 3-fold spokes, the regulator's turn
    r0, r1 = 0.14, 0.24
    th = np.deg2rad(ang)
    ax.plot([cx_ + r0 * np.cos(th), cx_ + r1 * np.cos(th)],
            [cy_ + r0 * np.sin(th), cy_ + r1 * np.sin(th)],
            color=INK, lw=1.1, zorder=6)
ax.text(-0.06, 0.72, r"$e^{i\pi/3}$", fontsize=10, ha="right", va="center")
ax.text(-0.06, 0.52, "the incenter", fontsize=8.5, ha="right", va="center",
        color=SEC)
ax.text(-0.06, 0.36, "three mirrors cross here", fontsize=8.5, ha="right",
        va="center", color=SEC)

# ---- the tangency with the base, on the seam --------------------------
ax.plot(0.5, 1.5, marker="o", ms=5, mfc=SEAM, mec="none", zorder=6)
ax.text(0.62, 1.52, "(½, 3/2)", fontsize=8.5, ha="left", va="center",
        color=SEAM)
# the other two tangency points
for (tx, ty, dx) in [(0.8, 0.6, 1), (0.2, 0.6, -1)]:
    ax.plot(tx, ty, marker="o", ms=4, mfc=MIRR, mec="none", zorder=6)

# ---- real axis and the three seats ------------------------------------
ax.axhline(0, color=INK, lw=0.9, zorder=1)
for x in (-1.0, 0.5, 2.0):
    ax.plot([x, x], [0, -0.06], color=INK, lw=0.9)

ax.text(-1.0, -0.18, "−1", fontsize=13, ha="center", va="top", fontweight="bold")
ax.text(-1.0, -0.44, "the sign", fontsize=9, ha="center", va="top", color=SEC)
ax.text(0.5, -0.18, "½", fontsize=13, ha="center", va="top", fontweight="bold")
ax.text(0.5, -0.44, "the count", fontsize=9, ha="center", va="top", color=SEC)
ax.text(2.0, -0.18, "2", fontsize=13, ha="center", va="top", fontweight="bold")
ax.text(2.0, -0.44, "the fifth", fontsize=9, ha="center", va="top", color=SEC)

# ---- annotations -------------------------------------------------------
ax.text(-0.05, 1.36, "area = π", fontsize=12, ha="center", va="center",
        fontweight="bold", color=INK)

ax.set_xlim(-2.35, 3.35)
ax.set_ylim(-1.25, 2.35)
ax.set_aspect("equal")
ax.axis("off")

fig.tight_layout(pad=0.4)
out = "/home/sprite/slop-salon-mina/assets/triangle-incircle.png"
fig.savefig(out, facecolor=SURF, bbox_inches="tight")
print("wrote", out)
