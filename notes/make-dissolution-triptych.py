#!/usr/bin/env python3
"""the dissolution typology, completed — dispersion / unweaving / the peel.

june 30 left this open: "two phenomena, one name" — gert's dispersion (no
seam, the medium's resistance, no preferred path) vs mina's unweaving (a
seam, coming apart along its own joints). "a typology, not a single
phenomenon." the typology was never finished.

aug 30 closed the seam with the peel: gap = (x-110)^2/x. the count is a
tangency — the inversion 12100/x and the fold's line 220-x share a seam at
110, and the seam releases to second order. that IS the june definition of
unweaving, now with the "how" measured. two registers apart, the open
typology closed from the other end.

the asymmetry: dispersion has no seam, so no law. unweaving has a seam, so
the release has a form. only the seamed dissolution is measurable — the
sign lives at the joint.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

SURF = "#fcfcfb"; INK = "#0b0b0b"; SEC = "#52514e"
SEAM = "#eb6834"; SIGN = "#a3343a"; MIRR = "#3b6ea5"; ZED = "#c9c6c0"

K = 110.0 * 110.0

def inv(x):   return K / x
def tangent(x): return 220.0 - x
def peel(x):  return (x - 110.0) ** 2 / x

fig, axes = plt.subplots(1, 3, figsize=(15.2, 5.6), dpi=200,
                         gridspec_kw={"wspace": 0.28})
for ax in axes:
    ax.set_facecolor(SURF)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
fig.patch.set_facecolor(SURF)

# ---------------- panel 1: dispersion (gert) — no seam, diffusive
ax = axes[0]
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
# a vertical line source at x=3, structure losing its surface
xs = np.linspace(3.0, 10.0, 400)
rng = np.random.default_rng(20260630)
ax.plot([3, 3], [1, 9], color=INK, lw=2.0, zorder=5)
for i in range(26):
    x0 = 3.0 + 0.05 * rng.standard_normal()
    y = np.linspace(1.0, 9.0, 400) + 0.5 * rng.standard_normal()
    # offset grows like diffusion from the source
    off = 4.5 * np.exp(-((y - 5.0) ** 2) / (2 * 4.0 ** 2)) * rng.standard_normal()
    off = np.clip(off, -2.6, 2.6)
    ax.plot(x0 + off, y, color=SEC, lw=0.5, alpha=0.55)
# the seam-less medium: no joint anywhere, just a widening fan
ax.annotate("", xy=(8.9, 8.6), xytext=(8.9, 7.2),
            arrowprops=dict(arrowstyle="-|>", color=SEC, lw=1.0))
ax.text(9.0, 8.9, "no seam", color=SEC, fontsize=8, ha="right", style="italic")
ax.text(5.0, 0.4, "dispersion", color=INK, fontsize=11, ha="center")
ax.text(5.0, 9.6, "structure without a surface", color=SEC, fontsize=8,
        ha="center", style="italic")

# ---------------- panel 2: unweaving (mina, june 30) — a seam comes apart
ax = axes[1]
ax.set_xlim(0, 10); ax.set_ylim(0, 10)
n = 14
ys = np.linspace(1.2, 8.8, n)
seam_x = lambda y: 2.0 + 0.72 * (y - 1.2)   # diagonal seam, left-high
for i, y in enumerate(ys):
    # woven above the seam: strands held by weave-ticks
    sx = seam_x(y)
    ax.plot([0.5, sx], [y, y], color=INK, lw=1.1)
    if i < n - 1:
        # weave ticks between adjacent strands, only in the woven zone
        wx = np.linspace(0.6, seam_x(y) - 0.1, 7)
        for w in wx:
            ax.plot([w, w], [y, y + (ys[1] - ys[0])], color=ZED, lw=0.9)
    # unwoven below the seam: strands pull apart, gap widening
    gap = 0.10 + 0.75 * (y - 1.2) / 7.6
    ax.plot([sx, 9.3], [y + gap, y + gap + 1.7 * (y - 1.2) / 7.6],
            color=SEC, lw=0.8, alpha=0.9)
# the seam itself
ysl = np.linspace(1.2, 8.8, 30)
ax.plot(seam_x(ysl), ysl, color=SEAM, lw=2.2, zorder=6)
ax.text(seam_x(8.8) + 0.25, 8.6, "the seam", color=SEAM, fontsize=8,
        ha="left", style="italic")
ax.text(5.0, 0.4, "unweaving", color=INK, fontsize=11, ha="center")
ax.text(5.0, 9.6, "the seam dictates how it comes apart", color=SEC,
        fontsize=8, ha="center", style="italic")

# ---------------- panel 3: the peel (aug 30) — the release, measured
ax = axes[2]
ax.set_xlim(96, 128); ax.set_ylim(96, 128)
x = np.linspace(96, 128, 600)
# the fold's line through the count (the shared tangent)
ax.plot(x, tangent(x), color=SIGN, lw=2.2, zorder=5)
# the inversion
ax.plot(x, inv(x), color=MIRR, lw=2.2, zorder=5)
# the quadratic wedge between them: the peel, shaded
wedge = Polygon(np.column_stack([
                    np.concatenate([x, x[::-1]]),
                    np.concatenate([tangent(x), inv(x[::-1])])]),
                closed=True, facecolor=SIGN, alpha=0.08, zorder=2)
ax.add_patch(wedge)
ax.plot([110], [110], "o", color=INK, ms=6, zorder=7)
ax.text(110, 101, "the count", color=INK, fontsize=8, ha="center")
# one explicit gap arrow: the seam's release at x=106
gx = 106.0
ax.annotate("", xy=(gx, inv(gx)), xytext=(gx, tangent(gx)),
            arrowprops=dict(arrowstyle="<->", color=SEAM, lw=1.4))
ax.text(gx + 1.6, 117, "gap = (x−110)²/x", color=SEAM, fontsize=8,
        va="center")
ax.text(112, 118.5, "the release, measured", color=INK, fontsize=11)
ax.text(112, 115.0, "first order they agree,\nsecond order they part",
        color=SEC, fontsize=8, style="italic")
ax.text(96, 96, "the inversion and the fold's line", color=SEC, fontsize=7,
        ha="left")

fig.suptitle("two phenomena, one name — the typology, completed",
             color=INK, fontsize=13, y=0.97)
fig.savefig("assets/dissolution-triptych.png", dpi=200,
            facecolor=SURF, bbox_inches="tight")
print("wrote assets/dissolution-triptych.png")

# numeric check of the link: the peel at a few points = the seam's release
for xx in (100, 104, 106, 108, 110, 112, 116):
    print(f"  x={xx:5.1f}  inv-tangent = gap = {inv(xx)-tangent(xx):10.4f}  "
          f"peel = {(xx-110)**2/xx:10.4f}")
