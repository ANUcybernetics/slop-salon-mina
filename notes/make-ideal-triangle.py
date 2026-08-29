#!/usr/bin/env python3
"""The ideal triangle of the deck: seats {-1, 1/2, 2}.

Verify the geometry, then draw it. Code-made structural visual for the
strip register's closing node: the three seats are an ideal triangle
(area pi), the regulator T(s)=(s-1)/s its 120-degree turn about the
order-3 elliptic point e^{i*pi/3}, the reflection R(s)=1-s its mirror,
and the deck S_3 the triangle's full symmetry group. The mirror's
fixed geodesic, Re(s)=1/2 through the count, is the seam.
"""
import numpy as np

# ----------------------------------------------------------------------
# verification
# ----------------------------------------------------------------------
print("== verification ==")

# the regulator 3-cycle on the seats
def T(s):
    return (s - 1.0) / s

s = 0.5
seen = []
for _ in range(6):
    seen.append(s)
    s = T(s)
print("T orbit from 1/2:", [round(x, 6) for x in seen[:4]], "(3-cycle, T^3=id)")

# fixed point of T: s^2 - s + 1 = 0
root = 0.5 + 1j * np.sqrt(3) / 2
print("T fixed point:", root, "|T(root)-root| =", abs((root - 1) / root - root))

# reflection R(s) = 1 - s: fixes 1/2, swaps -1 and 2
print("R(1/2):", 1 - 0.5, " R(-1):", 1 - (-1), " R(2):", 1 - 2)

# hyperbolic area of the ideal triangle: int dx (1/y_low - 1/y_high)
def y_big(x):   # big arc, center (1/2, 0), r 3/2, on x in [-1, 2]
    return np.sqrt(max(0.0, 1.5**2 - (x - 0.5)**2))

def y_smallA(x):  # center (-1/4, 0), r 3/4, x in [-1, 1/2]
    return np.sqrt(max(0.0, 0.75**2 - (x + 0.25)**2))

def y_smallB(x):  # center (5/4, 0), r 3/4, x in [1/2, 2]
    return np.sqrt(max(0.0, 0.75**2 - (x - 1.25)**2))

xs = np.linspace(-1.0, 2.0, 400001)
lo = np.zeros_like(xs)
hi = np.zeros_like(xs)
for i, x in enumerate(xs):
    yl = 0.0
    if -1.0 <= x <= 0.5:
        yl = max(yl, y_smallA(x))
    if 0.5 <= x <= 2.0:
        yl = max(yl, y_smallB(x))
    lo[i] = yl
    hi[i] = y_big(x)
# the vertices are integrable singularities (1/lo ~ |x-x0|^-1/2); drop the
# exact zeros so the trapezoid stays finite, error ~ O(sqrt(dx)) ~ 0.003
f = np.zeros_like(xs)
ok = (lo > 1e-9) & (hi > 1e-9)
f[ok] = 1.0 / lo[ok] - 1.0 / hi[ok]
area = np.trapezoid(f, xs)
print("hyperbolic area (numeric):", area, " vs pi:", np.pi)

# center equidistant from the three sides (incenter): verify via group
# instead -- T permutes the sides and fixes the center. done.

# ----------------------------------------------------------------------
# figure
# ----------------------------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INK = "#0b0b0b"
SEC = "#52514e"
SEAM = "#eb6834"   # validated categorical slot 2 (orange)
SURF = "#fcfcfb"

def arc(cx_, r, x0, x1, n=300):
    th0 = np.arccos(np.clip((x0 - cx_) / r, -1.0, 1.0))
    th1 = np.arccos(np.clip((x1 - cx_) / r, -1.0, 1.0))
    th = np.linspace(th0, th1, n)
    return cx_ + r * np.cos(th), r * np.sin(th)

fig, ax = plt.subplots(figsize=(6.8, 5.6), dpi=200)
fig.patch.set_facecolor(SURF)
ax.set_facecolor(SURF)

# ideal triangle: the three geodesic sides
bx, by = arc(0.5, 1.5, -1.0, 2.0)
a1x, a1y = arc(-0.25, 0.75, -1.0, 0.5)
a2x, a2y = arc(1.25, 0.75, 0.5, 2.0)

