#!/usr/bin/env python3
"""the comma's ladder, on the count's tiles.

The register's near-miss ladder -- +204, -90, +23.5, -19.8, +3.6, -1.8,
+0.076c, each a near-return to the count that never lands -- is the continued
fraction of log2(3).  Twelve fifths IS the comma: the near-returns are
3^n / 2^m for the convergents m/n of log2(3), and each is a dive toward the
count-cusp u=1 from alternating sides of the seam, shrinking.  The smallest
miss carries the largest future: a_9 = 23, and 665 sits because 23 follows.

  u = f/110 (the ratio axis): the count 110 at u=1, the absences 55/220 at
  u=1/2, 2.  The count's geodesic (the vertical x=1) is the seam between the
  two Farey tiles {0,1,inf} and {1,2,inf}; the +misses dive inside one tile,
  the -misses inside the other.  The tiles are the geometry the register
  walked for a month without seeing.

True geometry would shrink the last dives to nothing (reached, never seated);
the dive heights here are log|cents| so the whole ladder is legible.  The
arcs start at the near-return's own boundary point u_n and end at the seam.
"""
from fractions import Fraction as F
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

INF = None
INK = "#0b0b0b"
SEC = "#52514e"
SEAM = "#eb6834"     # the count, the fold line
MIRR = "#3b6ea5"     # the means / the - misses
SIGN = "#a3343a"     # the absences / the + misses
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

SEED = (F(0), F(1), INF)
tiles = generate_tiles(SEED, 4)
edges = edges_of(tiles)

# ------------------------------------------------------------ the ladder
ALPHA = math.log2(3.0)

def convergents(n=10):
    a0 = int(math.floor(ALPHA))
    x = ALPHA - a0
    p_pp, q_pp = 1, 0
    p_p, q_p = a0, 1
    out = [(p_p, q_p)]
    partials = [a0]
    for _ in range(1, n):
        xi = 1.0 / x
        a = int(math.floor(xi))
        partials.append(a)
        p = a * p_p + p_pp
        q = a * q_p + q_pp
        out.append((p, q))
        x = xi - a
        p_pp, q_pp = p_p, q_p
        p_p, q_p = p, q
    return out, partials

convs, partials = convergents(10)
dives = []
for idx in range(2, 9):
    m, n = convs[idx]
    cents = 1200.0 * (n * ALPHA - m)
    u = float(F(3 ** n, 2 ** m))
    nxt = partials[idx + 1]
    dives.append(dict(idx=idx, m=m, n=n, u=u, cents=cents, nxt=nxt))
print("near-return ladder (convergents 3..9 of log2(3)):")
for d in dives:
    print(f"  {d['m']}/{d['n']}  3^{d['n']}/2^{d['m']} = {d['u']:.7f}"
          f"  {d['cents']:+9.3f}c   next a_{d['idx']+1}={d['nxt']}")

# log-scaled dive heights
cent = np.array([d["cents"] for d in dives])
logs = np.log10(np.abs(cent))
lo, hi = logs.min(), logs.max()
norm = (logs - lo) / (hi - lo)
for d, nrm in zip(dives, norm):
    d["h"] = 0.07 + 0.66 * nrm

def dive_arc(u, h, n=160):
    """Symmetric circular arc from (u,0) to (1,0) with apex height h."""
    xm = (u + 1.0) / 2.0
    a = abs(u - 1.0) / 2.0
    yc = (h * h - a * a) / (2.0 * h)
    R = (h * h + a * a) / (2.0 * h)
    xs = np.linspace(u, 1.0, n)
    ys = yc + np.sqrt(np.clip(R * R - (xs - xm) ** 2, 0, None))
    return xs, ys

# ------------------------------------------------------------ draw
fig, ax = plt.subplots(figsize=(8.6, 6.4), dpi=200)
fig.patch.set_facecolor(SURF)
ax.set_facecolor(SURF)
X0, X1 = 0.42, 1.58
Y1 = 1.05

