#!/usr/bin/env python3
"""avatar: the cone's development.

cut the tritone -- omega = pi -- out of the wheel and glue: the wheel with a
semicircle removed is a half-disc; its straight edge is the seam, identified.
the ghost is the apex, at the centre of the seam; the count is the rim point
the two ends of the seam become when glued (one point, seen twice).
one lap around the cone's base is the arc (angle pi of travel) plus the glue:
the flat half-disc IS the lap, and it returns the frame flipped -- the -1.

the avatar is that: a half-disc, the seam, the apex, the count, one lap.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle

BG   = "#0d0d0c"
DISC = "#171614"
RIM  = "#e6e2d8"
SEAM = "#6ab7b0"
GHOST= "#f4efe2"
GOLD = "#d9a441"
ROSE = "#c94f4f"
INNER= "#2e2c28"

S = 10.0
CX = 0.0
YS = 0.0            # seam = the diameter, centred on the avatar
R  = 3.6            # wheel radius (the osculating circle)
X0, X1 = CX - R, CX + R

fig = plt.figure(figsize=(10.24, 10.24), dpi=200)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor(BG)
fig.patch.set_facecolor(BG)
ax.set_xlim(-S, S); ax.set_ylim(-S, S)
ax.set_aspect("equal"); ax.axis("off")

# ---- a faint framing ring, just inside the circular crop (the wheel's reach)
fr = Circle((CX, YS), 4.55, facecolor="none", edgecolor="#2a2825",
            lw=1.2, zorder=0)
ax.add_patch(fr)

# ---- the half-disc (the wheel with the tritone cut, glued flat)
th = np.linspace(0, np.pi, 600)
arcx = CX + R * np.cos(th)
arcy = YS + R * np.sin(th)
half = Polygon(np.column_stack([np.r_[arcx, CX, CX],
                                np.r_[arcy, YS, YS]]),
               closed=True, facecolor=DISC, edgecolor="none", zorder=1)
ax.add_patch(half)

# faint seating arcs inside (the deck, halved)
for rr in (0.62, 1.05, 1.6, 2.3, 3.0):
    t = np.linspace(0, np.pi, 400)
    ax.plot(CX + rr * np.cos(t), YS + rr * np.sin(t),
            color=INNER, lw=1.0, zorder=2)

# ---- the rim (the wheel's arc, the lap path)
ax.plot(arcx, arcy, color=RIM, lw=4.0, solid_capstyle="round", zorder=3)

# ---- the seam (the glued diameter): teal, fracture ticks at both ends
ax.plot([X0, X1], [YS, YS], color=SEAM, lw=3.0, zorder=4)
for x in (X0, X1):
    for sgn in (-1, 1):
        ax.plot([x, x + sgn * 0.22], [YS, YS + sgn * 0.30],
                color=SEAM, lw=1.5, zorder=4)

# ---- the ghost: glow + bright apex point at the centre of the seam
for rad, al in [(2.5, 0.10), (1.7, 0.16), (1.05, 0.26), (0.5, 0.42)]:
    c = Circle((CX, YS), rad, facecolor=GHOST, alpha=al, edgecolor="none",
               zorder=5)
    ax.add_patch(c)
ax.plot([CX], [YS], "o", ms=15, mfc=GHOST, mec="none", zorder=6)

# ---- the count: the rim point both seam ends become, seen twice
for x in (X0, X1):
    ax.plot([x], [YS], "o", ms=11, mfc=GOLD, mec=BG, mew=2.5, zorder=7)

# ---- the lap: one arc from count to count, gold leaving, rose returned
a0 = np.pi - 0.38
a1 = 0.38
def arrow_at(a, color):
    x = CX + R * np.cos(a)
    y = YS + R * np.sin(a)
    ang = np.degrees(np.arctan2(-np.sin(a), np.cos(a)))  # clockwise tangent
    ax.plot([x], [y], marker=(3, 0, ang), ms=20, mfc=color, mec="none",
            zorder=8)
arrow_at(a0, GOLD)
arrow_at(a1, ROSE)

# the travelled arc, faint dashed, between the two arrowheads
t = np.linspace(a0, a1, 200)
ax.plot(CX + R * np.cos(t), YS + R * np.sin(t), color="#55524c", lw=1.5,
        ls=(0, (4, 3)), zorder=3)

plt.savefig("assets/avatar-cone.png", facecolor=BG)
print("saved assets/avatar-cone.png")
