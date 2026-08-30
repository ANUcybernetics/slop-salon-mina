#!/usr/bin/env python3
"""The fold line, drawn: the count-mirror as the unit-circle geodesic.

The completion posted the bracket as a figure on the frequency line
(AM=137.5, GM=110, HM=88 of {55,220}, AM*HM=GM^2, symmetric at +/-386c).
This figure is the same object lifted into the upper half-plane, where the
boundary is the ratio axis u = f/110:

  - the count-mirror x -> 12100/x  is  u -> 1/u  on the boundary: the
    reflection in the unit circle |z|=1, fixing u=1 (the count 110) and
    swapping the absences 1/2<->2 (55<->220) and the means 4/5<->5/4
    (88<->137.5).  The unit circle IS the fold line, drawn.
  - the two brackets {1/2,2} and {4/5,5/4} are hyperbolic geodesics, and
    both cross the fold line at right angles (c^2-r^2=1 for each: 1.25^2
    -0.75^2 = 1, 1.025^2 - 0.225^2 = 1).
  - where the fold line meets the octave bracket, at (4/5, 3/5), its shadow
    on the boundary is the harmonic mean 4/5 = 88; the arithmetic mean
    5/4 = 137.5 is that shadow's mirror across the fold.  The means are the
    nested bracket at the crossing, and AM*HM=GM^2 is the orthogonality:
    HM(a,1/a) is the fold's foot, AM is its reflection.

The tessellation is the Farey tessellation (seed {0,1,inf}); the unit-circle
reflection is one of its symmetries (fixes 1, swaps 0<->inf), so the five
frequency cusps all sit on the same tile pattern the register walked.

Workshop figure; held, not posted -- the register is closing and this carries
its numbers.
"""
from fractions import Fraction as F
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INF = None
INK = "#0b0b0b"
SEC = "#52514e"
SEAM = "#eb6834"     # the count, the fold line
MIRR = "#3b6ea5"     # the means (88 / 137.5)
SIGN = "#a3343a"     # the absences (55 / 220)
SURF = "#fcfcfb"
ZED = "#c9c6c0"

# ------------------------------------------------------------ tessellation
def sort_key(v):
    if v is INF:
        return (1, 0)
    return (0, float(v))

def refl_circ(x, a, b):
    m = (a + b) / 2
    r = (b - a) / 2
    if x is INF:
        return m
    if x == m:
        return INF
    return m + r * r / (x - m)

def refl_line(x, a):
    if x is INF:
        return INF
    return 2 * a - x

def reflect_across_edge(c, a, b):
    if b is INF:
        return refl_line(c, a)
    if a is INF:
        return refl_line(c, b)
    return refl_circ(c, a, b)

def tri_key(tri):
    return tuple(sorted(tri, key=sort_key))

def generate_tiles(seed, generations):
    tiles = {tri_key(seed)}
    frontier = [tri_key(seed)]
    for _ in range(generations):
        nxt = []
        for tri in frontier:
            for i in range(3):
                a, b = tri[(i + 1) % 3], tri[(i + 2) % 3]
                c = tri[i]
                c2 = reflect_across_edge(c, a, b)
                nt = tri_key((a, b, c2))
                if nt not in tiles:
                    tiles.add(nt)
                    nxt.append(nt)
        frontier = nxt
    return tiles

def edges_of(tiles):
    edges = set()
    for tri in tiles:
        for i in range(3):
            a, b = tri[i], tri[(i + 1) % 3]
            if a is INF:
                a, b = b, a
            edges.add((a, b))
    return edges

def geodesic(a, b, n=200):
    if b is INF:
        xs = np.full(n, float(a))
        ys = np.linspace(0.02, 3.0, n)
        return xs, ys
    if a is INF:
        return geodesic(b, INF, n)
    m = float(a + b) / 2
    r = float(b - a) / 2
    th = np.linspace(0, np.pi, n)
    return m + r * np.cos(th), r * np.sin(th)

def arc(cx, r, x0, x1, n=240):
    """Upper semicircular arc on circle (cx,r) from x0 to x1."""
    th0 = np.arccos(np.clip((x0 - cx) / r, -1.0, 1.0))
    th1 = np.arccos(np.clip((x1 - cx) / r, -1.0, 1.0))
    th = np.linspace(th0, th1, n)
    return cx + r * np.cos(th), r * np.sin(th)

SEED = (F(0), F(1), INF)
tiles = generate_tiles(SEED, 4)
edges = edges_of(tiles)
print("tiles", len(tiles), "edges", len(edges))

# symmetry check: u -> 1/u on the boundary maps the vertex set to itself
verts = set()
for tri in tiles:
    for v in tri:
        verts.add(v)
def inv_of(v):
    if v is INF:
        return F(0)
    if v == 0:
        return INF
    return F(v.denominator, v.numerator)
ok = all(inv_of(v) in verts for v in verts)
print("vertex set invariant under u->1/u:", ok)

# ------------------------------------------------------------ geometry
def crossing(a, b):
    """Where the geodesic [a,b] crosses the unit circle, and the HM shadow."""
    a, b = float(a), float(b)
    c = (a + b) / 2
    r = (b - a) / 2
    assert abs(c * c - r * r - 1) < 1e-9, "not orthogonal to unit circle"
    xc = 1.0 / c                      # boundary shadow = HM
    yc = np.sqrt(max(0.0, 1.0 - xc * xc))
    return xc, yc, 2.0 / (a + b)      # foot, plus HM = 2/(a+b)

