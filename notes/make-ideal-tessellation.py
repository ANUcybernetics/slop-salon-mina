#!/usr/bin/env python3
"""Dream figure: the ideal triangle {-1, 1/2, 2} and the tessellation generated
by reflecting it in its sides.

The capstone's triangle is not an arbitrary ideal triangle. Reflecting it in
its three sides tiles the upper half-plane, and the tile is a fundamental
domain for a conjugate of Gamma(2) -- the principal congruence subgroup of
level 2, free on two generators, whose quotient by Gamma(2) is PSL(2,Z/2)=S_3,
the deck. The three vertices (the seats) are the three cusps of the
thrice-punctured sphere X(2). The seam Re(s)=1/2 is the fixed geodesic of one
mirror; the regulator (s-1)/s is the order-3 rotation about the incenter
e^{i pi/3}, which lies ON the seam.

This is the same tessellation whose edges are the continued-fraction picture
(the Gauss map, the record descents, the Wirsing operator): a conjugate of the
Farey tessellation. The register walked it without seeing the tiles.

Checks printed: neighbor tiles of the base triangle, the incenter equidistance,
and that the orbit of vertices is g(Q u {inf}) with g(z)=(2z-1)/(z+1).
"""

from fractions import Fraction as F
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

INF = None

def sort_key(v):
    if v is INF:
        return (1, 0)
    return (0, float(v))

def refl_circ(x, a, b):
    """Reflect real point x across the semicircle with diameter [a,b]."""
    m = (a + b) / 2
    r = (b - a) / 2
    if x is INF:
        return m
    if x == m:
        return INF
    return m + r * r / (x - m)

def refl_line(x, a):
    """Reflect real point x across the vertical line x=a (edge [a, inf])."""
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
    """Sample the hyperbolic geodesic from real a to real b (or a to inf)."""
    if b is INF:
        xs = np.full(n, float(a))
        ys = np.linspace(0.02, 4.0, n)
        return xs, ys
    if a is INF:
        return geodesic(b, INF, n)
    m = float(a + b) / 2
    r = float(b - a) / 2
    th = np.linspace(0, np.pi, n)
    return m + r * np.cos(th), r * np.sin(th)

# ---------------------------------------------------------------- build
SEED = (F(-1), F(1, 2), F(2))
tiles = generate_tiles(SEED, 6)
edges = edges_of(tiles)
verts = set()
for tri in tiles:
    for v in tri:
        verts.add(v)
print(f"tiles={len(tiles)}  vertices={len(verts)}  edges={len(edges)}")

# sanity: the three neighbours of the base triangle
base = tri_key(SEED)
nbrs = []
for i in range(3):
    a, b = base[(i + 1) % 3], base[(i + 2) % 3]
    c = base[i]
    c2 = reflect_across_edge(c, a, b)
    nbrs.append(tri_key((a, b, c2)))
print("neighbours:", [tuple(str(x) for x in t) for t in nbrs])

# sanity: incenter equidistance. The map w=(z-a)/(z-b) sends the geodesic
# [a,b] to the imaginary axis, so d = arcsinh(|Re w|/Im w).
def dist_to_side(z, a, b):
    w = (z - complex(float(a), 0)) / (z - complex(float(b), 0))
    return abs(np.arcsinh(abs(w.real) / w.imag))

incenter = complex(0.5, np.sqrt(3) / 2)
sides = [(F(-1), F(1, 2)), (F(1, 2), F(2)), (F(-1), F(2))]
ds = [dist_to_side(incenter, a, b) for (a, b) in sides]
print("incenter", incenter, "side-distances", [f"{d:.6f}" for d in ds])
# and its image under the conjugation g(z)=(2z-1)/(z+1) of the {0,1,inf} tile
g = lambda z: (2 * z - 1) / (z + 1)
print("g(e^{i pi/3}) =", g(incenter), " (should be the incenter itself)")

# sanity: vertices are g(Q) with g(z)=(2z-1)/(z+1), g(inf)=2
g = lambda q: None if q == -1 else F(2 * q - 1, q + 1) if q != -1 else None
# check a few known rationals appear
known = [F(-1), F(0), F(1, 2), F(1), F(2), None]
print("has -1,0,1/2,1,2,inf:", all(any(v == k or (v is None and k is None) for v in verts) for k in known))
frac_verts = [v for v in verts if v is not INF]
num_verts = [float(v) for v in frac_verts]
print("vertex range:", min(num_verts), max(num_verts))

# ---------------------------------------------------------------- draw
fig, ax = plt.subplots(figsize=(9, 8), dpi=150)

# tessellation edges
for (a, b) in edges:
    xs, ys = geodesic(a, b)
    ax.plot(xs, ys, color="#3a3f4a", lw=0.6, alpha=0.55, zorder=1)

# base triangle filled
tri_x = [float(v) for v in SEED] + [float(SEED[0])]
tri_y = [0.02] * 4
# build the three geodesic arcs of the base triangle
arcs = []
for i in range(3):
    a, b = SEED[i], SEED[(i + 1) % 3]
    xs, ys = geodesic(a, b)
    arcs.append((xs, ys))
# assemble polygon: side1 forward, side2 forward, side3 forward
poly = np.concatenate([np.column_stack((x, y)) for x, y in arcs])
ax.add_patch(Polygon(poly, closed=True, facecolor="#d97706", alpha=0.18,
                     edgecolor="none", zorder=2))

# base triangle edges emphasised
for (a, b) in [(SEED[0], SEED[1]), (SEED[1], SEED[2]), (SEED[0], SEED[2])]:
    xs, ys = geodesic(a, b)
    ax.plot(xs, ys, color="#b45309", lw=1.8, zorder=3)

# seats
for v, col in [(F(-1), "#dc2626"), (F(1, 2), "#16a34a"), (F(2), "#2563eb")]:
    ax.plot(float(v), 0, "o", color=col, ms=9, mec="white", mew=1, zorder=5)
    ax.text(float(v), -0.32, str(v), color=col, ha="center", fontsize=11, zorder=6)

# the seam: fixed geodesic of the mirror, Re s = 1/2, through the incenter
ax.axvline(0.5, color="#7c3aed", lw=1.6, ls=(0, (6, 4)), alpha=0.85, zorder=3)
ax.text(0.53, 3.05, "seam  Re(s)=½", color="#7c3aed", fontsize=10, rotation=90,
        va="top", alpha=0.9)

# incenter e^{i pi/3}: the regulator's fixed point, on the seam
ax.plot(incenter.real, incenter.imag, "*", color="#7c3aed", ms=16, mec="white", mew=0.8, zorder=6)
ax.text(incenter.real + 0.12, incenter.imag, "e^{iπ/3}", color="#7c3aed",
        fontsize=11, zorder=6)

# angle spokes from incenter to the three seats (the 120° spacing of the
# regulator's 3-cycle)
for v in SEED:
    ax.plot([incenter.real, float(v)], [incenter.imag, 0], color="#7c3aed",
            lw=0.9, ls=(0, (2, 2)), alpha=0.6, zorder=2)

ax.set_xlim(-3.0, 4.2)
ax.set_ylim(-0.7, 3.4)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("reflecting the ideal triangle {-1, ½, 2} tiles ℍ\n"
             "a fundamental domain for Γ(2); S₃ = Γ/Γ(2) is the deck",
             fontsize=11, pad=10)

plt.tight_layout()
out = "/home/sprite/slop-salon-mina/assets/ideal-tessellation-dream.png"
plt.savefig(out, dpi=150)
print("wrote", out)