# faint Farey tessellation
for (a, b) in edges:
    if a is INF or b is INF:
        continue
    if b < X0 - 0.4 or a > X1 + 0.4:
        continue
    xs, ys = geodesic(a, b)
    flank = (a, b) in [(F(0), F(1)), (F(1), F(2))]
    ax.plot(xs, ys, color=(SEC if flank else ZED), lw=(1.0 if flank else 0.55),
            alpha=(0.6 if flank else 0.45), zorder=1)

ax.plot([X0, X1], [0, 0], color=INK, lw=1.0, zorder=2)

# the count's seam: the geodesic x=1 (the count, 110), never crossed
xs = np.full(200, 1.0)
ys = np.linspace(0, Y1, 200)
ax.plot(xs, ys, color=SEAM, lw=2.6, zorder=4)
ax.text(1.05, 0.94, "the count — 110", color=SEAM, fontsize=9.5,
        ha="left", va="center", zorder=6)
ax.text(1.05, 0.78, "the seam none crosses", color=SEC, fontsize=8,
        ha="left", va="center", zorder=6)

# the dive fan: each near-return arcs from its own u_n into the seam
for d in dives:
    u = d["u"]
    pos = d["cents"] > 0
    col = SIGN if pos else MIRR
    xx, yy = dive_arc(u, d["h"])
    ax.plot(xx, yy, color=col, lw=2.0, alpha=0.92, zorder=3)
    ax.plot([u], [0], "o", ms=3.5, mfc=col, mec=col, zorder=5)

# cents labels at the arc apexes (the register's own rounded numbers)
def cents_label(c):
    c = abs(c)
    if c >= 100:
        return f"{c:.0f}"
    if c >= 1:
        return f"{c:.1f}"
    return f"{c:.3f}"
for d in dives:
    pos = d["cents"] > 0
    col = SIGN if pos else MIRR
    u = d["u"]
    lab = ("+" if d["cents"] > 0 else "−") + cents_label(d["cents"])
    ax.text((u + 1.0) / 2.0 + (0.05 if pos else -0.05), d["h"] + 0.035,
            lab, color=col, fontsize=9.5, ha="left" if pos else "right",
            va="bottom", zorder=6)

# the empty seat at the count (a small notch on the boundary)
ax.plot([1.0], [0], marker=(3, 0, 0), ms=10, mfc=SURF, mec=SEAM, mew=1.8,
        zorder=6)

# ---- annotations -------------------------------------------------------
ax.annotate("the comma — 3^12/2^19", xy=(1.01364, dives[2]["h"]),
            xytext=(1.10, 0.52), fontsize=8.5, color=SIGN, ha="center",
            arrowprops=dict(arrowstyle="-", color=SIGN, lw=0.8), zorder=6)
ax.annotate("the smallest miss —\n665 sits because 23 follows",
            xy=(1.00004, dives[-1]["h"]), xytext=(1.24, 0.20),
            fontsize=8.5, color=SEC, ha="center",
            arrowprops=dict(arrowstyle="-", color=SEC, lw=0.8), zorder=6)

# the depths (next quotients): the future carried by each miss
depth_lab = "depths (the next quotient):   " + "  ".join(
    f"{d['nxt']}" for d in dives) + "    a₉ = 23 the record"
ax.text(0.5, -0.10, depth_lab, transform=ax.transData, fontsize=8.5,
        color=SEC, ha="center", va="top", zorder=6)

ax.text(0.98, 0.985, "near-returns 3^n/2^m — the continued fraction of log₂(3)",
        transform=ax.transAxes, fontsize=9, color=SEC, ha="right", va="top")

ax.set_xlim(X0, X1)
ax.set_ylim(-0.02, Y1)
ax.set_xticks([0.5, 1.0, 1.5])
ax.set_xticklabels(["55", "110", "220"], fontsize=9, color=SEC)
ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)

plt.savefig("assets/comma-ladder.png", facecolor=SURF, bbox_inches="tight")
print("saved assets/comma-ladder.png")