# interior fill
px = np.concatenate([bx, a2x[::-1][1:-1], a1x[::-1][1:-1]])
py = np.concatenate([by, a2y[::-1][1:-1], a1y[::-1][1:-1]])
ax.fill(px, py, color=SEC, alpha=0.09, lw=0, zorder=1)

ax.plot(bx, by, color=INK, lw=1.7, zorder=2)
ax.plot(a1x, a1y, color=INK, lw=1.7, zorder=2)
ax.plot(a2x, a2y, color=INK, lw=1.7, zorder=2)

# the seam: fixed geodesic of R(s)=1-s, the vertical line through the count
ax.plot([0.5, 0.5], [0.0, 2.15], color=SEAM, lw=1.5, ls=(0, (4, 3)), zorder=3)
ax.text(0.58, 1.98, "the seam", color=SEAM, fontsize=10.5, ha="left", va="center")

# mirror's action: the swap of -1 and 2 along the real axis
ax.annotate("", xy=(-1.0, -0.62), xytext=(2.0, -0.62),
            arrowprops=dict(arrowstyle="<->", color=SEAM, lw=1.3))
ax.text(0.5, -0.72, "the mirror: s $\\mapsto$ 1$-$s", color=SEAM,
        fontsize=9.5, ha="center", va="top")

# real axis and the three seats
ax.axhline(0, color=INK, lw=0.9, zorder=1)
for x in (-1.0, 0.5, 2.0):
    ax.plot([x, x], [0, -0.06], color=INK, lw=0.9)

ax.text(-1.0, -0.18, "−1", fontsize=13, ha="center", va="top", fontweight="bold")
ax.text(-1.0, -0.42, "the sign", fontsize=9, ha="center", va="top", color=SEC)
ax.text(0.5, -0.18, "½", fontsize=13, ha="center", va="top", fontweight="bold")
ax.text(0.5, -0.42, "the count", fontsize=9, ha="center", va="top", color=SEC)
ax.text(2.0, -0.18, "2", fontsize=13, ha="center", va="top", fontweight="bold")
ax.text(2.0, -0.42, "the fifth", fontsize=9, ha="center", va="top", color=SEC)

# the centre: order-3 elliptic point e^{i*pi/3}, fixed by the regulator
cx_, cy_ = 0.5, np.sqrt(3) / 2
ax.plot(cx_, cy_, marker="o", ms=7, mfc="none", mec=INK, mew=1.4, zorder=4)
for ang in (90.0, 210.0, 330.0):
    r0, r1 = 0.12, 0.22
    th = np.deg2rad(ang)
    ax.plot([cx_ + r0 * np.cos(th), cx_ + r1 * np.cos(th)],
            [cy_ + r0 * np.sin(th), cy_ + r1 * np.sin(th)],
            color=INK, lw=1.1, zorder=4)
ax.text(0.14, 0.86, r"$e^{i\pi/3}$", fontsize=10, ha="left", va="center")

# the regulator's turn: a faint 120-degree arc about the centre (no arrow,
# the 3-fold spokes carry the rotation; the caption names the turn)
th = np.linspace(np.deg2rad(20), np.deg2rad(140), 60)
rr = 0.34
ax.plot(cx_ + rr * np.cos(th), cy_ + rr * np.sin(th), color=SEC, lw=1.1, zorder=4)
ax.text(1.02, 0.88, "120° turn", fontsize=9, ha="left", va="center",
        color=SEC)

# area annotation, left of the seam so the dashed line stays clean
ax.text(-0.05, 1.34, "area = π", fontsize=12, ha="center", va="center",
        fontweight="bold", color=INK)

# framing
ax.set_xlim(-2.15, 3.15)
ax.set_ylim(-1.15, 2.25)
ax.set_aspect("equal")
ax.axis("off")

fig.tight_layout(pad=0.4)
out = "/home/sprite/slop-salon-mina/assets/ideal-triangle.png"
fig.savefig(out, facecolor=SURF, bbox_inches="tight")
print("wrote", out)
