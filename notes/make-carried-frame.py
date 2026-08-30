#!/usr/bin/env python3
"""carried — the count a constant of motion, drawn.

The fold line in motion.  The pair breaths on xy=110^2 (here the ratio axis
u = f/110, so the mirror x -> 12100/x is u -> 1/u): the octave bracket
{1/r, r} and the nested means {HM, AM} shrink toward the count and widen
back, crossing the fold line (the unit circle) at right angles at every
instant — orthogonality carried, the product held.  At the close the pair
makes one long approach to r=1: the brackets collapse onto the count, the
fold's foot climbs the fold line to the seat, never seated.

Shared r(t) with make-carried-sound.py.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fractions import Fraction as F
import os

INF = None
INK = "#0b0b0b"
SEC = "#52514e"
SEAM = "#eb6834"     # the count, the fold line
MIRR = "#3b6ea5"     # the means (HM / AM)
SIGN = "#a3343a"     # the absences (the octave pair)
SURF = "#fcfcfb"
ZED = "#c9c6c0"

# ------------------------------------------------------------ r(t)
def r_of(t):
    out = np.empty_like(t)
    a = t < 22.0
    out[a] = 1.52 + 0.48 * np.cos(2 * np.pi * t[a] / 7.0)
    b = (t >= 22.0) & (t < 27.0)
    out[b] = 1.004 + (1.04 - 1.004) * np.exp(-(t[b] - 22.0) / 1.1)
    out[t >= 27.0] = 1.0045
    return out

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
    th0 = np.arccos(np.clip((x0 - cx) / r, -1.0, 1.0))
    th1 = np.arccos(np.clip((x1 - cx) / r, -1.0, 1.0))
    th = np.linspace(th0, th1, n)
    return cx + r * np.cos(th), r * np.sin(th)

SEED = (F(0), F(1), INF)
tiles = generate_tiles(SEED, 4)
edges = edges_of(tiles)

def pair_geod(r):
    a, b = 1.0 / r, r
    c, rad = (a + b) / 2, (b - a) / 2
    th = np.linspace(np.pi, 0, 220)
    return c + rad * np.cos(th), rad * np.sin(th)

def means(r):
    am = (r + 1.0 / r) / 2
    hm = 2.0 / (r + 1.0 / r)
    return hm, am

def means_geod(r):
    a, b = means(r)
    c, rad = (a + b) / 2, (b - a) / 2
    th = np.linspace(np.pi, 0, 220)
    return c + rad * np.cos(th), rad * np.sin(th)

# ------------------------------------------------------------ figure
FPS = 20
T = 30.0
NF = int(FPS * T)
os.makedirs("/tmp/carried-frames", exist_ok=True)

tt = np.arange(NF) / FPS
rr = r_of(tt)

fig, ax = plt.subplots(figsize=(8, 6), dpi=120)
fig.patch.set_facecolor(SURF)
ax.set_facecolor(SURF)

for (a, b) in edges:
    if a is INF or b is INF:
        continue
    xs, ys = geodesic(a, b)
    ax.plot(xs, ys, color=ZED, lw=0.55, alpha=0.28, zorder=1)

ax.plot([-0.12, 2.75], [0, 0], color=INK, lw=1.0, zorder=2)

# the fold line (the count-mirror): static
ux, uy = arc(0.0, 1.0, -1.0, 1.0)
ax.plot(ux, uy, color=SEAM, lw=2.6, zorder=4)
ax.text(0.16, 1.22, "the fold line", color=SEAM, fontsize=10,
        ha="center", va="center", zorder=6)
ax.text(0.16, 1.04, "x ↦ 12100/x, fixing 110", color=SEC, fontsize=8,
        ha="center", va="center", zorder=6)

# count cusp: the star that never moves
ax.plot(1.0, 0, "*", ms=15, color=SEAM, mec="white", mew=0.8, zorder=6)
ax.text(1.0, -0.44, "the count", fontsize=8.5, ha="center", va="top",
        color=SEC, zorder=6)

# a soft glow behind the count, strengthened on the approach
gx, gy = np.meshgrid(np.linspace(-1, 1, 160), np.linspace(-1, 1, 120))
glow = np.zeros((120, 160, 4))
glow[..., 3] = np.exp(-(gx**2 + gy**2) / 0.15)
glow_im = ax.imshow(glow, extent=[1 - 0.55, 1 + 0.55, 0.55, -0.55],
                    zorder=0, alpha=0.0, aspect="auto")

# the moving artists
outer_arc, = ax.plot([], [], color=SIGN, lw=2.2, zorder=4)
inner_arc, = ax.plot([], [], color=MIRR, lw=2.2, zorder=4)
upper_dot, = ax.plot([], [], "o", ms=7, mfc=SIGN, mec="white", mew=0.6, zorder=6)
lower_dot, = ax.plot([], [], "o", ms=7, mfc=SIGN, mec="white", mew=0.6, zorder=6)
upper_lab = ax.text(0, 0, "", fontsize=8.5, ha="left", va="center",
                    color=SIGN, zorder=6)
lower_lab = ax.text(0, 0, "", fontsize=8.5, ha="right", va="center",
                    color=SIGN, zorder=6)
foot_dot, = ax.plot([], [], "o", ms=6, mfc=SURF, mec=SEAM, mew=1.6, zorder=6)
foot_line, = ax.plot([], [], color=SEAM, lw=0.9, ls=(0, (3, 3)), zorder=3)

ax.set_xlim(-0.12, 2.75)
ax.set_ylim(-0.75, 1.4)
ax.set_aspect("equal")
ax.axis("off")

for i in range(NF):
    r = rr[i]
    hm, am = means(r)

    outer_arc.set_data(*pair_geod(r))
    inner_arc.set_data(*means_geod(r))

    upper_dot.set_data([r], [0])
    lower_dot.set_data([1.0 / r], [0])
    if i % FPS == 0:
        upper_lab.set_text("110·r")
        lower_lab.set_text("110/r")
    upper_lab.set_position((r + 0.03, -0.20))
    lower_lab.set_position((1.0 / r - 0.03, -0.20))

    fy = np.sqrt(max(0.0, 1.0 - hm * hm))
    foot_dot.set_data([hm], [fy])
    foot_line.set_data([hm, hm], [fy, 0])

    glow_im.set_alpha(0.16 * (1.0 - (r - 1.0) / 1.0))

    fig.savefig("/tmp/carried-frames/f%03d.png" % i)

print("rendered", NF, "frames")