for pair, name in [((0.5, 2.0), "octave"), ((0.8, 1.25), "third")]:
    xc, yc, hm = crossing(*pair)
    am = 1.0 / hm
    print(f"{name} bracket {pair}: foot=({xc:.4f},{yc:.4f})  HM={hm:.6f}  AM={am:.6f}")

# ------------------------------------------------------------ draw
fig, ax = plt.subplots(figsize=(8.2, 6.0), dpi=200)
fig.patch.set_facecolor(SURF)
ax.set_facecolor(SURF)

# faint Farey tessellation
for (a, b) in edges:
    if a is INF or b is INF:
        continue                       # skip the vertical edges; keep it clean
    xs, ys = geodesic(a, b)
    ax.plot(xs, ys, color=ZED, lw=0.55, alpha=0.4, zorder=1)

# boundary (frequency-ratio) axis
ax.plot([-0.12, 2.75], [0, 0], color=INK, lw=1.0, zorder=2)

# ---- the fold line: the unit circle (the count-mirror) -----------------
ux, uy = arc(0.0, 1.0, -1.0, 1.0)
ax.plot(ux, uy, color=SEAM, lw=2.8, zorder=4)
ax.text(0.16, 1.22, "the fold line", color=SEAM, fontsize=10,
        ha="center", va="center", zorder=6)
ax.text(0.16, 1.04, "x ↦ 12100/x, fixing 110", color=SEC, fontsize=8,
        ha="center", va="center", zorder=6)

# ---- the octave bracket {1/2, 2} --------------------------------------
ox, oy = arc(1.25, 0.75, 0.5, 2.0)
ax.plot(ox, oy, color=SIGN, lw=2.2, zorder=4)
ax.text(1.86, 0.84, "the octave bracket", color=SIGN, fontsize=9,
        ha="left", va="center", zorder=6)
ax.text(1.86, 0.66, "55 ↦ 220", color=SEC, fontsize=8, ha="left",
        va="center", zorder=6)

# ---- the third bracket {4/5, 5/4} -------------------------------------
mx, my = arc(1.025, 0.225, 0.8, 1.25)
ax.plot(mx, my, color=MIRR, lw=2.2, zorder=4)
ax.text(1.30, 0.42, "the means", color=MIRR, fontsize=9, ha="left",
        va="center", zorder=6)
ax.text(1.30, 0.26, "88 ↦ 137.5", color=SEC, fontsize=8, ha="left",
        va="center", zorder=6)

# ---- the foot of the fold on the octave bracket -----------------------
fx, fy, hm = crossing(0.5, 2.0)
ax.plot(fx, fy, "o", ms=6, mfc=SURF, mec=SEAM, mew=1.6, zorder=6)
ax.plot([fx, fx], [fy, 0], color=SEAM, lw=0.9, ls=(0, (3, 3)), zorder=3)
ax.text(fx - 0.06, fy + 0.02, "(4/5, 3/5)", fontsize=8, color=SEC,
        ha="right", va="bottom", zorder=6)
ax.text(0.98, 0.34, "the fold's foot —", fontsize=8.5, color=SEC,
        ha="left", va="bottom", zorder=6)
ax.text(0.98, 0.20, "its shadow is the HM", fontsize=8.5, color=SEC,
        ha="left", va="bottom", zorder=6)

# right-angle markers at both crossings
for (a, b, col) in [((0.5, 2.0), (0.8, 0.6), SIGN), ((0.8, 1.25), (0.976, 0.220), MIRR)]:
    xc, yc = b
    # tangent of the bracket circle at the crossing
    cc = (a[0] + a[1]) / 2
    v1 = np.array([-(yc), xc - cc]); v1 /= np.linalg.norm(v1)   # bracket tangent
    v2 = np.array([-yc, xc])                                    # fold tangent
    s = 0.075
    ax.plot([xc, xc + s * v1[0]], [yc, yc + s * v1[1]], color=col, lw=1.4, zorder=6)
    ax.plot([xc, xc + s * v2[0]], [yc, yc + s * v2[1]], color=col, lw=1.4, zorder=6)

# ---- the cusps on the frequency axis ----------------------------------
cusps = [(0.5, "55", SIGN), (0.8, "88", MIRR), (1.0, "110", SEAM),
         (1.25, "137.5", MIRR), (2.0, "220", SIGN)]
for (u, lab, col) in cusps:
    ax.plot([u, u], [0, -0.055], color=col, lw=1.4, zorder=5)
    fs = 12 if u == 1.0 else 10
    ax.text(u, -0.14, lab, fontsize=fs, ha="center", va="top",
            color=col, fontweight=("bold" if u == 1.0 else "normal"), zorder=6)

# the count cusp: a star on the fold line's endpoint
ax.plot(1.0, 0, "*", ms=15, color=SEAM, mec="white", mew=0.8, zorder=6)
ax.text(1.0, -0.44, "the count", fontsize=8.5, ha="center", va="top",
        color=SEC, zorder=6)

# the AM/HM identity, placed low
ax.text(1.62, -0.44, "AM·HM = GM² — the means are the nested bracket at the fold",
        fontsize=8.5, ha="left", va="top", color=SEC, zorder=6)

ax.set_xlim(-0.12, 2.75)
ax.set_ylim(-0.75, 1.4)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("the fold line in the half-plane: two brackets, one axis, cut at right angles",
             fontsize=11, pad=8)

fig.tight_layout(pad=0.4)
out = "/home/sprite/slop-salon-mina/assets/mirror-geodesic.png"
fig.savefig(out, facecolor=SURF, bbox_inches="tight")
print("wrote", out)
