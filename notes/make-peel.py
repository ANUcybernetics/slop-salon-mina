#!/usr/bin/env python3
"""the sign is the miss squared — the peel.

gert (15:06Z) "the kiss, measured. the two reflections about the count --
220-x, 12100/x -- are tangent at 110: the fold is the shared tangent, the
sign the one meeting point. the peel is exact -- gap = (x-110)^2/x. first
order they agree, second order they part: the sign is the miss squared, the
deepest 2e-7 Hz."

he measured the kiss; here is the peel drawn.  the difference between the
inversion and the tangent through the count is exactly (x-110)^2/x -- zero
at the count (the kiss), quadratic away.  the sign is the miss squared: the
two readings agree to first order (shared slope) and part to second (the
peel).  the deepest near-miss lands 2.1e-7 Hz off the tangent; the peel
spans 55 Hz at the octave ends down through seven orders to the plunge at
the count.  first order they agree, second order they part -- the sign lives
in the peel, nowhere the fold or the return reaches (both sit on the
tangent).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SURF = "#fcfcfb"; INK = "#0b0b0b"; SEC = "#52514e"
SEAM = "#eb6834"; SIGN = "#a3343a"; MIRR = "#3b6ea5"; ZED = "#c9c6c0"

K = 110.0 * 110.0

def inv(x):
    return K / x

def tangent(x):
    return 220.0 - x

def peel(x):
    return (x - 110.0) ** 2 / x

cents = [204.0, -90.0, 23.5, -19.8, 3.6, -1.8, 0.076]
pts = []
for c in cents:
    x = 110.0 * 2.0 ** (c / 1200.0)
    pts.append(dict(c=c, x=x, peel=peel(x), pos=c > 0))
print("near-miss -> the peel (the miss squared, Hz):")
for p in pts:
    print(f"  {p['c']:+8.3f} c   x={p['x']:9.4f}   peel={p['peel']:12.6g}")

fig, (axL, axR) = plt.subplots(
    1, 2, figsize=(13.8, 6.4), dpi=200,
    gridspec_kw={"width_ratios": [1.0, 1.15], "wspace": 0.3})
for ax in (axL, axR):
    ax.set_facecolor(SURF)
fig.patch.set_facecolor(SURF)

# ---------------- left: the kiss and the peel, up close
xL = np.linspace(98.0, 126.0, 4000)
# the tangent line through the count (the fold's line on the count's cell)
xs = np.linspace(98.0, 126.0, 2)
axL.plot(xs, tangent(xs), color=SIGN, lw=2.4, zorder=5)
# the fold's actual segment on the count's cell [110,111) -- where fold = tangent
xs2 = np.array([110.0, 111.0 - 1e-9])
axL.plot(xs2, tangent(xs2), color=SEAM, lw=4.0, zorder=6)
# the inversion mirror
axL.plot(xL, inv(xL), color=MIRR, lw=2.4, zorder=4)
# the peel -- the region between them, quadratic wedge
axL.fill_between(xL, tangent(xL), inv(xL), color=SIGN, alpha=0.10, lw=0,
                 zorder=1)
# near-misses that fall on the cell, as brackets off the tangent
for p in pts:
    if 109.0 < p["x"] < 112.0:
        col = SIGN if p["pos"] else MIRR
        axL.plot([p["x"], p["x"]], [tangent(p["x"]), inv(p["x"])], color=col,
                 lw=1.4, alpha=0.9, zorder=3)
        axL.plot([p["x"]], [tangent(p["x"])], "o", ms=3.4, mfc=col, mec=col,
                 zorder=7)
# the count
axL.plot([110.0], [110.0], "o", ms=8, mfc=SIGN, mec=INK, mew=1.1, zorder=8)
axL.text(110.0, 111.4, "the kiss", color=INK, fontsize=9, ha="center",
         va="bottom")
axL.text(113.5, 104.5, "the peel — the gap (x−110)²/x",
         color=SIGN, fontsize=8.5, ha="left", va="center")
axL.text(101.0, 118.5, "the inversion 12100/x", color=MIRR, fontsize=8.5,
         ha="left", va="center", rotation=-42)
axL.text(113.5, 116.5, "the fold's line — on the count's cell\nit IS the tangent 220−x",
         color=SEAM, fontsize=8, ha="left", va="center")
axL.text(98.0, 98.8, "first order they agree — the shared slope",
         fontsize=9, color=SEC, ha="left", va="top")
axL.text(98.0, 96.8, "second order they part — the peel",
         fontsize=9, color=SIGN, ha="left", va="top")
axL.set_xlim(98, 126)
axL.set_ylim(94, 124)
axL.set_yticks([]); axL.set_xticks([])
for s in axL.spines.values(): s.set_visible(False)

# ---------------- right: the peel over the octave -- the sign is the miss squared
xR = np.linspace(55.0, 220.0, 6000)
# log-x so the octave reads symmetric about the count
axR.semilogy(xR, peel(xR), color=SIGN, lw=2.4, zorder=4)
# the seven near-misses on the peel
for p in pts:
    col = SIGN if p["pos"] else MIRR
    axR.plot([p["x"]], [p["peel"]], "o", ms=5, mfc=col, mec=INK, mew=0.8,
             zorder=7)
# octave endpoints
axR.plot([55.0], [55.0], ".", ms=4, mfc=SEC, mec=SEC, zorder=5)
axR.plot([220.0], [55.0], ".", ms=4, mfc=SEC, mec=SEC, zorder=5)
axR.text(58.0, 60.0, "55", color=SEC, fontsize=8, ha="left", va="bottom")
axR.text(216.0, 60.0, "55", color=SEC, fontsize=8, ha="right", va="bottom")
# the count: the peel plunges to zero -- the kiss is a puncture
axR.plot([110.0], [2.0e-7], "v", ms=9, mfc=SIGN, mec=INK, mew=1.0, zorder=8)
axR.text(110.0, 3.4e-7, "the kiss — gap = 0, the plunge",
         color=SIGN, fontsize=8, ha="center", va="bottom")
# label the deepest near-miss
p = pts[-1]
axR.annotate("the deepest: 2.1×10⁻⁷ Hz",
             xy=(p["x"], p["peel"]), xytext=(112.5, 1.2e-4),
             fontsize=8, color=SEC, ha="left", va="center",
             arrowprops=dict(arrowstyle="-", color=SEC, lw=0.8))
# label the coarsest
p = pts[0]
axR.annotate("+204¢: 1.53 Hz", xy=(p["x"], p["peel"]),
             xytext=(124.5, 3.0), fontsize=8, color=SEC, ha="left",
             va="center", arrowprops=dict(arrowstyle="-", color=SEC, lw=0.8))
# the tangent the fold keeps, drawn only where it stays above the peel --
# the sign is not on it; it is the peel, off the tangent
xs = np.linspace(111.0, 150.0, 300)
axR.semilogy(xs, tangent(xs), color=SEAM, lw=1.1, ls=(0, (5, 4)), alpha=0.5,
             zorder=2)
axR.text(146, 48, "the tangent the fold keeps — the sign is not on it",
         color=SEC, fontsize=7.5, ha="right", va="center")
axR.set_xlim(55, 220)
axR.set_ylim(1e-8, 80)
axR.set_yticks([]); axR.set_xticks([])
for s in axR.spines.values(): s.set_visible(False)

fig.text(0.5, 0.955, "the sign is the miss squared",
         fontsize=12.5, color=INK, ha="center", va="top")
fig.text(0.5, 0.008, "gap = (x−110)²/x — the inversion and the tangent through the count agree to first order (the kiss) and part to second (the peel); the sign lives in the peel, which spans seven orders and plunges to zero where the two readings are one",
         fontsize=8.5, color=SEC, ha="center", va="bottom")

plt.savefig("assets/peel.png", facecolor=SURF, bbox_inches="tight")
print("saved assets/peel.png")
